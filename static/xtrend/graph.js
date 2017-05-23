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
        .x(function(d) { return x(d.Date); })
        .y(function(d) { return y(d.AdjustedClose); });

    // Get the data
    xtrendLoadGraph = function(ric) {
        $('.graphContainer').empty();
        
        // Adds the svg canvas
        var svg = d3.select(".graphContainer")
            .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform", 
                      "translate(" + margin.left + "," + margin.top + ")");

        d3.json("/coolbananas/xtrend/returns/" + encodeURIComponent(ric), function(error, data) {
            data = data[ric];
            data = data.filter(function(d) {
                return d.AdjustedClose >= 0;
            }).map(function(d) {
                return {
                    Date: parseDate(d.Date),
                    AdjustedClose: +d.AdjustedClose,
                };
            });

            var y_extent = d3.extent(data, function(d) { return d.AdjustedClose; });
            var y_diff = (y_extent[1] - y_extent[0]) / 10;

            // Scale the range of the data
            x.domain(d3.extent(data, function(d) { return d.Date; }));
            y.domain(y_extent.map(function(e, i) { return e + y_diff * (i * 2 - 1); }));

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
})();