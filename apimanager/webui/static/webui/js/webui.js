$(document).ready(function($) {
    $('.runner button.forSave').click(function(e) {
        e.preventDefault();
        const t = $(this);
        const runner = t.parent().parent().parent();
        const web_ui_props_name = $(runner).find('.web_ui_props_name').text();
        const web_ui_props_value = $(runner).find('.web_ui_props_value').val();
        $('.runner button.forSave').attr("disabled", "disabled");
        $('.runner button.forDelete').attr("disabled", "disabled");
        $.post('save/method', {
            'web_ui_props_name': web_ui_props_name,
            'web_ui_props_value': web_ui_props_value,
        }, function(response) {
            location.reload();
        });
    });

    $('.runner button.forDelete').click(function(e) {
        e.preventDefault();
        const t = $(this);
        const runner = t.parent().parent().parent();
        const props_id = $(runner).find('.web_ui_props_id');
        const web_ui_props_id = props_id.val();
        $('.runner button.forSave').attr("disabled", "disabled");
        $('.runner button.forDelete').attr("disabled", "disabled");
        $.post('delete/method', {
            'web_ui_props_id': web_ui_props_id,
        }, function(response) {
            location.reload();
        });
    });
});
