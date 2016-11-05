$(document).ready(function(){
  $(".button-collapse").sideNav();

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
});
