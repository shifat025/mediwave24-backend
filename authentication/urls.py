from django.urls import path
from .views import UserSignupView, EmailVerification


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('activate/<uid64>/<token>/', EmailVerification.as_view(), name='verify-email')
]
