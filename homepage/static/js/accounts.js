$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();
  // AJAX for reloading base page
  function reloadBase() {
    var type = 'ajax'
    $.ajax({
      url : '/budget/accounts/',
      type: 'GET',
      data: {'type': type},
      success : function(data) {
        console.log('here')
          $('#fakeLoader').attr('style', 'position: fixed; width: 100%; height: 100%; top: 0px; left: 0px; background-color: rgb(0, 200, 83); z-index: 1000; display: visible;');
          $('#modal').modal('close');
          $('#ajaxID').find('.ajaxBody').html(data);
          setTimeout(function (){
            $('#fakeLoader').hide();
          }, 1000);
      },
      // handle a non-successful response
      error : function(xhr,errmsg,err) {
      }
    });
  };

  $('.btnAddAccounts').click(function(e){
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
            if (data === "success") {
              // Ajax reload base page
              reloadBase();
            }else {
              $('.modal-content').find('.ajaxForm').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
            $('.modal-content').find('.ajaxForm').html(data);
          }
      });
  });
  ////////////////////////////////
  /// Edit Accounts /////////////
  //////////////////////////////
  $('.btnEditAccount').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
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
      var dest = '/budget/accounts_edit/' + id + '/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditAccountsForm').serialize(),
          success : function(data) {
            if (data === "success") {
              reloadBase();
            }else {
              $('.modal-content').find('.ajaxForm').html(data);
            }
          },
          // handle a non-successful response
          error : function(xhr,errmsg,err) {
            $('.modal-content').find('.ajaxForm').html(data);
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
          if (data === "success") {
            reloadBase();
          }else {
            $('.modal-content').find('.ajaxForm').html(data);
          }
        }
    });
  });
});
