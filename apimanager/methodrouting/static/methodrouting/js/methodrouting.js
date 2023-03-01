$(document).ready(function($) {
	const schema = {};
	const options = {
		mode: 'code',
		modes: ['code', 'text', 'tree', 'preview']
	};
	
	//each method_routing will have each own json_editor, and will put data into it when click `parameter` box
	//and will use the data from click `save` button.
	let json_editors = []
	$('.parameters').click(function() {
		let runner = $(this).parent().parent().parent();
		let json_editor_id= $(runner).find('.jsoneditor_div')[0].id;
		let json_editor_number = json_editor_id.replace("jsoneditor","");
		let container = $("#"+json_editor_id);
		let parameters = JSON.parse($(runner).find('textarea[name="parameters"]').text());
		let jsoneditor_div =  $(runner).find('.jsoneditor_div');
		//make sure only create one jsoneditor_div block, click once to open and then close the block.
		if (typeof json_editors[json_editor_number] === 'undefined') {
			json_editors[json_editor_number] = new JSONEditor(container[0], options, parameters);
			jsoneditor_div.css("display","block");
		}else{
			// json_editors[json_editor_number] = json_editors[json_editor_number].set(parameters)
			if(jsoneditor_div.css("display") ==="block"){
				jsoneditor_div.css("display","none");
			}else{
				jsoneditor_div.css("display","block");
			}
		}
	});
	
	$('.runner button.forSave').click(function() {
		let runner = $(this).parent().parent().parent();
		let method_routing_id = $(runner).find('.method_routing_id').text();
		let method_name = $(runner).find('.method_name').text();
		let connector_name = $(runner).find('.connector_name').val();
		let bank_id_pattern = $(runner).find('textarea[name="bank_id_pattern"]').val();
		let is_bank_id_exact_match = $(runner).find('.is_bank_id_exact_match').val();
		let parameters = $(runner).find('textarea[name="parameters"]').val();
		let jsoneditor_id= $(runner).find('.jsoneditor_div')[0].id;
		let json_editor_number = jsoneditor_id.replace("jsoneditor","");
		//if the user do not click the `parameters` box, then there is no json_editors here,so we use the parameters directly.
		if (typeof json_editors[json_editor_number] === 'undefined') {
			let parameters_Json_editor = parameters;
		} else {
			let parameters_Json_editor = JSON.stringify(json_editors[json_editor_number].get());
		}
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('methodrouting/save/method', {
			'method_routing_id': method_routing_id,
			'method_name': method_name,
			'connector_name': connector_name,
			'bank_id_pattern': bank_id_pattern,
			'is_bank_id_exact_match': is_bank_id_exact_match,
			'parameters_Json_editor': parameters_Json_editor,
		}, function (response) {
			location.reload(); 
		});
		runner.find('jsoneditor_div').css("display","none");
		return false;
	});

	$('.runner button.forDelete').click(function() {
		let runner = $(this).parent().parent().parent();
		let method_routing_id = $(runner).find('.method_routing_id').text();
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
