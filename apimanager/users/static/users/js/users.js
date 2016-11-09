$(document).ready(function($) {
	$('#user-detail').hide();
	$('.users .user-row').click(function() {
		$('.users .user-row').removeClass('active');
		$(this).addClass('active');
		var user_id = $(this).data('user-id')
		$.each(USERS, function (idx, user) {
			if (user['id'] == user_id) {
				$('#user-detail-id').val(user['id']);
				$('#user-detail-name').html(user['name_']);
				var isSuperAdmin = $('#user-detail-is-super-admin');
				if (user['is_super_admin']) {
					isSuperAdmin.html('Super Admin');
				} else {
					isSuperAdmin.html('');
				}
				$('#user-detail-email').html(user['email']);
				$('#user-detail-last-login').html(user['last_login']);
				$('#user-detail .entitlement').remove();
				$.each(user['entitlements'], function(idx, entitlement) {
					var role_name = entitlement['role_name'];
					console.log('entitlement ' + entitlement);
					var formgroup = $('#entitlement-template').clone();
					formgroup.removeAttr('id');
					formgroup.addClass('entitlement');
					var checkbox = formgroup.find('input');
					checkbox.prop('checked', true);
					checkbox.attr('name', 'entitlement-' + role_name);
					checkbox.attr('id', 'user-detail-entitlement-' + role_name);
					var label = formgroup.find('label');
					label.attr('for', 'user-detail-entitlement-' + role_name);
					label.html(role_name);
					formgroup.appendTo('#user-detail form');
				});
				$('#user-detail').show();
			}
		});
	});
});

