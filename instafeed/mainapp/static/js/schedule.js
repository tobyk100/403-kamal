$(document).on('ready', function() {
    $('#updateContent').bind('keyup keypress', countNewPostChars);
    //bind submit button
    //$('#submitScheduledPost').on('click', submit_scheduled_post);
});

function schedule_post(year_, month_, day_, hour_, minute_, message_, post_site_) {
    $.ajax({
        type: 'POST',
        url: '/scheduled_update/',
        data: {
	    year: year_,
            month: month_,
	    day: day_,
	    hour: hour_,
	    minute: minute_,
	    second: 0,
	    microsecond: 0,
	    message: message_,
	    post_site: post_site_,
            type: 'scheduled_post'
        },
        datatype: 'json',
        error: function(data) {
          alert(data);
        },
	success: function(data) {
	    alert("Message scheduled");
	}
    });
}

function submit_scheduled_post(){
    var year = $('#').val();
    var month = $('#').val();
    var day = $('#').val();
    var hour = $('#').val();
    var minute = $('#').val();
    var message = $('#').val();

    var post_site = $('#').val();
    //check to make sure all selected
    schedule_post(year, month, day, hour, minute, message, post_site);
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
