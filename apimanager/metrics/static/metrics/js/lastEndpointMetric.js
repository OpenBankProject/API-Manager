$(document).ready(function($) {
	getMetricLastEndpoint();
});

function getMetricLastEndpoint(){
	$.ajax({url: "/metrics/api/last-endpoint", success: function(result){
			var content = ""
				+result['implemented_by_partial_function']+" took "
				+result['duration']+"ms at "
				+result['date']+" "
				+result['verb']+" "
				+ result['url']
				
				+" ms.";
			$("#last_endpoint").text(content);
			setTimeout(function(){getMetricLastEndpoint();}, 5000); // will call function to update time every 5 seconds
		}});
}
