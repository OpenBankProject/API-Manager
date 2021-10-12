$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var api_collection_body = $(runner).find('.api-collection-body').val();
    
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('save/apicollection', {
			'api-collection-body': api_collection_body,
		}, function (response) {
			location.reload(); 
		});
    });

    $('.runner button.forDelete').click(function(e) {
		e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var api_collection_id = $(runner).find('.api_collection_id').html();
		$('.runner button.forSave').attr("disabled","disabled");
		$('.runner button.forDelete').attr("disabled","disabled");
		$.post('delete/apicollection', {
			'api_collection_id': api_collection_id
		}, function (response) {
			location.reload();
		});
    });
});
