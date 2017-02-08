$(document).ready(function(){
  var $filters = $('.filter [data-filter]'),
    $boxes = $('.boxes [data-category]');

  $('#filter_list').change(function() {
    var filter_val = $(this).val();
    if (filter_val == 'all') {
      $boxes.removeClass('is-animated')
        .fadeOut().promise().done(function() {
          $boxes.addClass('is-animated').fadeIn();
        });
    } else {
      $boxes.removeClass('is-animated')
        .fadeOut().promise().done(function() {
          $boxes.filter('[data-category = "' + filter_val + '"]')
            .addClass('is-animated').fadeIn();
        });
    }

  });

});
