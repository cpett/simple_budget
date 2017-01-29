$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();

  $('#btnAddAccounts').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();

    $.ajax({
        url: '/budget/accounts_add',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#AddAccountForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/budget/accounts_add/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#AddAccountForm').serialize(),
          success : function(data) {
            // TODO: FIX THIS HACK of AJAX success
            if (data === "success") {
              $('#modal').modal('close');
            }else {
              $('#modal').find('.modal-content').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
              $('#modal').find('.modal-content').html(data);
              // location.reload();
          }
      });
  });

  $('#btnRemoveAccounts').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();

    $.ajax({
        url: '/budget/accounts_remove',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
});
