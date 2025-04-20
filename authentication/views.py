from django.shortcuts import render, redirect
from .serializers import UserRegisterSerializer
from rest_framework.views import APIView, View
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.urls import reverse

from .utils import send_email
from .models import User
# Create your views here.


class UserSignupView(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request):
        user_serializer = self.serializer_class(data= request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"http://127.0.0.1:8000/user/activate/{uid}/{token}/"
            subject = "Active your account"
            template_name = 'active_account.html'
            context = {'confirm_link': confirm_link}
            success = send_email(subject, template_name, context, user)
            if success:
                return Response({'message': 'Signup successful! Check your inbox to activate your account.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Failed to send activation email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            


class EmailVerification(View):
    def get(self, request, uid64, token):
        try:
            uid = urlsafe_base64_decode(uid64).decode()
            user = User.objects.get(pk = uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request,  'Account activated! You can now log in.')
            return redirect("http://127.0.0.1:8000/login")
        
        else:
            messages.error(request,"Verification failed. Please check the link")

        return redirect(reverse('signup'))
