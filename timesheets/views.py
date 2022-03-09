import calendar
import datetime
import json
import locale

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from accounts.models import wtmUser
from config import settings
from .models import TimesheetDay, Timesheet

@login_required(login_url='home')
def timesheetsPersonalListView(request):
    timesheetsList = []
    month = datetime.date.today().month
    currentYear = datetime.date.today().year

    try:
        Timesheet.objects.get(timesheetOwner=request.user, monthNumber=month, year=currentYear)
    except Timesheet.DoesNotExist:
        timesheetsList.append({
            'timesheetYear': currentYear,
            'monthName': datetime.datetime.strptime(str(month), '%m').strftime("%B"),
            'monthNumber': month,
            'timesheetStatus': 'Not created',
        })

    userTimesheets = Timesheet.objects.filter(timesheetOwner=request.user).order_by('-monthNumber', '-year')

    for timesheet in userTimesheets:
        timesheetsList.append({
            'timesheetYear': timesheet.year,
            'monthName': datetime.datetime.strptime(str(timesheet.monthNumber), '%m').strftime("%B"),
            'monthNumber': timesheet.monthNumber,
            'timesheetStatus': timesheet.getTimesheetStatus(),
        })

    if request.POST:
        timesheetMonth = int(request.POST.get('timesheetMonth'))
        return HttpResponseRedirect(reverse('createTimesheet', args=(timesheetMonth,)))
    return render(request, 'timesheets/timesheetList.html', {'timesheetList': timesheetsList})

@login_required(login_url='home')
def timesheetPersonalView(request, timesheetMonth):
    dateObject = []
    timesheet = None
    currentYear = datetime.date.today().year
    timesheetMonthName = datetime.datetime.strptime(str(timesheetMonth), '%m').strftime("%B")

    try:
        timesheet = Timesheet.objects.get(timesheetOwner=request.user, month=timesheetMonthName, year=currentYear)
        dateObject = timesheet.getTimesheetObjectForTemplate()
    except Timesheet.DoesNotExist:
        teamManager = wtmUser.objects.get(user=request.user).team.manager
        timesheet = Timesheet.objects.create(timesheetOwner=request.user, managerToAccept=teamManager,
                                             month=timesheetMonthName, year=currentYear)

        days = getDayOfMonth(timesheetMonth, currentYear)
        for day in days:
            newDay = TimesheetDay.objects.create(owner=request.user, date=day.strftime("%Y-%m-%d"))
            timesheet.days.add(newDay)
            dateObject.append({
                'fullDate': day.strftime("%d %B, %Y").title(),
                'dayOfWeek': day.strftime("%A").title(),
                'startTime': "00:00",
                'endTime': "00:00",
                'breakTime': "00:00",
                'workTime': "00:00",
            })
    if request.POST.get('action') == 'saveTimesheet':
        fullDateList = []
        totalWorkMinutes = 0

        startTimeList = json.loads(request.POST.get('startTime'))
        endTimeList = json.loads(request.POST.get('endTime'))
        breakTimeList = json.loads(request.POST.get('breakTime'))
        workHoursList = calculateWorkHours(startTimeList, endTimeList, breakTimeList)

        for fullDate in json.loads(request.POST.get('fullDate')):
            print(fullDate)
            tempDate = convertTemplateDateToYYYYmmDD(fullDate)
            fullDateList.append(tempDate)
        for (date, startTime, endTime, breakTime, workTime) in zip(fullDateList, startTimeList, endTimeList,
                                                                   breakTimeList, workHoursList):
            totalWorkMinutes += convertTimeFieldToMinutes(workTime)
            workDay = TimesheetDay.objects.get(owner=request.user, date=date)
            if workDay.startTime.strftime("%H:%M") != startTime or workDay.endTime.strftime(
                    "%H:%M") != endTime or workDay.breakTime.strftime("%H:%M") != breakTime:
                workDay.startTime = startTime
                workDay.endTime = endTime
                workDay.breakTime = breakTime
                workDay.workTime = workTime
                workDay.save()

        timesheet.totalWorkMinutes = totalWorkMinutes
        timesheet.save()
        messages.info(request, "Timesheet saved successfully.")
        return JsonResponse({'result': "none", })
    if request.POST.get('action') == 'sendTimesheet':
        sendEmailNewTimesheetForApproval(request, timesheet.timesheetOwner, timesheet.managerToAccept)
        timesheet.sentToAccept = True
        timesheet.timesheetStatus = "SENTTOAPPROVE"
        timesheet.save()
    if request.POST.get('action') == 'autoCompleteTimesheet':
        totalWorkMinutes = 0
        tempWtmUser = wtmUser.objects.get(user=request.user)
        personalStartTime = tempWtmUser.personalStartTime
        personalEndTime = tempWtmUser.personalEndTime
        personalBreakTime = tempWtmUser.personalBreakTime
        for day in timesheet.days.all().order_by('date'):
            if not day.date.weekday() > 4:
                day.startTime = personalStartTime
                day.endTime = personalEndTime
                day.breakTime = personalBreakTime
                day.workTime = \
                    calculateWorkHours([personalStartTime.strftime("%H:%M")], [personalEndTime.strftime("%H:%M")],
                                       [personalBreakTime.strftime("%H:%M")])[0]
                totalWorkMinutes += int(day.workTime[:-3]) * 60 + int(day.workTime[-2:])
            else:
                day.startTime = "00:00"
                day.endTime = "00:00"
                day.breakTime = "00:00"
                day.workTime = "00:00"
            day.save()
        timesheet.totalWorkMinutes = totalWorkMinutes
        timesheet.save()
    totalTimeForContext = timesheet.getTimesheetTotalWorkMinutesForTemplate()
    if timesheet.timesheetStatus == 'SENTTOAPPROVE' or timesheet.timesheetStatus == 'APPROVED':
        timesheetNotEditable = True
    else:
        timesheetNotEditable = False
    return render(request, 'timesheets/editTimesheet.html',
                  {'date': dateObject,
                   'month': timesheetMonth,
                   'totalTime': totalTimeForContext,
                   'timesheetNotEditable': timesheetNotEditable,
                   'sendBackComment': timesheet.sendBackComment,
                   })

@login_required(login_url='home')
def timesheetsSentForApprovalListView(request):
    timesheets = Timesheet.objects.filter(managerToAccept=request.user, timesheetStatus='SENTTOAPPROVE')

    return render(request, 'timesheets/timesheetsToAccept.html', {'timesheets': timesheets})

@login_required(login_url='home')
def timesheetManagerView(request, pk):
    dateObject = []
    timesheet = Timesheet.objects.get(pk=pk)
    dateObject = timesheet.getTimesheetObjectForTemplate()
    totalTimeForContext = timesheet.getTimesheetTotalWorkMinutesForTemplate()
    if request.POST.get('action') == 'acceptTimesheet':
        timesheet = Timesheet.objects.get(pk=request.POST.get('timesheetPk'))
        timesheet.timesheetStatus = "APPROVED"
        timesheet.sendBackComment = ""
        timesheet.save()
        sendEmailTimesheetApproved(request, timesheet.timesheetOwner,
                                   datetime.datetime.strptime(str(timesheet.monthNumber), '%m').strftime("%B"),
                                   timesheet.year)
        messages.info(request, "Timesheet has been approved successfully.")
    if request.POST.get('action') == 'sendBackTimesheet':
        timesheet = Timesheet.objects.get(pk=request.POST.get('timesheetPk'))
        sendBackComment = request.POST.get('sendBackComment')
        timesheet.sendBackComment = sendBackComment
        timesheet.timesheetStatus = "SENTBACKFORCHANGE"
        timesheet.save()
        sendEmailTimesheetSentBack(request, timesheet.timesheetOwner,
                                   datetime.datetime.strptime(str(timesheet.monthNumber), '%m').strftime("%B"),
                                   timesheet.year, timesheet.sendBackComment)
    return render(request, 'timesheets/timesheetManager.html', {
        'timesheet': timesheet,
        'date': dateObject,
        'totalTime': totalTimeForContext, })


def getDayOfMonth(monthNumber, year):
    num_days = calendar.monthrange(year, monthNumber)[1]
    days = [datetime.date(datetime.date.today().year, monthNumber, day) for day in range(1, num_days + 1)]
    return days


def calculateWorkHours(startTimeList, endTimeList, breakTimeList):
    workHoursList = []
    for (startTime, endTime, breakTime) in zip(startTimeList, endTimeList, breakTimeList):
        startTimeMins = int(startTime[:-3]) * 60 + int(startTime[-2:])
        endTimeMins = int(endTime[:-3]) * 60 + int(endTime[-2:])
        breakTimeMins = int(breakTime[:-3]) * 60 + int(breakTime[-2:])
        workTime = endTimeMins - startTimeMins - breakTimeMins
        workTimeH = workTime / 60
        if workTimeH < 0:
            workTimeH = 24 + workTimeH
        workTimeM = workTime % 60
        workTime = str("%02d" % (workTimeH,)) + ':' + str("%02d" % (workTimeM,))
        workHoursList.append(workTime)
    return workHoursList


def convertTimeFieldToMinutes(time):
    workMinutes = int(time[:-3]) * 60 + int(time[-2:])

    return workMinutes


def convertTemplateDateToYYYYmmDD(templateDate):
    convertedDate = datetime.datetime.strptime(templateDate, "%d %B, %Y").strftime('%Y-%m-%d')
    return convertedDate


def sendEmailNewTimesheetForApproval(request, user, manager):
    emailSubject = 'Work Time manager - new timesheet for approval!'
    emailBody = render_to_string('emails/timesheetSentMail.html', {
        'user': user,
        'manager': manager,
    })

    email = EmailMessage(subject=emailSubject, body=emailBody, from_email=settings.EMAIL_FROM_USER, to=[manager.email])
    email.send()


def sendEmailTimesheetApproved(request, user, timesheetMonth, timesheetYear):
    emailSubject = 'Work Time manager - your timesheet has been approved!'
    emailBody = render_to_string('emails/timesheetApprovedMail.html', {
        'user': user,
        'timesheetMonth': timesheetMonth,
        'timesheetYear': timesheetYear
    })

    email = EmailMessage(subject=emailSubject, body=emailBody, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()


def sendEmailTimesheetSentBack(request, user, timesheetMonth, timesheetYear, timesheetComment):
    emailSubject = 'Work Time manager - your timesheet has been sent back for change!'
    emailBody = render_to_string('emails/timesheetSentBackMail.html', {
        'user': user,
        'timesheetMonth': timesheetMonth,
        'timesheetYear': timesheetYear,
        'timesheetComment': timesheetComment
    })

    email = EmailMessage(subject=emailSubject, body=emailBody, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.send()
