function getValueOf(id) {
    return document.getElementById(id).value;
}

function submitExplore() {
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


    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/coolbananas/api/' + query);
    xhr.onload = function() {
        if (xhr.readyState === xhr.DONE) {
            var data = JSON.parse(xhr.responseText);
            $('#explore-query').text('/coolbananas/api/' + query);
            $('#explore-result').jsonViewer(data, {collapsed: false, withQuotes: true});
            $('.explore').show();
        }
    };
    xhr.send();
}