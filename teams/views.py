from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse
from django.http import JsonResponse
import json
from accounts.models import wtmUser
from teams.models import Team


def createTeamView(request):
    managerCandidates = User.objects.filter(wtmuser__promotedToManager=True)
    teamCandidates = User.objects.filter(wtmuser__team=None)
    if request.POST:
        if request.POST.get("action") == "createTeamRequest":
            teamName = request.POST.get("teamName")
            managerSelect = json.loads(request.POST.get("managerSelect"))
            userSelect = json.loads(request.POST.get("userSelect"))
            manager = User.objects.get(pk=managerSelect)
            users = User.objects.filter(pk__in=userSelect)
            createdTeam = Team.objects.create(name=teamName, manager=manager)
            createdTeam.users.set(users)
            for user in createdTeam.users.all():
                tempUser = wtmUser.objects.get(user=user)
                tempUser.team = createdTeam
                tempUser.save()
                return JsonResponse({'createdTeamId': createdTeam.pk,})
    return render(request, 'teams/createTeam.html', {
        'managerCandidates': managerCandidates,
        'teamCandidates': teamCandidates})


def listTeamsView(request):
    teamList = Team.objects.all().order_by('-name')
    return render(request, 'teams/listTeams.html', {'teamList': teamList})


def addTeamMemberView(request, pk):
    team = Team.objects.get(pk=pk)
    teamCandidates = User.objects.filter(wtmuser__team=None)
    if request.POST:
        usersIds = request.POST.getlist('teamMembers')
        print(usersIds)
        for userId in usersIds:
            addedUser = User.objects.get(pk=userId)
            team.users.add(addedUser)
            tempUser = wtmUser.objects.get(user=addedUser)
            tempUser.team = team
            tempUser.save()
        messages.info(request, "Added new users successfully.")
        return HttpResponseRedirect(reverse('detailTeam', args=(pk,)))
    return render(request, 'teams/addTeamMember.html', {'teamCandidates': teamCandidates})


def teamDetailView(request, pk):
    team = Team.objects.get(pk=pk)
    if request.POST:
        usersIds = request.POST.getlist('teamMembers')
        for userId in usersIds:
            deletedUser = User.objects.get(pk=userId)
            team.users.remove(deletedUser)
            tempUser = wtmUser.objects.get(user=deletedUser)
            tempUser.team = None
            tempUser.save()
        messages.info(request, "Deleted users successfully.")
    return render(request, 'teams/detailTeam.html', {'team': team})
