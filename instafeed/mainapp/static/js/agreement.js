(function($, undefined) {
	var accept_btn = $($('.modal-footer .btn-primary')[0]);
	accept_btn.bind('click', function() {
		$('#agreement-checkbox').attr('checked', true);
	});
}) (jQuery);