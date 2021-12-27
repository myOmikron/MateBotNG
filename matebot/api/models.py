from django.db import models
from django.db.models import CharField, IntegerField, BooleanField, ForeignKey, DateTimeField, ManyToManyField


class ApplicationModel(models.Model):
    """This class represents an application.

    The token is used to authenticate the application via RCP.
    """
    token = CharField(max_length=255)


class UserAliasModel(models.Model):
    """This Model represents an alias.

    Aliases are in use to overcome the different usernames and ids of applications.
    """
    app_user_id = CharField(max_length=255, unique=True)
    application = ForeignKey(ApplicationModel, on_delete=models.CASCADE)

    def __str__(self):
        return self.app_user_id


class UserModel(models.Model):
    """This represents the basic user.

    It is not bound to any application and can be accessed by all applications.
    """
    name = CharField(max_length=255, null=True)
    balance = IntegerField(default=0)
    complete_access = BooleanField(default=False)
    active = BooleanField(default=True)
    external = BooleanField(default=False)
    voucher = ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)
    user_aliases = ManyToManyField(UserAliasModel, blank=True)

    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "identifier": self.id,
            "name": self.name,
            "balance": self.balance,
            "complete_access": self.complete_access,
            "active": self.active,
            "external": self.external,
            "voucher_id": self.voucher_id,
            "user_alias_ids": [x for x in self.user_aliases.values("id")],
            "created": self.created.timestamp(),
            "modified": self.modified.timestamp()
        }


class ApplicationCallbackModel(models.Model):
    """Callback to an application.

    Username and password is used via http basic auth.
    """
    uri = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)


class TransactionModel(models.Model):
    sender = ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name="transaction_sender")
    receiver = ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name="transaction_receiver")
    amount = IntegerField()
    reason = CharField(max_length=255, default="", blank=True)
    created = DateTimeField(auto_now_add=True)


class MultiTransactionModel(models.Model):
    transactions = ManyToManyField(TransactionModel)
    created = DateTimeField(auto_now_add=True)


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


class VoteModel(models.Model):
    """Model that is used to represent a single Vote.

    -1: Disapproved
    0 : Abstained from voting
    1 : Approved
    """
    vote = IntegerField(default=0)
    user = ForeignKey(UserModel, on_delete=models.DO_NOTHING)

    modified = DateTimeField(auto_now=True)


class PollModel(models.Model):
    """This represents a Poll."""
    question = CharField(max_length=255)
    active = BooleanField(default=True)
    votes = ManyToManyField(VoteModel, blank=True)
    modified = DateTimeField(auto_now=True)


class Refund(models.Model):
    """This represents the action of a payment from the community user to another user."""
    amount = IntegerField()
    reason = CharField(max_length=255, blank=True, default="")
    active = BooleanField(default=True)
    creator = ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    transaction = ForeignKey(TransactionModel, on_delete=models.DO_NOTHING, null=True)
    poll = ForeignKey(PollModel, on_delete=models.DO_NOTHING)

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
    accessed = DateTimeField(auto_now=True)

