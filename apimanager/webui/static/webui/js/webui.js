$(document).ready(function($) {
	function syntaxHighlight(json) {
		if (typeof json != 'string') {
			 json = JSON.stringify(json, undefined, 2);
		}
		json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
		return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
			var cls = 'number';
			if (/^"/.test(match)) {
				if (/:$/.test(match)) {
					cls = 'key';
				} else {
					cls = 'string';
				}
			} else if (/true|false/.test(match)) {
				cls = 'boolean';
			} else if (/null/.test(match)) {
				cls = 'null';
			}
			return '<span class="' + cls + '">' + match + '</span>';
		});
	}

	$('#config-json').html((syntaxHighlight(ConfigJson)));

	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		method = $(runner).find('#id_webui_props_key').innerHTML;
		value = $(runner).find('textarea[name="webui_props_value"]').val();

		$.post('/webui/save/method', {
			'method': method,
			'value': value,
			'csrfmiddlewaretoken': window.CSRF
		}, function (response) {
			t.next().show().fadeOut(1000);
		});
	});
});
