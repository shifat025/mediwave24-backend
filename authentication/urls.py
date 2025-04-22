from django.urls import path
from .views import UserSignupView, EmailVerification,LoginView


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uid64>/<token>/', EmailVerification.as_view(), name='verify-email')
]
