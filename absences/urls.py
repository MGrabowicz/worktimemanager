from django.urls import path

from absences.views import createAbsenceView, absenceRequestsSentForApprovalListView

urlpatterns = [
    path('createAbsence', createAbsenceView, name='createAbsence'),
    path('absenceRequestsManagerList', absenceRequestsSentForApprovalListView, name='absenceRequestsManagerList'),
]