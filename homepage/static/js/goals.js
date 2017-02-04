$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();

  $('#btnAddGoals').click(function(e){
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
  /// Edit Goals /////////////
  //////////////////////////////
  $('.btnEditGoal').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    console.log('herehehrerhe')
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/goals_edit/' + id,
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#EditGoalsForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var id = $('.submit_button').attr('id');
      var dest = '/budget/goals_edit/' + id;
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditGoalsForm').serialize(),
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

  // Button on accounts.html (initiate delete)
  $('.btnConfirmGoal').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/goals_remove_confirm/' + id + '/',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });

  // Button in the modal (Confirm delete)
  $('.btnRemoveGoal').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/goals_remove/' + id + '/',
        success : function(data) {
          // TODO: FIX THIS HACK of AJAX success
          if (data === "success") {
            $('#modal').modal('close');
            window.location.replace('/budget/goals/')
          }else {
            $('#modal').find('.modal-content').html(data);
          }
        }
    });
  });
});