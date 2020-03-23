$(document).ready(function($) {
	const schema = {};
	var json = [
		{
			key: 'url',
			value: 'http://localhost:8080'
		},
		{
			"key":"outBoundMapping",
			"value":{
				"cc":{
					"cId":"outboundAdapterCallContext.correlationId"
				},
				"bankId":"bankId.value + 'helloworld'",
				"originalJson":"$root"
			}
		},
		{
			"key":"inBoundMapping",
			"value":{
				"inboundAdapterCallContext$default":{
					"correlationId":"correlation_id_value",
					"sessionId":"session_id_value"
				},
				"status$default":{
					"errorCode":"",
					"backendMessages":[]
				},
				"data":{
					"bankId":{
						"value":"result.bank_id"
					},
					"shortName":"result.name",
					"fullName":"'full: ' + result.name",
					"logoUrl":"result.logo",
					"websiteUrl":"result.website",
					"bankRoutingScheme[0]":"result.routing.routing_scheme",
					"bankRoutingAddress[0]":"result.routing.routing_address",
					"swiftBic":"result.swift_bic",
					"nationalIdentifier":"result.national"
				}
			}
		}];

	const options = {
		mode: 'code',
		modes: ['code', 'text', 'tree', 'preview']
	};
	
	var jsoneditorNumber = $('.jsoneditor_div').length
	for (var step = 0; step < jsoneditorNumber; step++) {
		var container = $("#"+"jsoneditor"+step);
		new JSONEditor(container[0], options, json);
	}
	
// // get json
// const updatedJson = editor.get()

	$('.parameters').click(function() {
		var row = $(this).parent().parent();
		row.find('.jsoneditor_div').css("display","block");
	});
	
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		method_routing_id = $(runner).find('.method_routing_id').text();
		method_name = $(runner).find('.method_name').text();
		connector_name = $(runner).find('.connector_name').val();
		bank_id_pattern = $(runner).find('textarea[name="bank_id_pattern"]').val();
		is_bank_id_exact_match = $(runner).find('.is_bank_id_exact_match').val();
		parameters = $(runner).find('textarea[name="parameters"]').val();
		parameters_Json_editor = JSON.stringify(editor.get());
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('methodrouting/save/method', {
			'method_routing_id': method_routing_id,
			'method_name': method_name,
			'connector_name': connector_name,
			'bank_id_pattern': bank_id_pattern,
			'is_bank_id_exact_match': is_bank_id_exact_match,
			'parameters': parameters,
			'parameters_Json_editor': parameters_Json_editor,
		}, function (response) {
			location.reload(); 
		});
		runner.find('jsoneditor_div').css("display","none");
		return false;
	});

	$('.runner button.forDelete').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		method_routing_id = $(runner).find('.method_routing_id').text();
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");		
		$.post('methodrouting/delete/method', {
			'method_routing_id': method_routing_id
		}, function (response) {
			location.reload();
		});
		return false;
	});
});
