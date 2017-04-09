$(document).ready(function() {
    $(document).foundation();
    var $titleDiv = $('#title-div');
    var $faqMenu = $('#faq-menu');
    var faqExists = $faqMenu.position
    var initialHeight = $faqMenu.length ? $faqMenu.position().top : undefined;
    $(window).scroll(function() {
        var x = document.documentElement.scrollLeft || document.body.scrollLeft;
        var y = document.documentElement.scrollTop  || document.body.scrollTop;

        if (y == 0) {
            $titleDiv.removeClass('shrink');
        } else {
            $titleDiv.addClass('shrink');
        }

        if ($faqMenu.length) {
            if (y >= initialHeight + $titleDiv.height()) {
                $faqMenu.css({'position': 'fixed', 'top': initialHeight, 'left': $faqMenu.position().left});
            } else {
                $faqMenu.css({'position': 'static'});
            }
        }
    });
});