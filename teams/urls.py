from django.urls import path

from teams.views import createTeamView, listTeamsView, teamDetailView, addTeamMemberView

urlpatterns = [
    path('createTeam', createTeamView, name='createTeam'),
    path('listTeams', listTeamsView, name='listTeams'),
    path('detailTeam/<int:pk>', teamDetailView, name='detailTeam'),
    path('addTeamMember/<int:pk>', addTeamMemberView, name='addTeamMember'),
]
