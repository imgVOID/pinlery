jQuery(document).ready(function($) {
    var $win = $(window),
        $con = $(".masonry-grid")

    $con.isotope({
        itemSelector: '.masonry-grid-item',
        stagger: 30,
        layout: 'packery'
    });

    $con.imagesLoaded().progress( function() {
        $con.isotope('layout');
    });

    $con.on('layoutComplete', function(){
        $win.trigger("scroll");
    });

});