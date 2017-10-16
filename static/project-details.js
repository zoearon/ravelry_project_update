// set the status intially to the current status
$("#updateproject select option").each( function() {
    if ($(this).val() == {{project.status_id|tojson}}) {
        $(this).attr('selected', true);
    } 
});

var slider = document.getElementById("myRange");
var output = document.getElementById("loacation");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}

if($('#updateproject select').val() == 2) {
    $('#finished').show();
};
$('#updateproject select').change( function(evt){
    var currentStatus = $('#updateproject select').val();
    if (currentStatus == 2) {
       var message = "Congratulations for finishing a project! Be sure to set the finished date!";
       $('#flash').show();
       $('#flash h3').html(message);
       $('#flash').fadeOut(3000);

       $('#finished').show(); 
   }
   else {
   $('#finished').hide();
   $("#flash h3").empty();
    }
});

$('.update button').on('click', function() {
    $('#updateproject').toggle();
});