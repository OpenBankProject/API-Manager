$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var web_ui_props_name = $(runner).find('.web_ui_props_name').text();
        var web_ui_props_value = $(runner).find('.web_ui_props_value').val();
    
        var webui = $('#webui');
        if(web_ui_props_value.trim() === '') {
            $('<div class="alert alert-dismissible alert-danger dynamic-message" role="alert">\n' +
                '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>\n' +
                'Web UI Props Value should not be empty!' +
                '</div>'
            ).insertBefore(webui);
            return;
        }
		/*
        t.attr("disabled","disabled").toggleClass("disabled");
        t.next().attr("disabled","disabled").toggleClass("disabled");
        $.ajax({
            type: 'POST',
            url: '/webui/save/method',
            data: {
                'web_ui_props_name': web_ui_props_name,
                'web_ui_props_value': web_ui_props_value,
                'csrfmiddlewaretoken': window.CSRF
            },
            success: function (response) {
                t.removeAttr("disabled").toggleClass("disabled");
                t.next().removeAttr("disabled").toggleClass("disabled");
                $(runner).find('.web_ui_props_id').val(response['web_ui_props_id']);
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
		*/
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('/webui/save/method', {
			'web_ui_props_name': web_ui_props_name,
            'web_ui_props_value': web_ui_props_value,
		}, function (response) {
			location.reload(); 
		});
    });

    $('.runner button.forDelete').click(function(e) {
		e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var web_ui_props_name = $(runner).find('.web_ui_props_name').text();
        var textArea = runner.find('.web_ui_props_value');
        var props_id = $(runner).find('.web_ui_props_id');
        var web_ui_props_id = props_id.val();
        var webui = $('#webui');
		/*
        t.attr("disabled","disabled").toggleClass("disabled");
        t.next().attr("disabled","disabled").toggleClass("disabled");
			
        $.ajax({
            type: 'POST',
            url: '/webui/delete/method',
            data: {'web_ui_props_id': web_ui_props_id,
                'web_ui_props_name': web_ui_props_name,
                'csrfmiddlewaretoken': window.CSRF
            },
            success: function (response) {
                t.removeAttr("disabled").toggleClass("disabled");
                t.next().removeAttr("disabled").toggleClass("disabled");
                textArea.val(response['default_value']);
                props_id.val('default');
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
		*/
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('/webui/delete/method', {
			'web_ui_props_id': web_ui_props_id
		}, function (response) {
			location.reload();
		});
    });
});
