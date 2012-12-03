$(document).on('ready', function() {
    //bind submit button
    alert("got into js");
    $('#submitScheduledPost').on('click', submit_scheduled_post);
});

function schedule_post(year_, month_, day_, hour_, message_, post_site_) {
    $.ajax({
        type: 'POST',
        url: '/scheduled_update/',
        data: {
	    year: year_,
            month: month_;
	    day: day_;
	    hour: hour_,
	    minute: '0',
	    second: '0',
	    microsecond: '0',
	    message: message_,
	    post_site: post_site_,
            type: 'scheduled_post'
        },
        datatype: 'json',
        error: function(data) {
          alert(data);
        }
	success: function(data) {
	    alert("Message scheduled");
	}
    });
}

function submit_scheduled_post(){
    var year = $('#scheduleYear').val();
    var month = $('#scheduleMonth').val();
    var day = $('#scheduleDay').val();
    var hour = $('#scheduleHour').val();
    var message = $('#updateContent').val();
    var post_site = 0;
    if ($('#postOptionFacebook').is(':checked') && 
	$('#postOptionTwitter').is(':checked')) {
	post_site = 3;
    } else if ($('#postOptionFacebook').is(':checked')) {
	post_site = 1;
    } else if ($('#postOptionTwitter').is(':checked')) {
	post_site = 2;
    } else {
	return;
    }
    alert("calling shedule");
    //check to make sure all selected
    schedule_post(year, month, day, hour, message, post_site);
}