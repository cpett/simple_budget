$(document).ready(function(){
  // Menu Init
  $(".button-collapse").sideNav({
    menuWidth:200,
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
            // TODO: On successful login, the modal page loads /budget/.
            // need to figure out how to redirect the entire page
            if (data === 'success') {
                window.location.replace('/budget/')
            } else {
              $('#modal').find('.modal-content').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#modal').find('.modal-content').html(data);
              location.reload();
          }
      });
  });

  $('.btnSignIn').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/sign_in',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#LoginForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/sign_in/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#LoginForm').serialize(),
          success : function(data) {
            // TODO: On successful login, the modal page loads /budget/.
            // need to figure out how to redirect the entire page
            if (data === 'success') {
                window.location.replace('/budget/')
            } else {
              $('#modal').find('.modal-content').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#modal').find('.modal-content').html(data);
              // location.reload();
              console.log('Error logging in')
          }
      });
  });
});
