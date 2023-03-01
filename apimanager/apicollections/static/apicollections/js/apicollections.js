$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        let runner = $(this).parent().parent().parent();
        let api_collection_name = $(runner).find('.api_collection_name').val();
        let api_collection_is_sharable = $(runner).find('.api_collection_is_sharable').val();
        let api_collection_description = $(runner).find('.api_collection_description').val();
        $('.runner button.forUpdate').attr("disabled","disabled");
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('save/apicollection', {
			'api_collection_name': api_collection_name,
			'api_collection_is_sharable': api_collection_is_sharable,
			'api_collection_description': api_collection_description,
		}, function (response) {
			location.reload(); 
		});
    });
    $('.runner button.forUpdate').click(function(e) {
        e.preventDefault();
        let runner = $(this).parent().parent().parent();
        let api_collection_id = $(runner).find('.api_collection_id').attr("value");
        let api_collection_name = $(runner).find('.api_collection_name').val();
        let api_collection_is_sharable = $(runner).find('.api_collection_is_sharable').val();
        let api_collection_description = $(runner).find('.api_collection_description').val();
        $('.runner button.forUpdate').attr("disabled","disabled");
        $('.runner button.forSave').attr("disabled","disabled");
        $('.runner button.forDelete').attr("disabled","disabled");
        $.post('update/apicollection', {
                'api_collection_id': api_collection_id,
                'api_collection_name': api_collection_name,
                'api_collection_is_sharable': api_collection_is_sharable,
                'api_collection_description': api_collection_description,
            }, function (response) {
                location.reload();
        });
    });

    $('.runner button.forDelete').click(function(e) {
		e.preventDefault();
        let runner = $(this).parent().parent().parent();
        let api_collection_id = $(runner).find('.api_collection_id').attr("value");
        $('.runner button.forUpdate').attr("disabled","disabled");
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('delete/apicollection', {
			'api_collection_id': api_collection_id
		}, function (response) {
			location.reload();
		});
    });
});
