from django.urls import path
from .views import MyPage, SignUp, AnyUsers

urlpatterns = [
    path('mypage/', MyPage.as_view(), name='mypage'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('users/<int:pk>', AnyUsers.as_view(), name='users')
]
