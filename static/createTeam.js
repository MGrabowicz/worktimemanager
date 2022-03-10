$(document).ready(function() {
    document.getElementById("createTeamForm").addEventListener('submit', sendForm);

    function sendForm(event) {
        event.preventDefault();
        var teamName = document.getElementsByClassName("teamName")[0].value;
        var managerSelect = $('.managerSelect').val();
        var userSelect = $('.userSelect').val();
        $.ajax({
            url: '/teams/createTeam',
            type: 'post',
            data: {
                csrfmiddlewaretoken: csrftoken,
                action: 'createTeamRequest',
                teamName: teamName,
                managerSelect: managerSelect,
                userSelect: JSON.stringify(userSelect),
            },
            success: function(json) {
                location.href = "/teams/detailTeam/" + json["createdTeamId"];
            },
        })
    }
});