$(document).ready(function(){
  // initialize modal
  $('.modal').modal();
  // initialize dropdown select input element
  $('select').material_select();
  // AJAX for reloading base page

  function reloadBase() {
    var type = 'ajax'
    $.ajax({
      url : '/budget/envelopes/',
      type: 'GET',
      data: {'type': type},
      success : function(data) {
          $('#modal').modal('close');
          $('#fakeLoader').attr('style', 'position: fixed; width: 100%; height: 100%; top: 0px; left: 0px; background-color: rgb(0, 200, 83); z-index: 1000; display: visible;');
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

  ////////////////////////////////
  /// Edit Envelopes /////////////
  //////////////////////////////
  $('.btnEditEnvelopes').click(function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
    var id = $(this).attr('id')
    $.ajax({
        url: '/budget/envelopes_edit/' + id + '/',
        success: function(data) {
          $('#modal').find('.modal_container').html(data);
          $('#modal').modal('open');
        }
    });
  });
  $('#EditEnvelopesForm').on('submit', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      var id = $('.submit_button').attr('id');
      var dest = '/budget/envelopes_edit/' + id + '/';
      $.ajax({
          url : dest,
          type: 'POST',
          data: $('#EditEnvelopesForm').serialize(),
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
  });
