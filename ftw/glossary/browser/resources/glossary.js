// Escape strings to be used in regexps.
RegExp.escape = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
};
// Define our own highlight function because the one from Plone doesn't work
// well with IE.
jQuery.fn.glossaryHighlight = function (str, className) {
    if (str) {
        var rstr = RegExp.escape(str);
        var regex = new RegExp("(>[^<]*)("+rstr+")([^>]*<)", "gi");
        return this.each(function () {
            this.innerHTML = this.innerHTML.replace(regex, function($1, $2, $3, $4) {
                // maybe we have additional matches to highlight in the first group ($2)
                $2 = $2.replace(new RegExp("("+rstr+")", "gi"), "<span class=\"" + className + "\">$1</span>");
                return $2 + "<span class=\"" + className + "\">" + $3+ "</span>" + $4;
            });
        });
    }
};

jQuery(document).ready(function($) {
    // Load search results with AJAX
    $('#glossaryform').submit(function(event) {
        event.preventDefault();
        var formdata = $(this).serializeArray();
        $.get('glossary_view/results', formdata, function(data) {
            $('#glossary-searchresults').html(data);
            var search_term = $('#glossaryform input[name="glossary-search-field"]').val().replace(/\*/g, '');
            $('#glossary-searchresults').glossaryHighlight(search_term, 'highlightedSearchTerm');
            $('input[name=glossary-search-field]').autocomplete("close");
            $('#glossaryform input[name="glossary-search-field"]').removeClass('textSelected');
        });
    });

    // Load index query results with AJAX
    $('a.glossary-index-links').click(function(event) {
        event.preventDefault();
        var formdata = $('#glossaryform').serializeArray();
        formdata.push({name: 'search_letter', value: $(this).text()});
        $.get('glossary_view/results', formdata, function(data) {
            $('#glossary-searchresults').html(data);
        });
    });

    // Autocomplete
    $('input[name=glossary-search-field]').autocomplete({
        source: function(req, callback) {
                var categories = $('#glossaryform input[name="categories:list"]:checked');
                var formData = [];
                formData.push({"name":"term", "value":req.term});
                for (var i = 0; i < categories.length; i++) {
                    formData.push({"name":"categories:list", "value":$(categories[i]).val()});
                }
                $.get('glossary_view/matching_terms', formData, callback); },
        select: function(event, ui) {
                $('#glossaryform input[name="glossary-search-field"]').val(ui.item.value);
                $('#glossaryform').submit(); }
    });

    // Select all text when clicking inside search input field
    $('#glossaryform input[name="glossary-search-field"]').click(function(event) {
        if ($(this).hasClass('textSelected')) $(this).removeClass('textSelected');
        else $(this).focus().select().addClass('textSelected');
    });
});
