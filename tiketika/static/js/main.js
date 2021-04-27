var seatBtn = document.getElementsByClassName('seatList')
var reviewBtn = document.getElementById('reviewBtn')

  //preloader
  $(window).on('load', function() {
    if ($('#preloader').length) {
      $('#preloader').delay(100).fadeOut('slow', function() {
        $(this).remove();
      });
    }
  });

for( var i=0; i < seatBtn.length; i++ ){
    
    seatBtn[i].addEventListener('click', function(){
        
        var seat = this.dataset.seat
        var currentSeat = document.getElementById('selectedSeat').value
        console.log(seat);
        console.log(currentSeat);
        document.getElementById('selectedSeat').value=seat

        if( seat != currentSeat){
            document.getElementById(seat).classList.add('btn-warning')
            document.getElementById(currentSeat).classList.remove('btn-warning')
        }
    })
}

reviewBtn.addEventListener('click', function(){
    document.getElementById('formView').classList.remove('d-none')
    document.getElementById('reviewBtn').classList.add('d-none')

})

function validate(){
    var selectedSeat = document.getElementById('selectedSeat').value
    if (selectedSeat == ""){
        alert('please select a seat number')
        document.getElementById('selectedSeat').focus();
        return false
    }
}


  // Back to top button
  $(window).scroll(function() {
    if ($(this).scrollTop() > 150) {
      $('.back-to-top').show('slow');
    } else {
      $('.back-to-top').hide('slow');
    }
  });

  $('.back-to-top').click(function() {
    $('html, body').animate({
      scrollTop: 0
    },1000);

    return false;
  });

  $(window).scroll(function() {
    if ($(this).scrollTop() > 50) {
      $('#header').addClass('header-scrolled');
    } else {
      $('#header').removeClass('header-scrolled');
    }
  });