$(document).ready(function() {
    $(document).foundation();
    $(window).scroll(function() {
        var x = document.documentElement.scrollLeft || document.body.scrollLeft;
        var y = document.documentElement.scrollTop  || document.body.scrollTop;

        if (y == 0) {
            $('#title-div').removeClass('shrink');
        } else {
            $('#title-div').addClass('shrink');
        }
    });
});