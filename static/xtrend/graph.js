var xtrendLoadGraph = function(){};

    (function(){

    // Set the dimensions of the canvas / graph
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = $('.graphContainer').width() - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;
    // Parse the date / time
    var parseDate = d3.timeParse("%Y-%m-%d");

    // Set the ranges
    var x = d3.scaleTime().range([0, width]);
    var y = d3.scaleLinear().range([height, 0]);

    // Axis formatter
    var commasFormatter = d3.format(",.0f")

    // Define the axes
    var xAxis = d3.axisBottom()
        .scale(x)
        .ticks(d3.timeWeek.every(2));

    var yAxis = d3.axisLeft()
        .scale(y)
        .ticks(5)
        .tickFormat(function(d) { return "$" + commasFormatter(d); });

    // Define the line
    var valueline = d3.line()
        .x(function(d) { return x(d.date); })
        .y(function(d) { return y(d.close); });

    var globalRic = undefined;

    // Get the data
    xtrendLoadGraph = function(ric) {
        globalRic = ric;

        $('.graphContainer').empty();
        
        // Adds the svg canvas
        var svg = d3.select(".graphContainer")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", 
                      "translate(" + margin.left + "," + margin.top + ")");

        d3.csv("/coolbananas/xtrend/returns/"+encodeURIComponent(ric), function(error, data) {
            data.forEach(function(d) {
                d.date = parseDate(d.date);
                d.close = +d.close;
            });

            // Scale the range of the data
            x.domain(d3.extent(data, function(d) { return d.date; }));
            y.domain(d3.extent(data, function(d) { return d.close; }).map(function(e, i) { return (i ? Math.floor : Math.ceil)(e + i * 3 - 1.5); }));

            // Add the valueline path.
            svg.append("path")
                .attr("class", "line")
                .attr("d", valueline(data));

            // Add the X Axis
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + height + ")")
                .call(xAxis);

            // Add the Y Axis
            svg.append("g")
                .attr("class", "y axis")
                .call(yAxis);

        });
    }

    $(window).resize(function() {
        if (globalRic !== undefined) {
            xtrendLoadGraph(globalRic);
        }
    });
})();