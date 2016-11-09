$(document).ready(function($) {
	$('#consumer-detail').hide();
	$('.consumers .consumer-row td.select').click(function() {
		$('.consumers .consumer-row').removeClass('active');
		var tr = $(this).parent();
		tr.addClass('active');
		var consumer_id = tr.data('consumer-id');
		$.each(CONSUMERS, function (idx, consumer) {
			if (consumer['id'] == consumer_id) {
				$('#consumer-detail-id').val(consumer['id']);
				$('#consumer-detail-name').html(consumer['name']);
				$('#consumer-detail-developerEmail').html(consumer['developerEmail']);
				$('#consumer-detail-created').html(consumer['created']);
				$('#consumer-detail-description').html(consumer['description']);
				var isactive = $('#consumer-detail-isactive');
				var enableButton = $('#consumer-detail-enable');
				enableButton.removeClass('btn-green').removeClass('btn-red');
				if (consumer['enabled']) {
					enableButton.addClass('btn-red');
					enableButton.html('Disable');
					enableButton.attr('href',
						CONSUMERS_DISABLE.replace('0', consumer['id']));
					isactive.prop('checked', true);
				} else {
					enableButton.addClass('btn-green');
					enableButton.html('Enable');
					enableButton.attr('href',
						CONSUMERS_ENABLE.replace('0', consumer['id']));
					isactive.prop('checked', false);
				}
				$('#consumer-detail').modal('show');
			}
		});
	});
});
