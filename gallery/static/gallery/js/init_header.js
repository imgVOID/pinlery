$(function() {
    $("#header").mhead({
        scroll: {
            hide: 20000
        },
    });
});

$(function(){
  var prevScroll = 0,
      curDir = 'down',
      prevDir = 'up';

  $(window).scroll(function(){
        if($(this).scrollTop() >= prevScroll){
          curDir = 'down';
          if(curDir != prevDir){
          $('#pagination').stop();
            $('#pagination').animate({ bottom: '-50px' }, 300);
          prevDir = curDir;
          }
      } else {
          curDir = 'up';
          if(curDir != prevDir){
          $('#pagination').stop();
          $('#pagination').animate({ bottom: '0px' }, 300);
          prevDir = curDir;
          }
      }
      prevScroll = $(this).scrollTop();
  });
})

$(document).ready(function(){
    // scroll body to 0px on click
    $('#back-to-top').click(function () {
        $('body,html').animate({
            scrollTop: 0
        }, 400);
        return false;
    });
});