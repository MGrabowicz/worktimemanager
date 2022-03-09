$(document).ready(function() {

    document.getElementById("newAbsenceForm").addEventListener('submit', sendForm);
    document.getElementById("newAbsenceRequestButton").addEventListener('click', newAbsenceRequestButton);
    document.getElementById("pendingAbsenceRequestButton").addEventListener('click', pendingAbsenceRequestButtonFunction);
    document.getElementById("allAbsenceRequestButton").addEventListener('click', allAbsenceRequestButton);

    document.getElementById('startDateInput').valueAsDate = new Date();
    document.getElementById('endDateInput').valueAsDate = new Date();

    document.getElementsByClassName('pendingAbsenceRequestContainer')[0].style.display = 'none';
    document.getElementsByClassName('allAbsenceRequestContainer')[0].style.display = 'none';

    function newAbsenceRequestButton() {
        document.getElementsByClassName('absenceRequestContainer')[0].style.display = 'flex';
        document.getElementsByClassName('pendingAbsenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('allAbsenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('newAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-bright)';
        document.getElementsByClassName('pendingAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
        document.getElementsByClassName('allAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
    }

    function pendingAbsenceRequestButtonFunction() {
        document.getElementsByClassName('pendingAbsenceRequestContainer')[0].style.display = 'flex';
        document.getElementsByClassName('absenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('allAbsenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('pendingAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-bright)';
        document.getElementsByClassName('newAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
        document.getElementsByClassName('allAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
    }

    function allAbsenceRequestButton() {
        document.getElementsByClassName('allAbsenceRequestContainer')[0].style.display = 'flex';
        document.getElementsByClassName('absenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('pendingAbsenceRequestContainer')[0].style.display = 'none';
        document.getElementsByClassName('allAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-bright)';
        document.getElementsByClassName('newAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
        document.getElementsByClassName('pendingAbsenceRequestButton')[0].style.backgroundColor = 'var(--grey-middle)';
    }

    function sendForm(event) {
        event.preventDefault();
        var absenceTypeValue = document.getElementsByClassName("absenceTypeValue")[0].value;
        var startDateInput = document.getElementsByClassName("startDateInput")[0].value;
        var endDateInput = document.getElementsByClassName("endDateInput")[0].value;
        $.ajax({
            url: '/absences/createAbsence',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrftoken,
                action: 'sendAbsenceRequest',
                absenceType: absenceTypeValue,
                startDate: startDateInput,
                endDate: endDateInput,
            },
            success: function(json) {
                document.getElementById('startDateInput').valueAsDate = new Date();
                document.getElementById('endDateInput').valueAsDate = new Date();

                var div = '<div class="messageContainer" id="messageContainer">' + json['djangoMessage'] + '</div>';
                document.getElementById("messagesContainer").innerHTML = div;

                $('.absenceRequestsTable > tbody > tr:first').after('<tr><td><p class="absenceRequestOwner">' + json['userName'] + '</p></td>\
                <td><p class="absenceRequestStartDate">' + json['startDate'] + '</p></td>\
                <td><p class="absenceRequestEndDate">' + json['endDate'] + '</p></td>\
                <td><p class="absenceRequestWorkDays">' + json['workDays'] + '</p></td>\
                <td><p class="absenceRequestType"></p>' + json['absenceType'] + '</td></tr>');

                $('.allAbsenceRequestsTable > tbody > tr:first').after('<tr><td><p class="absenceRequestOwner">' + json['userName'] + '</p></td>\
                <td><p class="absenceRequestStartDate">' + json['startDate'] + '</p></td>\
                <td><p class="absenceRequestEndDate">' + json['endDate'] + '</p></td>\
                <td><p class="absenceRequestWorkDays">' + json['workDays'] + '</p></td>\
                <td><p class="absenceRequestType"></p>' + json['absenceType'] + '</td>\
                <td><p class="absenceRequestType"></p>Sent to approve</td></tr>');
            },
        })
    }
});