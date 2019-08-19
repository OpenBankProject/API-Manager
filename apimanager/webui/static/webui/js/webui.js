$(document).ready(function($) {
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		webui_props_name = $(runner).find('.webui_props_name').text();
		webui_props_value = $(runner).find('.webui_props_value').val();

		$.post('/webui/save/method', {
			'webui_props_name': webui_props_name,
			'webui_props_value': webui_props_value
		}, function (response) {
			t.next().show().fadeOut(1000);
		});
	});

	$('.runner button.forDelete').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		web_ui_props_id = $(runner).find('.web_ui_props_id').val();

		$.post('/webui/delete/method', {
			'web_ui_props_id': web_ui_props_id
		}, function (response) {
			t.next().show().fadeOut(1000);
		});
	});
});
