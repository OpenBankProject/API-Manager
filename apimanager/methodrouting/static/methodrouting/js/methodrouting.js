$(document).ready(function($) {
	$('.runner button.forSave').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		method_routing_id = $(runner).find('.method_routing_id').text();
		method_name = $(runner).find('.method_name').text();
		connector_name = $(runner).find('.connector_name').val();
		bank_id_pattern = $(runner).find('textarea[name="bank_id_pattern"]').val();
		is_bank_id_exact_match = $(runner).find('.is_bank_id_exact_match').val();
		parameters = $(runner).find('textarea[name="parameters"]').val();

		$.post('methodrouting/save/method', {
			'method_routing_id': method_routing_id,
			'method_name': method_name,
			'connector_name': connector_name,
			'bank_id_pattern': bank_id_pattern,
			'is_bank_id_exact_match': is_bank_id_exact_match,
			'parameters': parameters
		}, function (response) {
			t.next().show().fadeOut(1000);
		});
	});

	$('.runner button.forDelete').click(function() {
		var t = $(this);
		var runner = $(this).parent().parent().parent();
		method_routing_id = $(runner).find('.method_routing_id').text();
		$.post('methodrouting/delete/method', {
			'method_routing_id': method_routing_id
		}, function (response) {
			t.parent().parent().parent().remove();
		});
	});
});
