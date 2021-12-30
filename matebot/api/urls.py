from django.urls import path

from api.views import *


urlpatterns = [
    path("getConsumables", GetConsumableView.as_view()),

    path("performTransaction", PerformTransactionView.as_view()),

    path("getUser", GetUserView.as_view()),
    path("createUser", CreateUserView.as_view()),
    path("getHistory", GetHistoryView.as_view()),
    path("deleteUserAlias", DeleteUserAliasView.as_view()),


    path("startVouch", StartVouchView.as_view()),
    path("endVouch", EndVouchView.as_view()),


    path("startRefund", StartRefundView.as_view()),
    path("cancelRefund", CancelRefundView.as_view()),
    path("voteRefund", VoteRefundView.as_view()),
]
