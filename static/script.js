$(document).ready(function() {
    $(document).foundation();
    var $titleDiv = $('#title-div');
    $(window).scroll(function() {
        var y = document.documentElement.scrollTop || document.body.scrollTop;

        if (y == 0) {
            $titleDiv.removeClass('shrink');
        } else {
            $titleDiv.addClass('shrink');
        }
    });
    $(window).scroll();
});