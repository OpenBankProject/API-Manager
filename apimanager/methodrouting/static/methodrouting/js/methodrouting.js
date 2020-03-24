$(document).ready(function($) {
	const schema = {};
	const options = {
		mode: 'code',
		modes: ['code', 'text', 'tree', 'preview']
	};
	
	//each method_routing will have each own json_editor, and will put data into it when click `parameter` box
	//and will use the data from click `save` button.
	var json_editors = []
	$('.parameters').click(function() {
		var runner = $(this).parent().parent().parent();
		var json_editor_id= $(runner).find('.jsoneditor_div')[0].id;
		var json_editor_number = json_editor_id.replace("jsoneditor","");
		var container = $("#"+json_editor_id);
		parameters = JSON.parse($(runner).find('textarea[name="parameters"]').text());
		var jsoneditor_div =  $(runner).find('.jsoneditor_div');
		//make sure only create one jsoneditor_div block 
		if(!(jsoneditor_div.css("display") ==="block")){
			json_editors[json_editor_number] = new JSONEditor(container[0], options, parameters);
			jsoneditor_div.css("display","block");
		}else{
			json_editors[json_editor_number] = json_editors[json_editor_number].set(parameters)
		}
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
		var jsoneditor_id= $(runner).find('.jsoneditor_div')[0].id
		var json_editor_number = jsoneditor_id.replace("jsoneditor","")
		parameters_Json_editor = JSON.stringify(json_editors[json_editor_number].get());
		console.log("parameters_Json_editor:"+parameters_Json_editor)
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('methodrouting/save/method', {
			'method_routing_id': method_routing_id,
			'method_name': method_name,
			'connector_name': connector_name,
			'bank_id_pattern': bank_id_pattern,
			'is_bank_id_exact_match': is_bank_id_exact_match,
			'parameters': parameters_Json_editor,
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
