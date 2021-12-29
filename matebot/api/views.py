import json

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
import rc_protocol
from django.views.decorators.csrf import csrf_exempt

from api import models


@method_decorator(csrf_exempt, name='dispatch')
class AuthView(View):
    """This is the base class to ensure requests are only allowed when authenticated"""

    def _check_auth(self, request, data=None):
        if "Authorization" not in request.headers:
            return JsonResponse({"success": False, "info": "Authentication failed"}, status=401)
        if " " not in request.headers["Authorization"]:
            return JsonResponse({"success": False, "info": "Authentication failed"}, status=401)
        checksum = request.headers["Authorization"].split(" ")[1]
        if request.META["REQUEST_METHOD"] == "GET":
            if not any([
                rc_protocol.validate_checksum(
                    dict(((x, request.GET[x]) for x in request.GET)),
                    checksum,
                    x.token,
                    salt=request.path
                )
                for x in models.ApplicationModel.objects.all()
            ]):
                return JsonResponse({"success": False, "info": "Authorization failed"}, status=403)
        elif request.META["REQUEST_METHOD"] == "POST":
            if not any([
                rc_protocol.validate_checksum(data, checksum, x.token, salt=request.path)
                for x in models.ApplicationModel.objects.all()
            ]):
                return JsonResponse({"success": False, "info": "Authorization failed"}, status=403)
        else:
            return JsonResponse({"success": False, "info": "Method not supported"}, status=405)

    def get(self, request: WSGIRequest, *args, **kwargs):
        ret = self._check_auth(request)
        if isinstance(ret, JsonResponse):
            return ret
        return self.secure_get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            decoded = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "info": "JSON could not be decoded"}, status=400)
        ret = self._check_auth(request, data=decoded)
        if isinstance(ret, JsonResponse):
            return ret
        return self.secure_post(request, decoded, *args, **kwargs)

    def secure_get(self, request, *args, **kwargs):
        return JsonResponse({"success": False, "info": "Method not allowed"}, status=405)

    def secure_post(self, request, decoded, *args, **kwargs):
        return JsonResponse({"success": False, "info": "Method not allowed"}, status=405)


class GetConsumableView(AuthView):
    def secure_get(self, request, *args, **kwargs):
        data = [x.to_dict() for x in models.ConsumableModel.objects.all()]
        return JsonResponse({"success": True, "data": data})


class GetUserView(AuthView):
    def secure_get(self, request, *args, **kwargs):
        if "filter" in request.GET:
            try:
                data = models.UserModel.objects.get(id=request.GET["filter"]).to_dict()
            except models.UserModel.DoesNotExist:
                return JsonResponse({"success": True, "data": []})
        else:
            data = [x.to_dict() for x in models.UserModel.objects.all()]
        return JsonResponse({"success": True, "data": data})


class CreateUserView(AuthView):

    def secure_post(self, request: WSGIRequest, decoded: dict, *args, **kwargs):
        required = ["application_id", "user_alias"]
        if not all([x in decoded for x in required]):
            return JsonResponse({"success": False, "info": "Missing mandatory parameter"}, status=400)
        try:
            name = decoded["name"] if "name" in decoded else ""
        except ValueError:
            return JsonResponse({"success": False, "info": "Bad parameter type"}, status=400)
        try:
            application = models.ApplicationModel.objects.get(id=decoded["application_id"])
        except models.ApplicationModel.DoesNotExist:
            return JsonResponse({"success": False, "info": "Application with that ID does not exist"}, status=400)
        user = models.UserModel.objects.create(name=name)
        models.UserAliasModel.objects.create(
            user_alias=decoded["user_alias"],
            application=application,
            user=user
        )
        return JsonResponse({"success": True, "data": user.id})


class PerformTransactionView(AuthView):

    def secure_post(self, request, decoded, *args, **kwargs):
        required = ["sender_id", "receiver_id", "amount", "reason"]
        if not all([x in decoded for x in required]):
            return JsonResponse({"success": False, "info": "Missing mandatory parameter"}, status=400)
        try:
            sender = models.UserModel.objects.get(id=decoded["sender_id"])
            receiver = models.UserModel.objects.get(id=decoded["receiver_id"])
        except models.UserModel.DoesNotExist:
            return JsonResponse({"success": False, "info": "Sender or Received not found"}, status=400)
        try:
            amount = int(decoded["amount"])
            if amount <= 0:
                raise ValueError
        except ValueError:
            return JsonResponse({"success": False, "info": "Amount was no positive integer"}, status=400)
        reason = decoded["reason"]
        transaction = models.TransactionModel.objects.create(
            sender=sender, receiver=receiver, amount=amount, reason=reason
        )
        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()
        return JsonResponse({"success": True, "data": transaction.id})


class GetHistoryView(AuthView):

    def secure_get(self, request, *args, **kwargs):
        required = ["target_id"]
        if not all([x in request.GET for x in required]):
            return JsonResponse({"success": False, "info": "Missing mandatory parameter"}, status=400)
        target_id = request.GET["target_id"]
        try:
            target = models.UserModel.objects.get(id=target_id)
        except models.UserModel.DoesNotExist:
            return JsonResponse({"success": False, "info": "Target user is invalid"}, status=400)
        if "amount" in request.GET:
            try:
                amount = int(request.GET["amount"])
                if amount <= 0:
                    raise ValueError
            except ValueError:
                return JsonResponse({"success": False, "info": "Amount is no valid positive integer"}, status=400)
        else:
            amount = 10
        transactions = models.TransactionModel.objects.filter(receiver=target).order_by("-created")[:amount]
        return JsonResponse({"success": True, "data": [x.to_dict() for x in transactions]})
