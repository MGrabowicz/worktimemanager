from django.urls import path

from timesheets.views import timesheetPersonalView, timesheetsPersonalListView, timesheetsSentForApprovalListView, timesheetManagerView

urlpatterns = [
    path('createTimesheet', timesheetsPersonalListView, name='createTimesheet'),
    path('createTimesheet/<int:timesheetMonth>', timesheetPersonalView, name='createTimesheet'),
    path('timesheetsManagerList', timesheetsSentForApprovalListView, name='timesheetsManagerList'),
    path('timesheetsManager/<int:pk>', timesheetManagerView, name='timesheetsManager'),
]
