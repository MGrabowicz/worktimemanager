from django.urls import path

from accounts.views import signupView, activateUser, resendActivationEmailView, passwordResetRequestView, \
    passwordResetView, editProfileView

urlpatterns = [
    path('signup/', signupView, name='signup'),
    path('activateUser/<uidb64>/<token>', activateUser, name='activate'),
    path('resendActivationEmail', resendActivationEmailView, name='resendActivationEmail'),
    path('passwordResetForm/<uidb64>/<token>', passwordResetView, name='passwordResetForm'),
    path('passwordReset', passwordResetRequestView, name='passwordReset'),
    path('editProfile', editProfileView, name='editProfile'),
]
