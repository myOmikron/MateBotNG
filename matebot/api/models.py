from django.db import models
from django.db.models import CharField, IntegerField, BooleanField, ForeignKey, DateTimeField, ManyToManyField


class ApplicationModel(models.Model):
    """This class represents an application.

    The token is used to authenticate the application via RCP.
    """
    token = CharField(max_length=255)


class UserModel(models.Model):
    """This represents the basic user.

    It is not bound to any application and can be accessed by all applications.
    """
    name = CharField(max_length=255, null=True, blank=True)
    balance = IntegerField(default=0)
    active = BooleanField(default=True)
    internal = BooleanField(default=False)
    voucher = ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "identifier": self.id,
            "name": self.name,
            "balance": self.balance,
            "active": self.active,
            "internal": self.internal,
            "voucher_id": self.voucher_id,
            "vouched_for": [x.id for x in self.usermodel_set.all()],
            "user_alias_ids": dict((x.application_id, x.user_alias) for x in self.useraliasmodel_set.all()),
            "created": self.created.timestamp(),
            "modified": self.modified.timestamp()
        }


class UserAliasModel(models.Model):
    """This Model represents an alias.

    Aliases are in use to overcome the different usernames and ids of applications.
    """
    user_alias = CharField(max_length=255)
    application = ForeignKey(ApplicationModel, on_delete=models.CASCADE)
    user = ForeignKey(UserModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_alias


class ApplicationCallbackModel(models.Model):
    """Callback to an application.

    Username and password is used via http basic auth.
    """
    uri = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)


class TransactionModel(models.Model):
    """This model represents a transaction between two users"""
    sender = ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name="transaction_sender")
    receiver = ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name="transaction_receiver")
    amount = IntegerField()
    reason = CharField(max_length=255, default="", blank=True)
    created = DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "amount": self.amount,
            "reason": self.reason,
            "created": self.created.timestamp()
        }


class ConsumableMessageModel(models.Model):
    """This represents a message that is sent when a consumable is consumed."""
    message = CharField(max_length=255)


class ConsumableModel(models.Model):
    """This model represents a consumable."""
    name = CharField(max_length=255, unique=True)
    description = CharField(max_length=255, default="", blank=True)
    price = IntegerField()
    symbol = CharField(max_length=15)
    messages = ManyToManyField(ConsumableMessageModel, blank=True)

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "symbol": self.symbol,
            "messages": [x.message for x in self.messages.all()]
        }


class VoteModel(models.Model):
    """Model that is used to represent a single Vote."""
    positive = BooleanField()
    user = ForeignKey(UserModel, on_delete=models.DO_NOTHING)

    modified = DateTimeField(auto_now=True)


class RefundModel(models.Model):
    """This represents the action of a payment from the community user to another user."""
    amount = IntegerField()
    reason = CharField(max_length=255, blank=True, default="")
    active = BooleanField(default=True)
    creator = ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    transaction = ForeignKey(TransactionModel, on_delete=models.DO_NOTHING, null=True)
    votes = ManyToManyField(VoteModel, blank=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class MembershipPollModel(models.Model):
    """This class represents a poll. Polls are used to accept the membership requests of users"""
    votes = ManyToManyField(VoteModel, blank=True)
    creator = ForeignKey(UserModel, on_delete=models.CASCADE)
    active = BooleanField(default=False)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class CommunismUserModel(models.Model):
    """User model for communisms.

    Links a user to a quantity
     - quantity specifies the relative amount a user has consumed:
            q/n, where n = participants of communism and q = quantity
    """
    user = ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    quantity = IntegerField(default=1)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "quantity": self.quantity
        }


class CommunismModel(models.Model):
    """Model for communisms.

    Use this to distribute costs among other users.
    n = participants including "external" users
    q = quantity of one user (user + its added externals)

    So each user pays q/n * amount to the creator
    """
    active = BooleanField(default=True)
    amount = IntegerField()
    reason = CharField(max_length=255)
    creator = ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    participants = ManyToManyField(CommunismUserModel, blank=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "identifier": self.id,
            "active": self.active,
            "amount": self.amount,
            "reason": self.reason,
            "creator_id": self.creator_id,
            "participants": [x.to_dict() for x in self.participants.all()],
            "created": self.created.timestamp(),
            "modified": self.modified.timestamp()
        }

