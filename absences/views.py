import datetime
import json

import numpy as np
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.messages import get_messages

from absences.models import Absence, getAbsenceTypesForTemplate
from accounts.models import wtmUser
from config import settings


@login_required(login_url='home')
def createAbsenceView(request):
    pendingAbsenceRequestsList = Absence.objects.filter(
        owner=request.user, statusType='SENTTOAPPROVE').order_by('-pk')
    allAbsenceRequestsList = Absence.objects.filter(owner=request.user).order_by('-pk')
    requesterManager = wtmUser.objects.get(user=request.user).team.manager
    absenceTypes = getAbsenceTypesForTemplate()
    if request.POST:
        if request.POST.get('action') == 'sendAbsenceRequest':
            absenceType = request.POST.get('absenceType')
            startDate = request.POST.get('startDate')
            endDate = request.POST.get('endDate')

            if (startDate == endDate):
                workDays = 1
            else:
                workDays = np.busday_count(startDate, endDate)

            if workDays <= 0:
                messages.info(
                    request, "You entered wrong dates, working days sum equal or smaller than 0.")
            else:
                createdAbsenceRequest = Absence.objects.create(
                    owner=request.user, manager=requesterManager, startDate=startDate, endDate=endDate, absenceType=absenceType, workDays=workDays)
                createdAbsenceRequest = Absence.objects.get(pk=createdAbsenceRequest.pk)
                sendEmailNewAbsenceRequestForApproval(
                    request, request.user, requesterManager)
                return JsonResponse({
                                    'djangoMessage': "Absence request has been sent to your manager.",
                                    'userName': request.user.get_full_name(),
                                    'startDate': createdAbsenceRequest.getStartDateForTemplate(),
                                    'endDate': createdAbsenceRequest.getEndDateForTemplate(),
                                    'workDays': createdAbsenceRequest.workDays,
                                    'absenceType': createdAbsenceRequest.getAbsenceRequestType(),
                                    })

    return render(request, 'absences/newAbsence.html', {'requesterManager': requesterManager,
                                                        'absenceTypes': absenceTypes,
                                                        'pendingAbsenceRequestsList': pendingAbsenceRequestsList,
                                                        'allAbsenceRequestsList': allAbsenceRequestsList
                                                        })


@login_required(login_url='home')
def absenceRequestsSentForApprovalListView(request):
    absenceRequestsList = Absence.objects.filter(
        manager=request.user, statusType='SENTTOAPPROVE')
    if request.POST:
        if request.POST.get('action') == 'approveAbsenceRequest':
            absenceRequestPk = request.POST.get('absenceRequestPk')
            absenceRequest = Absence.objects.get(pk=absenceRequestPk)
            absenceRequest.statusType = 'APPROVED'
            absenceRequest.save()
        if request.POST.get('action') == 'declineAbsenceRequest':
            absenceRequestPk = request.POST.get('absenceRequestPk')
            absenceRequest = Absence.objects.get(pk=absenceRequestPk)
            absenceRequest.statusType = 'DECLINED'
            absenceRequest.save()

    return render(request, 'absences/absenceRequestsToAccept.html', {'absenceRequestsList': absenceRequestsList})


def sendEmailNewAbsenceRequestForApproval(request, user, manager):
    emailSubject = 'Work Time manager - new absence request for approval!'
    emailBody = render_to_string('emails/absenceRequestSentMail.html', {
        'user': user,
        'manager': manager,
    })

    email = EmailMessage(subject=emailSubject, body=emailBody,
                         from_email=settings.EMAIL_FROM_USER, to=[manager.email])
    email.send()
