function plotData($title, $increased, $decreased) {

var chart = new CanvasJS.Chart("chartContainer", {
	animationEnabled: true,
	zoomEnabled: true,
	theme: "light2", // "light1", "light2", "dark1", "dark2"
	exportEnabled: true,
	title:{
		text: $title
	},
	axisX: {
	    interval: 1,
		valueFormatString: "DD-MM-YYYY"
	},
	axisY: {
		prefix: "$",
		title: "Price (in USD)"
	},
	toolTip: {
		shared: true
	},
	legend: {
		cursor: "pointer",
		itemclick: toogleDataSeries
	},
	data: [{
		type: "candlestick",
		risingColor: "green",
		legendMarkerColor: "green",
		showInLegend: true,
		name: "Rise",
		yValueFormatString: "$###0.00",
		xValueFormatString: "DD MMM YYYY",
		dataPoints: $increased
	},
	{
		type: "candlestick",
		fallingColor: "red",
		legendMarkerColor: "red",
		showInLegend: true,
		name: "Fall",
		yValueFormatString: "$###0.00",
		xValueFormatString: "DD MMM YYYY",
		dataPoints: $decreased
	}]
});
changeBorderColor(chart);
chart.render();

function toogleDataSeries(e) {
	if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
		e.dataSeries.visible = false;
	} else {
		e.dataSeries.visible = true;
	}
	e.chart.render();
}

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

function giveError($error){
    $('#chartContainer').empty();
    $('#chartContainer').append($error);
}

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

$(document).ready(function(){
    $today = new Date();
    $('#endDate').val($today.toISOString().substr(0, 10));
    $('#searchBtn').click(function(e){
        e.preventDefault();
        giveError("");
        loader(true);
        $.ajax({
            url: "/getPlot",
            type: "POST",
            data: $('#codeForm').serialize(),
            success: function(response){
                if(response["error"] != null){
                    giveError(response["error"]);
                }
                else{
                    $inc__ = response["data"][0];
                    $dec__ = response["data"][1];
                    $incData__ = [];
                    $decData__ = [];
                    $.each($inc__ , function (index, value){
                      $incData__[index] = {"x": new Date(value["x"][0], value["x"][1] - 1, value["x"][2]),
                                        "y": value["y"]};
                    });
                    $.each($dec__ , function (index, value){
                      $decData__[index] = {"x": new Date(value["x"][0], value["x"][1] - 1, value["x"][2]),
                                        "y": value["y"]};
                    });
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