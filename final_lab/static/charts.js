(function(){

var charts = {}

charts.draw = function(id, data, state, timedata, times){
    var container = document.getElementById("info")
    var margin = {top: 20, right: 160, bottom: 35, left: 50};

    var width = 450 - margin.left - margin.right;//container.width - margin.left - margin.right,
        height = 250 - margin.top - margin.bottom;

    d3.select(id).html("<h2>"+state+"</h2> Click on a bar to see our past predictions.");
    d3.select("#linesvg").html("");
    var svg = d3.select(id)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


    /* Data in strings like it would be if imported from a csv */
    // svg.draw(data){

    // }
    // var data = [{"cand1":"A","cand2":"B","district":"1","party1":"dem","party2":"rep","pred":0.7,"state":"Arizona","time":0},{"cand1":"A","cand2":"B","district":"5","party2":"dem","party1":"rep","pred":0.25,"state":"Massachusetts","time":0}]
    console.log(data);
    data.forEach(entry => {entry[entry["party1"]] = [entry["cand1"], entry["pred1"]]})
    data.forEach(entry => {entry[entry["party2"]] = [entry["cand2"], entry["pred2"]]})
    console.log("WHAT", data);
    // var data = [
    //   { year: "2006", redDelicious: "10", mcintosh: "15", oranges: "9", pears: "6" },
    // ];

    // var parse = d3.time.format("%Y").parse;


    // Transpose the data into layers
    // var dataset = d3.layout.stack()(["redDelicious", "mcintosh", "oranges", "pears"].map(function(fruit) {
    //   return data.map(function(d) {
    //     return {x: parse(d.year), y: +d[fruit]};
    //   });
    // }));

    var dataset = d3.layout.stack()(["dem", "rep"].map(function(party){
        return data.map(function(d, index){
            return {x: d["district"], y: +d[party][1], z:d[party][0], district: d["district"], state:d["state"]}
        })
    }));


    // Set x, y and colors
    // var x = d3.scale.ordinal()
    //   .domain(dataset[0].map(function(d, index) { return d.x; }))
    //   .rangeRoundBands([10, width-10], 0.02);

    var x = d3.scale.ordinal()
    .domain(dataset[0].map(function(d, index) { return d.district; }))
    .rangeRoundBands([10, width-10], 0.02);

    var y = d3.scale.linear()
    .domain([0, d3.max(dataset, function(d) {  return d3.max(d, function(d) { return d.y0 + d.y; });  })])
    .range([height, 0]);

    var colors = ["0015BC", "E9141D", "FFFFFF"];


    // Define and draw axes
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(5)
    .tickSize(-width, 0, 0)
    .tickFormat( function(d) { return d } );

    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    //   .tickFormat(d3.time.format("%Y"));

    svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

    svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

    svg.append("text")
    .attr("transform", "translate(" + (width / 2) + " ," + (height + margin.bottom) + ")")
    .style("text-anchor", "middle")
    .text("District");

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Percentage");

    // Create groups for each series, rects for each segment 
    var groups = svg.selectAll("g.cost")
    .data(dataset)
    .enter().append("g")
    .attr("class", "cost")
    .style("fill", function(d, i) { return colors[i]; });

    function mouseOver(d){
        console.log("over",d);
        // alert(d);
        d3.select("#tooltip").transition().duration(200).style("opacity", .9);      

        d3.select("#tooltip").html("<h4>"+d.z+"</h4>"
            +"<h3> Probability of winning: "+d.y+"</h3>")  
            .style("left", (d3.event.pageX) + "px")     
            .style("top", (d3.event.pageY - 28) + "px");
    }

    function mouseOut(){
        d3.select("#tooltip").transition().duration(500).style("opacity", 0);      
    }

    function click(d){
        var area = d3.select("#linesvg").html("<h2>Past Predictions: District "+d.district+"</h2>");
        // .text("<h2>"+History+"</h2>");
        var linesvg = area.append("svg")
            .attr("width", 2*(width) + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

        var relevantTimedata = timedata.filter((entry) => entry['state']==d.state && entry['district'] ==d.district);
        var parse = d3.time.format("%Y-%m-%d").parse
        var a = relevantTimedata.map(entry => times.map(function(date){
            return {x: date, y: parseFloat(entry[date]), party: entry["party"], name: entry["person"]};
        }))
        var b = relevantTimedata.flatMap(entry => times.map(function(date){
            return {x: date, y: parseFloat(entry[date]), party: entry["party"], name: entry["person"]};
        }))
        console.log(b)

        var x = d3.scale.ordinal()
            .domain(a[0].map(function(d) { return d.x; }))
            .rangeRoundBands([10, 2*(width)-10], 0.02);
        
        var y = d3.scale.linear()
        .domain([0, 1])
        .range([height, 0]);
        
        console.log(a);
        var dem = a.filter(d => d[0].party=="dem")
        console.log(dem);
        var rep = a.filter(d => d[0].party== "rep")
        
        rep.forEach(time => time.forEach(d => d.y = 1-d.y))
        console.log(rep);
        var colors = {"dem":"#0015BC", "rep": "#E9141D", "others": "#FFFFFF"};
    
        // Define and draw axes
        var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(5)
        .tickSize(-2*width, 0, 0)
        .tickFormat( function(d) { return d } );
    
        var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom");
        //   .tickFormat(d3.time.format("%Y"));
    
        linesvg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
    
        linesvg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);
        
        // linesvg.append("g")
        //     .attr("transform", "translate(0," + height + ")")
        //     // .orient("bottom")
        //     // .call(xAxis)
        //     .call(d3.axisBottom(x));
        // var y = d3.scaleLinear()
        //     .domain([0, d3.max(a, function(d) { return +d.y; })])
        //     .range([ height, 0 ]);
        // linesvg.append("g")
        //     .orient("left")
        //     .call(yAxis)
            // .call(d3.axisLeft(y));

        // // Add the line
        // var linegraph = d3.svg.line()
        //     .x(function(d) {return x.rangeBand()/2 + x(d.x)})
        //     .y(function(d) {return y(d.y)});

        // console.log(a);
        // a.forEach(d => 
        //     linesvg.append("path")
        //     .attr("fill", "none")
        //     .attr("stroke", function () {return colors[d.party]})
        //     .attr("stroke-width", 1.5)
        //     .attr("d", linegraph(d.values)));
            // d3.svg.line()
            //     .x(function() { return x.rangeBand()/2 + x(candidate.x) })
            //     .y(function() { return y(candidate.y) })
            //     ))
        linesvg.append("path")
            .data(dem)
            .attr("fill", "none")
            .attr("stroke", colors["dem"])
            .attr("stroke-width", 1.5)
            .attr("d", d3.svg.line()
                .x(function(d) { return x.rangeBand()/2 + x(d.x) })
                .y(function(d) { return y(d.y) })
                );
        linesvg.append("path")
        .data(rep)
        .attr("fill", "none")
        .attr("stroke", colors["rep"])
        .attr("stroke-width", 1.5)
        .attr("d", d3.svg.line()
            .x(function(d) { return x.rangeBand()/2 + x(d.x) })
            .y(function(d) { return y(d.y) })
            );
        var legend = linesvg.selectAll(".llegend")
        .data(["0015BC", "E9141D"])
        .enter().append("g")
        .attr("class", "llegend")
        .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
        
        legend.append("rect")
        .attr("x", 2*width - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", function(d, i) {return ["0015BC", "E9141D"].slice()[i];});
        
        legend.append("text")
        .attr("x", 2*width + 5)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "start")
        .text(function(d, i) { 
            switch (i) {
            case 0: return dem[0][0].name;
            case 1: return rep[0][0].name;
            }
        });
        
        var circles = a.map(d => {console.log(d); return {x: x.rangeBand()/2+ x(d[0].x), y: y(d.y)}});
        console.log(b)
        console.log(circles);
        linesvg.selectAll(".dot")
            .data(b)
            .enter()
            .append("circle") // Uses the enter().append() method
            .attr("class", "dot") // Assign a class for styling
            .attr("cx", function(d,i) { return x.rangeBand()/2 + x(d.x) })
            .attr("cy", function(d,i) { return y(d.y) })
            .attr("r", 5); 

        console.log(rep);
        linesvg.selectAll(".dot")
            .data(rep)
            .enter()
            .append("circle") // Uses the enter().append() method
            .attr("class", "dot") // Assign a class for styling
            .attr("cx", function(d,i) { console.log(d); return x.rangeBand()/2 + x(d[i].x) })
            .attr("cy", function(d,i) { return y(d[i].y) })
            .attr("r", 5); 
        
    }
    var rect = groups.selectAll("rect")
    .data(function(d) { return d; })
    .enter()
    .append("rect")
    .attr("x", function(d) { return x(d.x); })
    .attr("y", function(d) { return y(d.y0 + d.y); })
    .attr("name", function(d) {return d.z;})
    .attr("district", function(d) {return d.district})
    .attr("height", function(d) { return y(d.y0) - y(d.y0 + d.y); })
    .attr("width", x.rangeBand())
    .attr("state", function(d){return d.state})
    .on("mouseover", (d) => mouseOver(d) )
    .on("mouseout", mouseOut )
    .on("mousemove", function(d){
        // var xPosition = d3.mouse(this)[0]-15;
        // var yPosition = d3.mouse(this)[1]-25;
        d3.select("#tooltip").style("left", (d3.event.pageX) + "px")     
        .style("top", (d3.event.pageY - 28) + "px");
        // .attr("transform", "translate(" + xPosition + "," + yPosition + ")");
    })
    .on("click", click);
    // .on("mouseover", function() { tooltip.style("display", null); })
    // .on("mouseout", function() { tooltip.style("display", "none"); })
    // .on("mousemove", function(d) {
    //     var xPosition = d3.mouse(this)[0] - 15;
    //     var yPosition = d3.mouse(this)[1] - 25;
    //     tooltip.attr("transform", "translate(" + xPosition + "," + yPosition + ")");
    //     tooltip.html("<h4>"+d.z+"<h4>")
    //     // tooltip.select("text").text(d.z);
    // });

    // d3.selectAll(".data").on("mouseover", mouseOver )
    //     .on("mouseout", mouseOut )
    //     .on("click", alert("clicked"));
    // Draw legend
    var legend = svg.selectAll(".legend")
    .data(colors)
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) { return "translate(30," + i * 19 + ")"; });
    
    legend.append("rect")
    .attr("x", width - 18)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", function(d, i) {return colors.slice()[i];});
    
    legend.append("text")
    .attr("x", width + 5)
    .attr("y", 9)
    .attr("dy", ".35em")
    .style("text-anchor", "start")
    .text(function(d, i) { 
        switch (i) {
        case 0: return "Democrats";
        case 1: return "Republicans";
        }
    });


    // Prep the tooltip bits, initial display is hidden
    var tooltip = svg.append("g")
    .attr("class", "tooltip")
    .style("display", "none");
        
    // tooltip.append("rect")
    // .attr("width", 150)
    // .attr("height", 20)
    // .attr("fill", "white")
    // .style("opacity", 0.5);

    // tooltip.append("text")
    // .attr("x", 75)
    // .attr("dy", "1.2em")
    // .style("text-anchor", "middle")
    // .attr("font-size", "12px")
    // .attr("font-weight", "bold");
}
this.charts = charts;})();