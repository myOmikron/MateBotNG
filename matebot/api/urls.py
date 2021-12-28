from django.urls import path

from api.views import *


urlpatterns = [
    path("getConsumables", GetConsumableView.as_view()),

    path("getUser", GetUserView.as_view()),

]
