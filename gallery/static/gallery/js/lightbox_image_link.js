    $(document).on('afterShow.fb', function( e, instance, slide ) {
        $(".fancybox-image").wrap('<a href="' + slide.opts.link + '" />');
        document.body.style.cursor = 'grab';
    });

    $(document).on('afterClose.fb', function( e, instance, slide ) {
        document.body.style.cursor = 'default';
    });