$(document).ready(function(){
  $(".button-collapse").sideNav();

  // $('ul.tabs a').on('click', function(e){
  //   if($(this).attr("target") ) {
  //     window.location = $(this).attr("href");
  //   }
  // });

  $('.btnSignUp').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/sign_up',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').openModal();
        }
    });
  });

  $('.btnSignIn').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/sign_in',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').openModal();
        }
    });
  });
});
