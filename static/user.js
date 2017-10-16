$('button.update').on('click', function() {
    $('.update').toggle();
});

function submitUserUpdate(evt) {
    evt.preventDefault();

    var phone = $("#phone-field").val();
    var frequency = $("#frequency-field").val();
    var subscribed = $("#subscribe-field").val();
    var formInputs = {
            "phone": phone,
            "frequency": frequency,
            "subscribed": subscribed,
    };
    if (phone.length == 10) {
        $.post('/user/update', 
               formInputs,
               success);
    }
}
function success(result) {
    alert(result);
}

$('#updateuser').on('submit', submitUserUpdate);

function syncProjects(username) {
    var user = {"user": username};
    console.log(user);
    $.get('/sync', user, success);
}