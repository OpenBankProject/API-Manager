$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var connector_method_name = $(runner).find('.connector_method_name').val();
        var connector_method_programming_lang = $(runner).find('.connector_method_programming_lang').val();
        var connector_method_body = $(runner).find('.connector_method_body').val();

        $('.runner button.forSave').attr("disabled", "disabled");
        $('.runner button.forDelete').attr("disabled", "disabled");
        $.post('save/connectormethod', {
            'connector_method_name': connector_method_name,
            'connector_method_programming_lang': connector_method_programming_lang,
            'connector_method_body': connector_method_body,
        }, function(response) {
            location.reload();
        });
    });

    $('.runner button.forUpdate').click(function(e) {
        e.preventDefault();
        var t = $(this);
        var runner = t.parent().parent().parent();
        var connector_method_id = $(runner).find('.connector_method_id').html();
        var connector_method_programming_lang_update = $(runner).find('.connector_method_programming_lang_update').val();
        var connector_method_body_update = $(runner).find('.connector_method_body_update').val();

        $('.runner button.forSave').attr("disabled", "disabled");
        $('.runner button.forUpdate').attr("disabled", "disabled");
        $.post('update/connectormethod', {
            'connector_method_id': connector_method_id,
            'connector_method_programming_lang_update': connector_method_programming_lang_update,
            'connector_method_body_update': connector_method_body_update,
        }, function(response) {
            location.reload();
        });
    });
});