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
});