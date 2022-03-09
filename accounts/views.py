from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.html import format_html
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .models import wtmUser, Team
from .utils import generateToken
from accounts.forms import SignUpForm, LogInForm
from teams.forms import CreateTeamForm
from django.core.mail import EmailMessage
from django.conf import settings


def homeView(request):
    return render(request, 'home.html')


def loginView(request):
    if request.method == 'POST':
        userLoginForm = LogInForm(data=request.POST)
        if userLoginForm.is_valid():
            username = userLoginForm.cleaned_data.get('username')
            password = userLoginForm.cleaned_data.get('password')
            user = User.objects.get(username=username)
            if user.wtmuser.isEmailVerified:
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "You have to activate your account first!")
                messages.error(request,
                               "If you have problem with receiving activation email you can request new one here:")
                messages.error(request,
                               format_html("<a href='/accounts/resendActivationEmail' class='authLink'>Send email</a>"))
                return redirect('login')
        else:
            messages.error(request,
                           "If you don't remeber your password and want to change it click here:")
            messages.error(request,
                           format_html("<a href='/accounts/passwordReset' class='authLink'>Reset password</a>"))
            print(userLoginForm.errors)
    else:
        userLoginForm = LogInForm()
    return render(request, 'accounts/loginT.html', {'loginForm': userLoginForm})


def signupView(request):
    if request.method == 'POST':
        userCreateForm = SignUpForm(request.POST)
        if userCreateForm.is_valid():
            createdUser = userCreateForm.save()
            wtmU = wtmUser(user=createdUser)
            wtmU.save()
            # Turned off for testing purpose
            # sendVerificationEmail(request, createdUser)
            messages.info(request, "Account created successfully.")
            messages.info(request, "Check your mail for activation mail.")
            return redirect('login')
        else:
            print(userCreateForm.errors)
    else:
        userCreateForm = SignUpForm()
    return render(request, 'accounts/signupT.html', {'signupForm': userCreateForm})


def resendActivationEmailView(request):
    if request.POST:
        try:
            username = request.POST.get('username')
            user = User.objects.get(username=username)
            sendVerificationEmail(request, user)
            messages.info(request, "Check your mail for activation mail.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, "No user with that username found.")
            return redirect(reverse('resendActivationEmail'))
    return render(request, 'accounts/resendActivationEmail.html')


def passwordResetRequestView(request):
    if request.POST:
        try:
            email = request.POST.get('Email')
            user = User.objects.get(email=email)
            sendPasswordChangeEmail(request, user)
            messages.info(request, "Check your mail for password reset mail.")
            return redirect(reverse('login'))
        except Exception as e:
            messages.error(request, "No user associated with that email found.")
            return redirect(reverse('passwordReset'))
    return render(request, 'accounts/passwordResetRequest.html')


def passwordResetView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None
    if request.POST:
        passwordResetForm = SetPasswordForm(user=user, data=request.POST)
        if passwordResetForm.is_valid():
            passwordResetForm.save()
            messages.info(request, "Your password was changed successfully.")
            return redirect('login')
        else:
            print(passwordResetForm.errors)
    else:
        passwordResetForm = SetPasswordForm(user=user)
    return render(request, 'accounts/passwordResetForm.html', {'passwordResetForm': passwordResetForm})

def editProfileView(request):
    wtmuser = wtmUser.objects.get(user=request.user)
    personalStartTime = wtmuser.personalStartTime.strftime("%H:%M")
    personalEndTime = wtmuser.personalEndTime.strftime("%H:%M")
    personalBreakTime = wtmuser.personalBreakTime.strftime("%H:%M")

    if request.POST.get('action') == 'saveProfile':
        personalStartTime = request.POST.get('personalStartTime')
        personalEndTime = request.POST.get('personalEndTime')
        personalBreakTime = request.POST.get('personalBreakTime')
        wtmuser.personalStartTime = personalStartTime
        wtmuser.personalEndTime = personalEndTime
        wtmuser.personalBreakTime = personalBreakTime
        wtmuser.save()

    return render(request, 'accounts/editProfile.html', {
        'personalStartTime': personalStartTime,
        'personalEndTime': personalEndTime,
        'personalBreakTime': personalBreakTime,
    })


def sendVerificationEmail(request, user):
    currentSite = get_current_site(request)
    emailSubject = 'Work Time manager - activation email'
    emailBody = render_to_string('emails/activationEmail.html', {
        'user': user,
        'domain': currentSite,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })

    email = EmailMessage(subject=emailSubject, body=emailBody, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


def sendPasswordChangeEmail(request, user):
    currentSite = get_current_site(request)
    emailSubject = 'Work Time manager - password reset email'
    emailBody = render_to_string('emails/passwordResetEmail.html', {
        'user': user,
        'domain': currentSite,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generateToken.make_token(user)
    })

    email = EmailMessage(subject=emailSubject, body=emailBody, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


def activateUser(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception as e:
        user = None

    if user and generateToken.check_token(user, token):
        wtm = wtmUser.objects.get(user=user)
        wtm.isEmailVerified = True
        wtm.save()
        messages.info(request, "Your account has been activated successfully.")
        return redirect(reverse('login'))

    return render(request, 'accounts/activationEmail.html')
