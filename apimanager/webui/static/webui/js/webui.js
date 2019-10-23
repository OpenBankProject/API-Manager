$(document).ready(function($) {
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		webui_props_name = $(runner).find('.webui_props_name').text();
		webui_props_value = $(runner).find('.webui_props_value').val();

		$.ajax({
          type: 'POST',
          url: '/webui/save/method',
          data: {
                'webui_props_name': webui_props_name,
                'webui_props_value': webui_props_value,
                'csrfmiddlewaretoken': window.CSRF
            },
          success: function (response) {
              alert('Saved');
              t.next().show().fadeOut(1000);
        },
          async:false
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
