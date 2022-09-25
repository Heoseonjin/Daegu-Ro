from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>', views.BoardDetail.as_view()),
    path('', views.BoardList.as_view()),
]