function giveOutput($error, $data){
    $('#graph').empty();
    if ($error != null){
        $('#graph').append($error);
    }
    else{
        $script = $data[0];
        $html = $data[1];
        $('#graph').append($html);
        $('#graph').append($script);
    }
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
        giveOutput("", "");
        loader(true);
        $.ajax({
            url: "/getPlot",
            type: "POST",
            data: $('#codeForm').serialize(),
            success: function(response){
                if(response["error"] != null){
                    giveOutput(response["error"], null);
                }
                else{
                    giveOutput(null, response["data"]);
                }
                loader(false);
            },
            error: function(){
                loader(false);
            }
        });
    })
});