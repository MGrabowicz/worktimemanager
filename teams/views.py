from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse

from accounts.models import wtmUser
from teams.forms import CreateTeamForm
from teams.models import Team


def createTeamView(request):
    managerCandidates = User.objects.filter(wtmuser__promotedToManager=True)
    teamCandidates = User.objects.filter(wtmuser__team=None)
    if request.POST:
        createTeamForm = CreateTeamForm(data=request.POST, managerCandidates=managerCandidates,
                                        teamCandidates=teamCandidates)
        if createTeamForm.is_valid():
            newTeam = createTeamForm.save()
            for user in newTeam.users.all():
                tempUser = wtmUser.objects.get(user=user)
                tempUser.team = newTeam
                tempUser.save()
            return HttpResponseRedirect(reverse('detailTeam', args=(newTeam.pk,)))
        else:
            print(createTeamForm.errors)
    else:
        createTeamForm = CreateTeamForm(managerCandidates=managerCandidates, teamCandidates=teamCandidates)
    return render(request, 'teams/createTeam.html', {'groupForm': createTeamForm})


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
