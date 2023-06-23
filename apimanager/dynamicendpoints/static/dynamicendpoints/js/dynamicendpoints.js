$(document).ready(function($) {
	const schema = {};
	const options = {
		mode: 'code',
		modes: ['code', 'text', 'tree', 'preview']
	};
	
	//each dynamic_endpoint will have each own json_editor, and will put data into it when click `parameter` box
	//and will use the data from click `save` button.
	let json_editors = []
	$('.parameters').click(function() {
		let runner = $(this).parent().parent().parent();
		let json_editor_id= $(runner).find('.jsoneditor_div')[0].id;
		let json_editor_number = json_editor_id.replace("jsoneditor","");
		let container = $("#"+json_editor_id);
		let parameters = JSON.parse($(runner).find('textarea[name="parameters"]').text());
		let jsoneditor_div =  $(runner).find('.jsoneditor_div');
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
		let runner = $(this).parent().parent().parent();
		let jsoneditor_id= $(runner).find('.jsoneditor_div')[0].id
		let json_editor_number = jsoneditor_id.replace("jsoneditor","")
		let parameters_Json_editor = JSON.stringify(json_editors[json_editor_number].get());
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
	    e.preventDefault();
		let runner = $(this).parent().parent().parent();
		let dynamic_endpoint_id = $(runner).find('.dynamic_endpoint_id').attr("value");
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
