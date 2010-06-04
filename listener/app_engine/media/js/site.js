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
    $("input.date").dateinput({
        format: "mm/dd/yyyy"
    });
});