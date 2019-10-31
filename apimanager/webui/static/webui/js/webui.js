$(document).ready(function($) {
	$('.runner button.forSave').click(function(e) {
		e.preventDefault();
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		var webui_props_name = $(runner).find('.webui_props_name').text();
		var webui_props_value = $(runner).find('.webui_props_value').val();
		$('.dynamic-message').each(function(i, d_msg){
			$(d_msg).remove();
		});
		var webui = $('#webui');
		if(webui_props_value.trim() === '') {
			$('<div class="alert alert-dismissible alert-danger dynamic-message" role="alert">\n' +
				'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n' +
				'Web UI Props Value should not be empty!' +
				'</div>'
			).insertBefore(webui);
			return;
		}
		t.attr("disabled","disabled").toggleClass("disabled");
		t.next().attr("disabled","disabled").toggleClass("disabled");
		$.ajax({
			type: 'POST',
			url: '/webui/save/method',
			data: {
				'webui_props_name': webui_props_name,
				'webui_props_value': webui_props_value,
				'csrfmiddlewaretoken': window.CSRF
			},
			success: function () {
				t.removeAttr("disabled").toggleClass("disabled");
				t.next().removeAttr("disabled").toggleClass("disabled");
				$('<div class="alert alert-dismissible alert-success dynamic-message" role="alert">\n' +
					'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Success!</div>'
				).insertBefore(webui);
			},
			error: function (response) {
				var errors = response.responseJSON ? response.responseJSON['errors'] : [response.responseText];
				errors.forEach(function(e){
					$('<div class="alert alert-dismissible alert-danger dynamic-message" role="alert">\n' +
						'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n' +
						e +
						'</div>'
					).insertBefore(webui);
				});
				t.removeAttr("disabled").toggleClass("disabled");
				t.next().removeAttr("disabled").toggleClass("disabled")
			}
        });
	});

	$('.runner button.forDelete').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		var web_ui_props_id = $(runner).find('.web_ui_props_id').val();
		$('.dynamic-message').each(function(i, d_msg){
			$(d_msg).remove();
		});
		var webui = $('#webui');
		t.attr("disabled","disabled").toggleClass("disabled");
		t.next().attr("disabled","disabled").toggleClass("disabled");

		$.ajax({
			type: 'POST',
			url: '/webui/delete/method',
			data: {'web_ui_props_id': web_ui_props_id },
			success: function () {
				t.removeAttr("disabled").toggleClass("disabled");
				t.next().removeAttr("disabled").toggleClass("disabled");
				$('<div class="alert alert-dismissible alert-success dynamic-message" role="alert">\n' +
					'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Success!</div>'
				).insertBefore(webui);
			},
			error: function (response) {
				var errors = response.responseJSON ? response.responseJSON['errors'] : [response.responseText];
				errors.forEach(function(e){
					$('<div class="alert alert-dismissible alert-danger dynamic-message" role="alert">\n' +
						'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n' +
						e +
						'</div>'
					).insertBefore(webui);
				});
				t.removeAttr("disabled").toggleClass("disabled");
				t.next().removeAttr("disabled").toggleClass("disabled")
			}
		});
	});
});
