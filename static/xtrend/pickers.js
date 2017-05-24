var companies = [];
var chosenRics = new Set();
var updateChosenRics = function() {};

$.getJSON('/coolbananas/api/companies/', function(data) {
    data.Companies.forEach(function(e) {
        if (e['Exchanges'].hasOwnProperty('AX')) {
            companies.push({'InstrumentID': e['InstrumentID'] + '.AX', 'Name': e['Name']});
        }
    });
    companies = companies.sort(function(a, b) {
        var x = a['InstrumentID'], y = b['InstrumentID'];
        return x == y ? 0 : (x > y ? 1 : -1);
    });
}).then(function() {
    var $parent = $('#ricpicker-container');
    var $companyPicker = $('<select>');
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

    companies.forEach(function(company) {
        var display = company['InstrumentID'] + ' - ' + company['Name'];
        var $option = $('<option>').attr('value', company['InstrumentID']).text(display);

        $option.appendTo($companyGroup);
    });

    $defaultCompanyOption.appendTo($companyPicker);
    $companyGroup.appendTo($companyPicker);

    $companyPicker.change(function() {
        var ric = $(this).val();
        chosenRics.add(ric);
        updateChosenRics();
    });

    function makeLabel($el, text) {
        var $label = $('<label>').text(text);
        $el.appendTo($label);
        $label.appendTo($parent);
    }

    makeLabel($companyPicker, 'Companies');
    makeLabel($chosenRics, 'Chosen Instrument IDs');
    updateChosenRics();
    $parent.foundation();
});