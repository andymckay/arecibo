$(document).ready(function(){
    $('table.listing tbody tr').each(function() {
        var href = $(this).find("a").attr("href");
        if (href) {
            $(this).find("td").bind("click", function() {
                window.location = href;
                return false;
            });
        };
    });
    $("pre").each(function() {
        $(this).before('<a href="" class="unwrap">Unwrap</a><br />');
    });
    $(".unwrap").live("click", function() {
        $(this).parent().find("pre").addClass("wrapped");
        $(this).removeClass().addClass("wrap").text("Wrap");
        return false;
    });
    $(".wrap").live("click", function() {
        $(this).parent().find("pre").removeClass();
        $(this).removeClass().addClass("unwrap").text("Unwrap");
        return false;
    })
    $("input.date").dateinput({
        format: "mm/dd/yyyy"
    });
    var delay = 60000; // one minute
    function reload() {
        $.ajax({
            url: "/list/snippet/" + window.location.search, 
            dataType: "json",
            success: function(data) {
                $("#list-snippet").html(data.html);                
                if (data.count > 0) {
                    $("#listing-list").show();
                    $("#listing-error").hide();
                };
                var date = new Date();
                function pad(n){return n<10 ? '0'+n : n}
                $("#refresh-count").html('<p>Updated at: ' + pad(date.getHours()) + ':' + pad(date.getMinutes()) + '.</p>');
                setTimeout(reload, delay);
            },
            error: function() {
                $("#refresh-count").html('<p class="warning">An error occured.</p>');
                time = null;
            }
        });
    };   
    if ($("#list-snippet")) {
        setTimeout(reload, delay);
    };
});