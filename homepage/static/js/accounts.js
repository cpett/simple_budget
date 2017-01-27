$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  $('#btnAddAccounts').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/budget/accounts_add',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });

  $('#btnRemoveAccounts').click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/budget/accounts_remove',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
});
