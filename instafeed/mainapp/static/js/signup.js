var error_msg_class = 'error-msg';

function remove_error(elem) {
	if (elem.attr('type') === 'checkbox') {
		elem.parent().css('border-bottom', '');
		elem.parent().next().remove();
	} else {
		elem.css('border', '1px solid #CCC');
		elem.next().remove();
	}
}

// add red border on the box contained the element.
function mark_as_error(elem, msg, error_msg_class) {
	var error_msg = $('<span>').addClass(error_msg_class).text(msg).css('color', 'red');
	if (elem.attr('type') === 'checkbox') {
		elem.parent().css('border-bottom', '2px solid red');
		elem.parent().after(error_msg);
	} else {
		elem.css('border', '2px solid red');
		if (elem.parent().find('.' + error_msg_class).length == 0) {
			elem.after(error_msg);
		} else {
			elem.next().text(msg);
		}
	}
}

function verify_email(email_field) {
	remove_error(email_field);
	var re = /\S+@\S+\.\S+/;
	if (email_field.val() === '') {
		mark_as_error(email_field, 'Please fill in email address.');
		return false;
	} else if (!re.test(email_field.val())) {
		mark_as_error(email_field, 'Incorrect email format.');
		return false;
	}
	return true;
}

function verify_pw(pw) {
	remove_error(pw);
	if (pw.val() === '') {
		mark_as_error(pw, 'Please fill in your password.');
		return false;
	}
	return true;
}

function verify_pw_again(pw, pw_again) {
	remove_error(pw_again);
	if (pw_again.val() === '') {
		mark_as_error(pw_again, 'Please confirm your password.');
		return false;
	} else if (pw.val() !== pw_again.val()) {
		mark_as_error(pw_again, 'Passwords don\'t match.');
		return false;
	}
	return true;
}

function verify_agreement_checkbox(agreement_checkbox) {
	remove_error(agreement_checkbox);
	if (agreement_checkbox.attr('checked') !== 'checked') {
		mark_as_error(agreement_checkbox, 'Please accept our agreement.');
		return false;
	}
	return true;
}

(function($, undefined) {
	$($('.modal-footer .btn-primary')[0]).bind('click', function() {
		$('#agreement-checkbox').attr('checked', true);
	});

	// validate email address
	var email_field = $('#id_email');
	email_field.bind('blur', function() {
		verify_email(email_field);
	});

	var pw = $('#id_password1'),
		pw_again = $('#id_password2');

	pw.bind('blur', function() {
		verify_pw(pw);
	});

	pw_again.bind('blur', function () {
		verify_pw_again(pw, pw_again);
	});

	var agreement_checkbox = $('#agreement-checkbox');
	agreement_checkbox.bind('click', function() {
		verify_agreement_checkbox(agreement_checkbox);
	})

	$('#signup-submit').bind('click', function(e) {
		e.preventDefault();
		var e1 = verify_email(email_field),
			e2 = verify_pw(pw),
			e3 = verify_pw_again(pw, pw_again),
			e4 = verify_agreement_checkbox(agreement_checkbox);
		
		if (e1 && e2 && e3 && e4) {
			console.log("Submit!!", 
				{
					'email': email_field.val(), 
					'password': pw.val(), 
					'set_cookies': $('#set-cookies').attr('checked') === 'checked'
				}
			);
		}
	});
}) (jQuery);