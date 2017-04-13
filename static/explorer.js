

function viewArticlesWindow(jsonData) {

    /*var html = '<h3>'
    + jsonData.NewsDataSet[0].Headline
    + '</h3>'
    + '<div>'
    + jsonData.NewsDataSet[0].NewsText;
*/
    var $ulTag = $("#news-articles");
    $ulTag.find("li").remove(); // get rid of li tags inside
    // li tag .appendTo(html);
    var $bullets = $("#news-article-bullets");
    $bullets.children().remove();
    // delete existing children
    for (var i = 0; i < jsonData.NewsDataSet.length; i++) {
        var article = jsonData.NewsDataSet[i];
        // add new li tag
        var $liTag = $("<li>").addClass("orbit-slide");
        if (i == 0) {
            $liTag.addClass("is-active");
        }
        var $h3Tag = $("<h3>").text(article.Headline);
        var $textTag = $("<div>").text(article.NewsText).css({'font-family': 'Droid Sans Mono, monospace'});
        $textTag.html($textTag.html().replace(/\n    /g, "<br><br>"));
        // div tag
        $h3Tag.appendTo($liTag);
        $textTag.appendTo($liTag);
        $liTag.appendTo($ulTag);
        

        // add new bullet
        var $bullet = $("<button>").attr("data-slide", i.toString());
        if (i == 0) {
            $bullet.addClass("is-active");
        }
        var $span = $("<span>").addClass("show-for-sr");
        $span.appendTo($bullet);
        $bullet.appendTo($bullets);
    }
    Foundation.reInit($('#news-articles-container'));
}

function viewNews() {
    var query = readFormInput();

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/coolbananas/api/' + query);

    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            var data = JSON.parse(xhr.responseText);
            viewArticlesWindow(data);
            $('.explore').hide();
            $('.html-articles').show();
        }
    };
    xhr.send();
}



function submitExplore() {
    var query = readFormInput()

    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/coolbananas/api/' + query);
    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            var data = JSON.parse(xhr.responseText);
            console.log(data);
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
    submitExplore();
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