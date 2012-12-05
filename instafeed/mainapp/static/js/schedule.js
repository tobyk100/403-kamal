$(document).on('ready', function() {
    $('#updateContent').bind('keyup keypress', countNewPostChars);
    //bind submit button
    $('#sumbitScheduledPost').on('click', submit_scheduled_post);
    $('#scheduledPosts.edit-post"
});

function schedule_post(year_, month_, day_, hour_, message_, post_site_) {
    alert("ajax");
    $.ajax({
        type: 'POST',
        url: '/scheduled_update/',
        data: {
            year: year_,
            month: month_,
            day: day_,
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
          alert("failure" + data.error);
        },
        success: function(data) {
            alert("Message scheduled");
        }
    });
}

function submit_scheduled_post(){
    //alert("button clicked");
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
    
    if (year == 'Year' || month == 'Month' || 
		day == 'Day' || hour == 'Hour' || 
		message == '') {
		alert("Fill in all fields");
		return;
    }
    alert("about to call ajax function");
    schedule_post(year, month, day, hour, message, post_site);
}

function countNewPostChars() {
  if ($('#postOptionTwitter').is(':checked')) {
    var count = $(this).val().length,
        count_elem = $('#textCount');
    count_elem.text(count);
    if (count > 140) {
      count_elem.addClass('text-error');
    } else {
      count_elem.removeClass('text-error');
    }
  } else {
    $('#textCount').text('');
  }
}

