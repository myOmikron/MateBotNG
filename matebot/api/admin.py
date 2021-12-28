from django.contrib import admin

from api.models import *


@admin.register(ApplicationModel)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(UserModel)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(VoteModel)
class VoteAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAliasModel)
class UserAliasAdmin(admin.ModelAdmin):
    pass


@admin.register(ConsumableMessageModel)
class ConsumableMessageAdmin(admin.ModelAdmin):
    pass


@admin.register(ConsumableModel)
class ConsumableAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunismModel)
class CommunismAdmin(admin.ModelAdmin):
    pass


@admin.register(CommunismUserModel)
class CommunismUserAdmin(admin.ModelAdmin):
    pass


@admin.register(TransactionModel)
class TransactionAdmin(admin.ModelAdmin):
    pass


@admin.register(MembershipPollModel)
class MembershipPollAdmin(admin.ModelAdmin):
    pass


@admin.register(RefundModel)
class RefundAdmin(admin.ModelAdmin):
    pass
