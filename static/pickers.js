var topics = [];
var companies = {};
var chosenRics = new Set();
var chosenTopics = new Set();
var updateChosenRics = function() {};
var updateChosenTopics = function() {};

$.getJSON('/coolbananas/api/topics/', function(data) {
    data.TopicCodes.forEach(function(e) {
        topics.push(e);
    });
    topics.sort();
}).then(function() {
    var $parent = $('#topicpicker-container');
    var $topicPicker = $('<select>');
    var $chosenTopics = $('<div>');

    updateChosenTopics = function() {
        $chosenTopics.empty();
        var $topicContainer;
        if (chosenTopics.size) {
            $topicContainer = $('<div>').css({'height': '44px', 'border': '1px solid #cacaca', 'padding': '1px', 'margin-bottom': '16px'});
            var i = 0;
            chosenTopics.forEach(function(topic) {
                var $btn = $('<span>').css({'margin-right': '3px', 'display': 'inline-flex', 'align-items': 'center', 'flex-wrap': 'nowrap'});
                var $topicText = $('<span>').text(topic).css({'padding-right': '5px'});
                var $closeBtn = $('<span>').html('&#215;').css({'padding-left': '5px'});
                if (i & 1) {
                    $btn.addClass('button warning');
                    $closeBtn.css({'border-left': '1px solid black'});
                } else {
                    $btn.addClass('button alert');
                    $closeBtn.css({'border-left': '1px solid white'});
                }
                $closeBtn.click(function() {
                    chosenTopics.delete(topic);
                    updateChosenTopics();
                });
                $topicText.appendTo($btn);
                $closeBtn.appendTo($btn);
                $btn.appendTo($topicContainer);
                i++;
            });
        } else {
            $topicContainer = $('<input>').attr('type', 'text').attr('disabled', '');
            $topicContainer.attr('placeholder', 'Use the drop-down menus to choose Topic Codes!');
        }
        $topicContainer.appendTo($chosenTopics);
    }

    var $defaultTopicOption = $('<option>').attr('selected', '').attr('disabled', '').text('Select a topic code...');
    var $topicGroup = $('<optgroup>').attr('label', 'Topic Codes');

    topics.forEach(function(topic) {
        var display = topic; // if/when we implement topic codes' names, we'll do this too
        var $option = $('<option>').attr('value', topic).text(display);

        $option.appendTo($topicGroup);
    });

    $defaultTopicOption.appendTo($topicPicker);
    $topicGroup.appendTo($topicPicker);

    $topicPicker.change(function() {
        var topic = $topicPicker.val();
        chosenTopics.add(topic);
        updateChosenTopics();
    });

    function makeLabel($el, text) {
        var $label = $('<label>').text(text);
        $el.appendTo($label);
        $label.appendTo($parent);
    }

    makeLabel($topicPicker, 'Topic Codes');
    makeLabel($chosenTopics, 'Chosen Topic Codes');
    updateChosenTopics();
    $parent.foundation();
});

$.getJSON('/coolbananas/api/companies/', function(data) {
    data.Companies.forEach(function(e) {
        companies[e['InstrumentID']] = e;
    });
}).then(function() {
    var $parent = $('#ricpicker-container');
    var $companyPicker = $('<select>');
    var $exchangePicker = $('<select>').attr('disabled', '');
    var $chosenRics = $('<div>');

    updateChosenRics = function() {
        $chosenRics.empty();
        var $ricContainer;
        if (chosenRics.size) {
            $ricContainer = $('<div>').css({'height': '44px', 'border': '1px solid #cacaca', 'padding': '1px', 'margin-bottom': '16px'});
            var i = 0;
            chosenRics.forEach(function(ric) {
                var $btn = $('<span>').css({'margin-right': '3px', 'display': 'inline-flex', 'align-items': 'center', 'flex-wrap': 'nowrap'});
                var $ricText = $('<span>').text(ric).css({'padding-right': '5px'});
                var $closeBtn = $('<span>').html('&#215;').css({'padding-left': '5px'});
                if (i & 1) {
                    $btn.addClass('button warning');
                    $closeBtn.css({'border-left': '1px solid black'});
                } else {
                    $btn.addClass('button alert');
                    $closeBtn.css({'border-left': '1px solid white'});
                }
                $closeBtn.click(function() {
                    chosenRics.delete(ric);
                    updateChosenRics();
                });
                $ricText.appendTo($btn);
                $closeBtn.appendTo($btn);
                $btn.appendTo($ricContainer);
                i++;
            });
        } else {
            $ricContainer = $('<input>').attr('type', 'text').attr('disabled', '');
            $ricContainer.attr('placeholder', 'Use the drop-down menus to choose Instrument IDs!');
        }
        $ricContainer.appendTo($chosenRics);
    }

    var $defaultCompanyOption = $('<option>').attr('selected', '').attr('disabled', '').text('Select a company...');
    var $companyGroup = $('<optgroup>').attr('label', 'Companies');

    var companyRics = Array.from(Object.keys(companies)).sort();
    companyRics.forEach(function(ric) {
        var display = ric + ' - ' + companies[ric]['Name'];
        var $option = $('<option>').attr('value', ric).text(display);

        $option.appendTo($companyGroup);
    });

    $defaultCompanyOption.appendTo($companyPicker);
    $companyGroup.appendTo($companyPicker);

    $companyPicker.change(function() {
        var $this = $(this);
        $exchangePicker.empty();
        $exchangePicker.removeAttr('disabled');
        var $defaultExchangeOption = $('<option>').attr('selected', '').attr('disabled', '').text('Select an exchange...');
        var $exchangeGroup = $('<optgroup>').attr('label', 'Exchanges');
        var exchanges = companies[$this.val()]['Exchanges'];

        for (var exchange in exchanges) {
            var display = exchange + ' - ' + exchanges[exchange];
            var $option = $('<option>').attr('value', exchange).text(display);
            $option.appendTo($exchangeGroup);
        }

        $defaultExchangeOption.appendTo($exchangePicker);
        $exchangeGroup.appendTo($exchangePicker);
    });

    $exchangePicker.change(function() {
        var ric = $companyPicker.val() + '.' + $exchangePicker.val();
        chosenRics.add(ric);
        updateChosenRics();
    });

    function makeLabel($el, text) {
        var $label = $('<label>').text(text);
        $el.appendTo($label);
        $label.appendTo($parent);
    }

    makeLabel($companyPicker, 'Companies');
    makeLabel($exchangePicker, 'Exchanges');
    makeLabel($chosenRics, 'Chosen Instrument IDs');
    updateChosenRics();
    $parent.foundation();
});