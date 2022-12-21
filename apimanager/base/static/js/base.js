$(document).ready(function($) {
	$('table.tablesorter').tablesorter();
	$('#authentication-select').change(function() {
		$('.authentication-method').hide();
		let method = $(this).val();
		$(`#authenticate-${method}`).show();
	});
});
