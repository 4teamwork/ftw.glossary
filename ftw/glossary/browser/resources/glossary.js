// Escape strings to be used in regexps.
RegExp.escape = function(text) {
    return text.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, "\\$&");
};
// Define our own highlight function because the one from Plone doesn't work
// well with IE.
jQuery.fn.glossaryHighlight = function (str, className) {
    var rstr = RegExp.escape(str);
    var regex = new RegExp("(>[^<]*)("+rstr+")([^>]*<)", "gi");
    return this.each(function () {
        this.innerHTML = this.innerHTML.replace(regex, function($1, $2, $3, $4) {
            // maybe we have additional matches to highlight in the first group ($2)
            $2 = $2.replace(new RegExp("("+rstr+")", "gi"), "<span class=\"" + className + "\">$1</span>");
            return $2 + "<span class=\"" + className + "\">" + $3+ "</span>" + $4;
        });
    });
};
jq(function() {
    // Load search results with AJAX
    jq('#glossaryform').submit(function(event) {
        event.preventDefault();
        var formdata = jq(this).serializeArray();
        jq.get('glossary_view/results', formdata, function(data) {
            jq('#glossary-searchresults').html(data);
            var search_term = jq('#glossaryform input[name="glossary-search-field"]').val().replace(/\*/g, '');
            jq('#glossary-searchresults').glossaryHighlight(search_term, 'highlightedSearchTerm');
            jq('input[name=glossary-search-field]').autocomplete("close");
            jq('#glossaryform input[name="glossary-search-field"]').removeClass('textSelected');
        });
    });

    // Load index query results with AJAX
    jq('a.glossary-index-links').click(function(event) {
        event.preventDefault();
        var formdata = jq('#glossaryform').serializeArray();
        formdata.push({name: 'search_letter', value: jq(this).text()});
        jq.get('glossary_view/results', formdata, function(data) {
            jq('#glossary-searchresults').html(data);
        });
    });

    // Autocomplete
    jq('input[name=glossary-search-field]').autocomplete({
        source: function(req, callback) {
                var categories = jq('#glossaryform input[name="categories:list"]:checked');
                var formData = new Array();
                formData.push({"name":"term", "value":req.term});
                for (var i = 0; i < categories.length; i++) {
                    formData.push({"name":"categories:list", "value":jq(categories[i]).val()});
                };
                jq.get('glossary_view/matching_terms', formData, callback); },
        select: function(event, ui) {
                jq('#glossaryform input[name="glossary-search-field"]').val(ui.item.value);
                jq('#glossaryform').submit(); }
    });

    // Select all text when clicking inside search input field
    jq('#glossaryform input[name="glossary-search-field"]').click(function(event) {
        if (jq(this).hasClass('textSelected')) jq(this).removeClass('textSelected');
        else jq(this).focus().select().addClass('textSelected');
    });
});
