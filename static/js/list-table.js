$(document).ready(function(){
    $(".toggle-favourite").click(function(){
        var button = $(this);
        button.addClass("loading");
        $.ajax({
            type: "POST",
            url: button.data("url"),
            headers: { "X-CSRFToken":  button.data("csrf") },
            dataType: "json",
            data: {
                coin_id: button.data("coin_id")
            },
            success: function(response){
                console.log(response);
                button.toggleClass("filled");
                button.removeClass("loading");
            },
            error: function(response){
                console.log(response);
                button.removeClass("loading");
            }
        });
    });
});