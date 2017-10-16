$('.need').on('click', function() {
    $('.need div').toggle();
});
$('.updated').on('click', function() {
    $('.updated div').toggle();
});
$('.finished').on('click', function() {
    $('.finished div').toggle();
});
$('.hibernating').on('click', function() {
    $('.hibernating div').toggle();
});
$('.frogged').on('click', function() {
    $('.frogged div').toggle();
});
$('div div').toggle();

var options = { responsive: true };

var ctx_donut = $("#donutChart").get(0).getContext("2d");

var ctx_donut2 = $("#donutChart2").get(0).getContext("2d");

var counts = {{dict|safe}};

var wips = {{wip|safe}};

var myDonutChart = new Chart(ctx_donut, {
                                        type: 'doughnut',
                                        data: counts,
                                        options: options
                                      });
$('#projectLegend').html(myDonutChart.generateLegend());
$('#project-chart').hide()

var stackedBar = new Chart(ctx_donut2, {
    type: 'horizontalBar',
    data: wips,
    options: {
        scales: {
            xAxes: [{
                stacked: true
            }],
            yAxes: [{
                stacked: true
            }]
        }
    }
});
$('#updateLegend').html(myDonutChart.generateLegend());