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
    onSet: function( arg ){
        if ( 'select' in arg ){ //prevent closing on selecting month/year
            this.close();
        }
    }
  });

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
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/goals/')
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
  /// Edit Goals /////////////
  //////////////////////////////
  $('.btnEditGoal').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/goals_edit/' + id + '/',
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
      var dest = '/budget/goals_edit/' + id + '/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditGoalsForm').serialize(),
          success : function(data) {
            if (data === "success") {
              $('#modal').modal('close');
              window.location.replace('/budget/goals/')
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
            $('.modal-content').find('.ajaxForm').html(data);
          }
        }
    });
  });
});
