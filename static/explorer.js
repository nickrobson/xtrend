var flipHeight = -1;

$(document).ready(function() {
    $('#news-article-prev').click(function() {
        var slide = parseInt($('#news-article-bullets .is-active').attr('data-slide'));
        slide = slide == 0 ? $('#news-article-bullets').children().length - 1 : slide - 1;
        setActiveSlide(slide);
    });
    $('#news-article-next').click(function() {
        var slide = parseInt($('#news-article-bullets .is-active').attr('data-slide')) + 1;
        slide = slide == $('#news-article-bullets').children().length ? 0 : slide;
        setActiveSlide(slide);
    });

    var $bullets = $('#news-article-bullets-container');

    $(window).scroll(function(e) {
        var y = e.currentTarget.scrollY;
        if (flipHeight < 0)
            return;
        if (y >= flipHeight && $bullets.css('position') !== 'fixed') {
            $bullets.css({
                'position': 'fixed',
                'top': 120,
                'left': $bullets.offset().left,
                'width': 'inherit'
            });
        }
        if (y < flipHeight && $bullets.css('position') === 'fixed') {
            $bullets.css({ 'position': 'initial', 'width': '100%' });
        }
    })
    $(window).scroll();
});

function setActiveSlide(slide) {
    $('#news-article-bullets').children().removeClass('is-active').eq(slide).addClass('is-active');
    $('#news-articles').children().hide().eq(slide).show();
}

function loadFormatted(jsonData) {
    var $ulTag = $("#news-articles");
    $ulTag.find("li").remove(); // get rid of li tags inside
    // li tag .appendTo(html);
    var $bullets = $("#news-article-bullets");
    $bullets.children().remove();
    // delete existing children
    for (var i = 0; i < jsonData.NewsDataSet.length; i++) {
        var article = jsonData.NewsDataSet[i];
        
        // add new li tag
        var $liTag = $("<li>").addClass("card");
        $liTag.css({'padding': '20px'});
        if (i == 0) {
            $liTag.addClass("is-active");
        }
        var $h3Tag = $("<h3>").text(article.Headline).css({'font': 'normal 400 41px/43px "Unit Slab Pro Bold","Times New Roman",Times,serif'});
        var $hrTag = $("<hr>");
        var $textTag = $("<div>").text(article.NewsText).css({'font-family': "Times New Roman"});
        var $dateTag = $("<div>").text(new Date(article.TimeStamp).toString()).css({'font-family': "Times New Roman", 'color': '#555'});
        $textTag.html($textTag.html().replace(/\n    /g, "<br><br>"));
        
        $h3Tag.appendTo($liTag);
        $dateTag.appendTo($liTag);
        $hrTag.appendTo($liTag);
        $textTag.appendTo($liTag);
        $liTag.appendTo($ulTag);

        $liTag.css({'height': 'auto'});
        
        // add new bullet
        var $bullet = $("<button>").attr("data-slide", i.toString());
        if (i == 0) {
            $bullet.addClass("is-active");
        }
        $bullet.appendTo($bullets);
    }
    $("#news-articles").css({'height': 'auto'});

    $('#news-article-bullets button').click(function() {
        var attr = this.getAttribute('data-slide');
        if (attr == '')
            return;
        var slide = parseInt(attr);
        setActiveSlide(slide);
    });

    setActiveSlide(0);
}

function viewFormatted() {
    var query = readFormInput();

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/coolbananas/api/' + query);

    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            var data = JSON.parse(xhr.responseText);
            loadFormatted(data);
            $('.explore').hide();
            $('.html-articles').show();
            flipHeight = $('#news-article-bullets-container').offset().top - 120;
            $(window).scroll();
        }
    };
    xhr.send();
}

function viewJSON() {
    var query = readFormInput();

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/coolbananas/api/' + query);
    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            var data = JSON.parse(xhr.responseText);
            $('#explore-query').text('/coolbananas/api/' + query);
            $('#explore-result').jsonViewer(data, {collapsed: false, withQuotes: true});
            $('.html-articles').hide();
            $('.explore').show();
        }
    };
    xhr.send();
}

function fillExample() {
    $('#explore-rics').val("BHP.AX,BLT.L");
    $('#explore-topics').val("AMERS,COM");
    $('#explore-start-date').val("2015-10-01T00:00:00");
    $('#explore-end-date').val("2015-10-10T00:00:00");
    viewFormatted();
}

function getValueOf(id) {
    return document.getElementById(id).value;
}

function readFormInput() {
    var rics = getValueOf('explore-rics');
    var topics = getValueOf('explore-topics');
    var startDate = getValueOf('explore-start-date');
    var endDate = getValueOf('explore-end-date');

    if (startDate.length < 17) {
        startDate += ':00';
    }
    if (startDate.length < 20) {
        startDate += '.000';
    }
    if (!startDate.endsWith('Z')) {
        startDate += 'Z';
    }

    if (endDate.length < 17) {
        endDate += ':00';
    }
    if (endDate.length < 20) {
        endDate += '.000';
    }
    if (!endDate.endsWith('Z')) {
        endDate += 'Z';
    }

    var query_params = [
        ['InstrumentIDs', rics],
        ['TopicCodes', topics],
        ['StartDate', startDate],
        ['EndDate', endDate]
    ];

    var query = "";

    for (var i = 0, j = query_params.length; i < j; i++) {
        var query_param = query_params[i];
        if (query_param[1].length == 0) {
            continue;
        }
        query += query.length ? '&' : '?';
        query += query_param[0];
        query += '=';
        query += encodeURIComponent(query_param[1]);
    }
    return query
}