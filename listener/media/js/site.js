$(document).ready(function(){
    function load(node) {
        if (history.pushState) {
            history.pushState({path:node.text()}, '', node.attr('href'));
        }
        $('.content-wrapper').load(node.attr('href') + ' .container:eq(2)', function() {
           // pass 
        });
        return false;
    };
    $('#list-snippet').each(function() {
        if ($(this).find("a").length) {
            $(this).find("td").bind("click", function() {
                return load($(this).closest('tr').find('a'));
            });
        };
    });
    $(window).bind('popstate', function() {
        $('.content-wrapper').load(location.pathname + ' .container:eq(2)');
    });
    $("pre").each(function() {
        $(this).before('<a href="" class="unwrap">Wrap</a><br />');
    });
    $(".unwrap").live("click", function() {
        $(this).parent().find("pre").addClass("wrapped");
        $(this).removeClass().addClass("wrap").text("Unwrap");
        return false;
    });
    $(".wrap").live("click", function() {
        $(this).parent().find("pre").removeClass();
        $(this).removeClass().addClass("unwrap").text("Wrap");
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
                $("#refresh-count").html('<p>Updated at: ' +
                    pad(date.getHours()) + ':' +
                    pad(date.getMinutes()) + '.</p>');
                setTimeout(reload, delay);
            },
            error: function() {
                $("#refresh-count").html('<p class="warning">An error occured.</p>');
                time = null;
            }
        });
    };
    if ($("#list-snippet") != null) {
        setTimeout(reload, delay);
    };
    if ($("form.issue")) {
        var title = $('#id_title');
        var desc = $('#id_description');
        desc.focus();
        function makeTitle() {
            var src = jQuery.trim(desc.val());
            if (src.length > 50) {
                title.val(substr(0, 50) + '...');
            } else {
                title.val(src);
            }
        };
        if (title.val() < 1) {
            desc.bind("keydown", makeTitle);
            title.bind("keydown", function() {
                desc.unbind("keydown", makeTitle);
            });
        };
    };
});
