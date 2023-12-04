$(document).ready(function($) {
	getMetricLastEndpoint();
});

function getMetricLastEndpoint(){
	$.ajax({url: "/metrics/api/last-endpoint", success: function(result){
			var content = "Last call: "
				+result['app_name']+" "
				+result['verb']+" "
				+ result['implemented_by_partial_function']
				+" costed "
				+result['duration']
				+" ms.";
			$("#last_endpoint").text(content);
			setTimeout(function(){getMetricLastEndpoint();}, 5000); // will call function to update time every 5 seconds
		}});
}
