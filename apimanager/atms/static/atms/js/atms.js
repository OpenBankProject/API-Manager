$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        let runner = $(this).parent().parent().parent();
        let name = $(runner).find('.atm_attribute_name').val();
        let type = $(runner).find('.atm_attribute_type').val();
        let value = $(runner).find('.atm_attribute_value').val();
        $('.runner button.forUpdate').attr("disabled","disabled");
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('save/attribute', {
			'name': name,
			'type': type,
			'value': value,
		}, function (response) {
			location.reload();
		});
    });
    $('.runner button.forUpdate').click(function(e) {
            e.preventDefault();
            let runner = $(this).parent().parent().parent();
            let name = $(runner).find('.atm_attribute_name').val();
            let type = $(runner).find('.atm_attribute_type').val();
            let value = $(runner).find('.atm_attribute_value').val();
            $('.runner button.forUpdate').attr("disabled","disabled");
    		$('.runner button.forSave').attr("disabled","disabled");
    		$('.runner button.forDelete').attr("disabled","disabled");
    		$.post('updateattribute/attribute', {
    			'name': name,
    			'type': type,
    			'value': value,
    		}, function (response) {
    			location.reload();
    		});
        });

    $('.runner button.forDelete').click(function(e) {
		e.preventDefault();
        let runner = $(this).parent().parent().parent();
        let atm_attribute_id = $(runner).find('.atm_attribute_id').attr("value");
        $('.runner button.forUpdate').attr("disabled","disabled");
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('delete/attribute', {
			'atm_attribute_id': atm_attribute_id
		}, function (response) {
			location.reload();
		});
    });
});
