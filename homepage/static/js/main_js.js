$(document).ready(function(){
  // Menu Init
  $(".button-collapse").sideNav();
  // initialize modal
  $('.modal').modal();

  // PARALLAX INIT
  $(document).ready(function(){
        $('.parallax').parallax();
  });

  $('.btnSignUp').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/sign_up',
        success: function(data) {
          console.log(data)
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });

  $('.btnSignIn').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/sign_in',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
});
