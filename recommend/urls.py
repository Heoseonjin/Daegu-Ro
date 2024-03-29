from django.urls import path
from . import views


urlpatterns = [
    path('category/<str:slug>/', views.category_page),
    path('<int:pk>', views.RecommendDetail.as_view()),
    path('', views.RecommendList.as_view()),
]