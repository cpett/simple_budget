$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();

  $('.btnAddGoals').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/budget/goals_add',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#AddGoalForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/budget/goals_add/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#AddGoalForm').serialize(),
          success : function(data) {
            // TODO: FIX THIS HACK of AJAX success
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/goals/')
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
  ////////////////////////////////
  /// Edit Accounts /////////////
  //////////////////////////////
  $('.btnEditAccount').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    console.log('herehehrerhe')
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/accounts_edit/' + id,
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#EditAccountsForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var id = $('.submit_button').attr('id');
      var dest = '/budget/accounts_edit/' + id;
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditAccountsForm').serialize(),
          success : function(data) {
            // TODO: FIX THIS HACK of AJAX success
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/accounts/')
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

  // Button on accounts.html (initiate delete)
  $('.btnConfirmAccount').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/accounts_remove_confirm/' + id + '/',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });

  // Button in the modal (Confirm delete)
  $('.btnRemoveAccount').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/accounts_remove/' + id + '/',
        success : function(data) {
          // TODO: FIX THIS HACK of AJAX success
          if (data === "success") {
            $('#modal').modal('close');
            window.location.replace('/budget/accounts/')
          }else {
            $('#modal').find('.modal-content').html(data);
          }
        }
    });
  });
});
