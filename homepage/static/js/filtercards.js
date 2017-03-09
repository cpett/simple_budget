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

  $('#sort_list').change(function() {
    var filter_val = $(this).val();
      var $wrapper = $('.boxes');
    if (filter_val == 'alph') {
      $wrapper.find('.mix').sort(function(a, b) {
          return String.prototype.localeCompare.call(a.getAttribute('data-category').toLowerCase(),
            b.getAttribute('data-category').toLowerCase());
      })
      .appendTo($wrapper);
    } else {
      $wrapper.find('.mix').sort(function(a, b) {
          return +a.getAttribute('data-value') - +b.getAttribute('data-value');
      })
      .appendTo($wrapper);
    }

  });
});
