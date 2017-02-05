$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();
  $('.datepicker').pickadate({
    selectMonths: true, // Creates a dropdown to control month
    selectYears: 15, // Creates a dropdown of 15 years to control year
    container: 'body',
    format: 'yyyy-mm-dd',
    closeOnSelect: true
  });

  $('#btnAddTransactions').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    $.ajax({
        url: '/budget/transactions_add',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#AddTransactionsForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var dest = '/budget/transactions_add/';
      var date = $('#id_date_root').val();
      console.log(date)
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#AddTransactionsForm').serialize(),
          success : function(data) {
            // TODO: FIX THIS HACK of AJAX success
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/transactions/')
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
  /// Edit Transactions /////////
  //////////////////////////////
  $('.btnEditTransactions').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/transactions_edit/' + id,
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#EditTransactionsForm').on('submit', function(e){
    console.log('here')
      e.preventDefault();
      e.stopImmediatePropagation();
      var id = $('.submit_button').attr('id');
      var dest = '/budget/transactions_edit/' + id;
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditTransactionsForm').serialize(),
          success : function(data) {
            // TODO: FIX THIS HACK of AJAX success
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/transactions/')
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
  $('.btnConfirm').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/transactions_remove_confirm/' + id + '/',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });

  // Button in the modal (Confirm delete)
  $('.btnRemove').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/transactions_remove/' + id + '/',
        success : function(data) {
          // TODO: FIX THIS HACK of AJAX success
          if (data === "success") {
            $('#modal').modal('close');
            window.location.replace('/budget/transactions/')
          }else {
            $('#modal').find('.modal-content').html(data);
          }
        }
    });
  });
});
