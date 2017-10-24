

var slider = document.getElementById("myRange");
var output = document.getElementById("loacation");
output.innerHTML = slider.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider.oninput = function() {
    output.innerHTML = this.value;
}

$('#updateproject select').change( function(evt){
    var currentStatus = $('#updateproject select').val();
    if (currentStatus == 2) {
       var message = "Congratulations for finishing a project! Be sure to set the finished date!";
       $('#flash').show();
       $('#flash').append(
          '<div class="alert alert-info">
            <h6>Congratulations for finishing a project! Be sure to set the finished date!</h6>
          </div>');
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

if($('#updateproject select').val() == 2) {
    $('#finished').show();
};