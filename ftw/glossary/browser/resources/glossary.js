jq(function() {
    // Load search results with AJAX
    jq('input[name=glossary-search-button]').click(function(event) {
        event.preventDefault();
        var formdata = jq('#glossaryform').serializeArray();
        jq.get('glossary_view/results', formdata, function(data) {
            jq('#glossary-searchresults').html(data);
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
    jq('input[name=glossary-search-field]').autocomplete(
        {source: function(req, callback){
              var categories = jq('#glossaryform input[name="categories:list"]:checked');
              var formData = new Array();
              formData.push({"name":"term", "value":req.term});
              for (var i = 0; i < categories.length; i++) {
                  formData.push({"name":"categories:list", "value":jq(categories[i]).val()});
              };
              jq.get('glossary_view/matching_terms', formData, callback);
        }
    });  
});
