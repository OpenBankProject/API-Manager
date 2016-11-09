$(document).ready(function($) {
	var ctx = $("#call-graph");
	var randomColor = function(alpha) {
	};
	var backgroundColors = [];
	var borderColors = [];
 	$.each(CALLS_VALUES, function(idx, val) {
		var red = Math.floor((Math.random() * 255) + 1); 
		var green = Math.floor((Math.random() * 255) + 1); 
		var blue = Math.floor((Math.random() * 255) + 1); 
		var backgroundColor = 'rgba(' + red + ', ' + green + ', ' + blue + ', 0.2)';
		backgroundColors.push(backgroundColor);
		var borderColor = 'rgba(' + red + ', ' + green + ', ' + blue + ', 1)';
		borderColors.push(borderColor);
	});
	var myChart = new Chart(ctx, {
    	type: 'bar',
		maintainAspectRation: false,
		data: {
			labels: CALLS_LABELS,
			datasets: [{
				data: CALLS_VALUES,
				backgroundColor: backgroundColors,
				borderColor: borderColors,
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true,
						fixedStepSize: 1
					}
				}]
			},
			legend: {
				display: false
			}
		}
	});
});
