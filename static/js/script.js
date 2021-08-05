// Function to plot chart by canvas js
function plotData($title, $increased, $decreased) {
    // Making Chart
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true, // Animation
        zoomEnabled: true, // Zoom Tool
        theme: "light2", // Theme
        exportEnabled: true,
        // Title
        title:{
            text: $title
        },
        // X-axis
        axisX: {
            interval: 1,
            valueFormatString: "DD-MM-YYYY"
        },
        // Y-axis
        axisY: {
            prefix: "$",
            title: "Price (in USD)"
        },
        // Hover tooltips
        toolTip: {
            shared: true
        },
        // Legends
        legend: {
            cursor: "pointer",
            itemclick: toogleDataSeries
        },
        // Data to plot
        data: [
            // Fall days
            {
                type: "candlestick",
                fallingColor: "red",
                legendMarkerColor: "red",
                showInLegend: true,
                name: "Fall",
                yValueFormatString: "$###0.00",
                xValueFormatString: "DD MMM YYYY",
                dataPoints: $decreased
            },
            // Rise days
            {
                type: "candlestick",
                risingColor: "green",
                legendMarkerColor: "green",
                showInLegend: true,
                name: "Rise",
                yValueFormatString: "$###0.00",
                xValueFormatString: "DD MMM YYYY",
                dataPoints: $increased
            }
        ]
    });

    // Calling Function for plotting
    changeBorderColor(chart);

    // Rendering Chart
    chart.render();

    // Function to toggle data when clicked on legends
    function toogleDataSeries(e) {
        if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
            e.dataSeries.visible = false;
        } else {
            e.dataSeries.visible = true;
        }
        e.chart.render();
    }

    // Function to give border color according to day status
    function changeBorderColor(chart){
        var dataSeries;
        for( var i = 0; i < chart.options.data.length; i++){
            dataSeries = chart.options.data[i];
          for(var j = 0; j < dataSeries.dataPoints.length; j++){
            dataSeries.dataPoints[j].color = (dataSeries.dataPoints[j].y[0] <= dataSeries.dataPoints[j].y[3]) ? (dataSeries.risingColor ? dataSeries.risingColor : dataSeries.color) : (dataSeries.fallingColor ? dataSeries.fallingColor : dataSeries.color);
          }
        }
    }
}

// Function to show error if any
function giveError($error){
    $('#chartContainer').empty();
    $('#chartContainer').append($error);
}

// Function to show spinner until data is being fetched
function loader($inp){
    if($inp){
        $('#searchBtn').hide();
        $('#loadBtn').show();
    }
    else{
        $('#loadBtn').hide();
        $('#searchBtn').show();
    }
}

// Starting Point
$(document).ready(function(){
    // Setting end date input to today
    $today = new Date();
    $('#endDate').val($today.toISOString().substr(0, 10));

    // Clicking search button
    $('#searchBtn').click(function(e){
        // Initializations
        e.preventDefault();
        giveError("");
        loader(true);

        // Sending request to fetch data
        $.ajax({
            url: "/getPlot",
            type: "POST",
            data: $('#codeForm').serialize(),
            success: function(response){
                if(response["error"] != null){
                    // If data cannot be fetched
                    giveError(response["error"]);
                }
                else{
                    // Getting response data
                    $inc__ = response["data"][0];
                    $dec__ = response["data"][1];
                    $incData__ = [];
                    $decData__ = [];

                    // Formatting fetched data to be usable
                    $.each($inc__ , function (index, value){
                      $incData__[index] = {"x": new Date(value["x"][0], value["x"][1] - 1, value["x"][2]),
                                        "y": value["y"]};
                    });
                    $.each($dec__ , function (index, value){
                      $decData__[index] = {"x": new Date(value["x"][0], value["x"][1] - 1, value["x"][2]),
                                        "y": value["y"]};
                    });

                    // Plotting data
                    plotData($('#companyCode').val(), $incData__, $decData__);
                }
                loader(false);
            },
            error: function(){
                loader(false);
            }
        });
    })
});