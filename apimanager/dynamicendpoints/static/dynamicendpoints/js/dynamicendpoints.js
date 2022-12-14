$(document).ready(function($) {
	const schema = {};
	const options = {
		mode: 'code',
		modes: ['code', 'text', 'tree', 'preview']
	};
	
	//each dynamic_endpoint will have each own json_editor, and will put data into it when click `parameter` box
	//and will use the data from click `save` button.
	var json_editors = []
	$('.parameters').click(function() {
		var runner = $(this).parent().parent().parent();
		var json_editor_id= $(runner).find('.jsoneditor_div')[0].id;
		var json_editor_number = json_editor_id.replace("jsoneditor","");
		var container = $("#"+json_editor_id);
		var parameters = JSON.parse($(runner).find('textarea[name="parameters"]').text());
		var jsoneditor_div =  $(runner).find('.jsoneditor_div');
		//make sure only create one jsoneditor_div block 
		if(!(jsoneditor_div.css("display") ==="block")){
			json_editors[json_editor_number] = new JSONEditor(container[0], options, parameters);
			$(runner).find('textarea[name="parameters"]').prop( "disabled", true );
			jsoneditor_div.css("display","block");
		}else{
			json_editors[json_editor_number] = json_editors[json_editor_number].set(parameters)
			$(runner).find('textarea[name="parameters"]').prop( "disabled", true );
		}
	});
	
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		var jsoneditor_id= $(runner).find('.jsoneditor_div')[0].id
		var json_editor_number = jsoneditor_id.replace("jsoneditor","")
		var parameters_Json_editor = JSON.stringify(json_editors[json_editor_number].get());
		console.log("parameters_Json_editor:"+parameters_Json_editor)
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('dynamicendpoints/save/dynamicendpoint', {
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
		var dynamic_endpoint_id = $(runner).find('.dynamic_endpoint_id').text();
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('dynamicendpoints/delete/dynamicendpoint', {
			'dynamic_endpoint_id': dynamic_endpoint_id
		}, function (response) {
			location.reload();
		});
		return false;
	});
});
