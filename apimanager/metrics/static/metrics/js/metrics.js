$(document).ready(function($) {
	var barChart = new Chart($("#barchart"), {
		type: 'horizontalBar',
		data: {
			labels: BarchartData['labels'],
			datasets: [{
				label: 'Count',
				data: BarchartData['data'],
				backgroundColor: BarchartData['backgroundColor'],
				borderColor: BarchartData['borderColor'],
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				xAxes: [{
					ticks: {
						beginAtZero: true
					}
				}]
			},
			legend: {
				display: false
			}
		}
	});
});
