$(document).ready(function(){
  // Menu Init
  $(".button-collapse").sideNav({
    menuWidth:150,
  });
  // initialize modal
  $('.modal').modal();
  // PARALLAX INIT
  $('.parallax').parallax();

  $('.btnSignUp').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/sign_up',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#signupForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/sign_up/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#signupForm').serialize(),
          success : function(data) {
            if (data === 'success') {
              // call fakeLoader and redirect the page
              window.location.replace('/budget/accounts/')
            } else {
              $('.modal-content').find('.ajaxForm').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
            $('.modal-content').find('.ajaxForm').html(data);
              // location.reload();
          }
      });
  });

  $('.btnSignIn').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/login',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#LoginForm').on('submit', function(e){
    $('#modal').modal('close')
    $("#fakeLoader1").fakeLoader({
          timeToHide:6500, //Time in milliseconds for fakeLoader disappear
          zIndex:1000, // Default zIndex
          spinner:"spinner" + (Math.floor(Math.random() * 6) + 1),//Options: 'spinner1', 'spinner2', 'spinner3', 'spinner4', 'spinner5', 'spinner6', 'spinner7'
          bgColor:"#00C853" //Hex, RGB or RGBA colors
          // imagePath:"yourPath/customizedImage.gif" //If you want can you insert your custom image
    });
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/login/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#LoginForm').serialize(),
          success : function(data) {
            if (data === 'success') {
              // call fakeLoader and redirect the page
              loader()
            } else {
              $('#modal').modal('open')
              $('.modal-content').find('.ajaxForm').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
            $('.modal-content').find('.ajaxForm').html(data);
          }
      });
  });

  function loader() {
    $('#modal').modal('close');
      $("#fakeLoader").fakeLoader({
        timeToHide:15000, //Time in milliseconds for fakeLoader disappear
        zIndex:1000, // Default zIndex
        spinner:"spinner" + (Math.floor(Math.random() * 6) + 1),//Options: 'spinner1', 'spinner2', 'spinner3', 'spinner4', 'spinner5', 'spinner6', 'spinner7'
        bgColor:"#00C853" //Hex, RGB or RGBA colors
        // imagePath:"yourPath/customizedImage.gif" //If you want can you insert your custom image
      });
      window.location.replace('/budget/')
  }

  $('.btnPremium').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/budget/premium',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('.close_modal').click(function(){
    $('#modal').modal('close');
  });

  $(window).scroll(function () {
    if ( $(this).scrollTop() > 100 ) {
      $('#sub-nav').fadeIn(500);
    } else if ( $(this).scrollTop() <= 100 ) {
      $('#sub-nav').fadeOut(500);
    }
  });
});
