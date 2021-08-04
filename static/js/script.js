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

$(document).ready(function(){
    $('#searchBtn').click(function(e){
        e.preventDefault();
        giveOutput("", "");
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
            },
        });
    })
});