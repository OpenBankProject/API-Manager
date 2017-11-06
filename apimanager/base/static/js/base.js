$(document).ready(function($) {
	$('table.tablesorter').tablesorter();
	$('#authentication-select').change(function() {
		$('.authentication-method').hide();
		var method = $(this).val();
		$(`#authenticate-${method}`).show();
	});
});
