$(document).ready(function($) {
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		webui_props_name = $(runner).find('.webui_props_name').text();
		webui_props_value = $(runner).find('.webui_props_value').val();

		$.post('/webui/save/method', {
			'webui_props_name': webui_props_name,
			'webui_props_value': webui_props_value,
			'csrfmiddlewaretoken': window.CSRF
		}, function (response) {
			t.next().show().fadeOut(1000);
		});
	});
});
