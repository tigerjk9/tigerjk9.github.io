---
layout: none
---

var idx = lunr(function () {
  this.field('title')
  this.field('excerpt')
  this.field('categories')
  this.field('tags')
  this.ref('id')

  this.pipeline.remove(lunr.trimmer)

  for (var item in store) {
    this.add({
      title: store[item].title,
      excerpt: store[item].excerpt,
      categories: store[item].categories,
      tags: store[item].tags,
      id: item
    })
  }
});

$(document).ready(function() {
  $('input#search').on('keyup', function () {
    var resultdiv = $('#results');
    var query = $(this).val().toLowerCase();
    var result =
      idx.query(function (q) {
        query.split(lunr.tokenizer.separator).forEach(function (term) {
          q.term(term, { boost: 100 })
          if(query.lastIndexOf(" ") != query.length-1){
            q.term(term, {  usePipeline: false, wildcard: lunr.Query.wildcard.TRAILING, boost: 10 })
          }
          if (term != ""){
            q.term(term, {  usePipeline: false, editDistance: 1, boost: 1 })
          }
        })
      });
    resultdiv.empty();
    resultdiv.prepend('<p class="results__found">'+result.length+' {{ site.data.ui-text[site.locale].results_found | default: "Result(s) found" }}</p>');

    function esc(s) {
      return String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
    function pad3(n) { return n > 999 ? String(n) : ('000' + n).slice(-3); }

    var listHtml = '';
    for (var item in result) {
      var ref = result[item].ref;
      var doc = store[ref];

      var seqHtml = doc.seq > 0
        ? '<span class="entry-seq" aria-hidden="true">' + pad3(doc.seq) + '</span>'
        : '<span class="entry-seq entry-seq--empty" aria-hidden="true"></span>';

      var cat = (doc.categories && doc.categories.length) ? esc(doc.categories[0]) : '';
      var date = doc.date ? esc(doc.date) : '';
      var eyebrow = '';
      if (cat) { eyebrow += '<span class="entry-eyebrow__cat">' + cat + '</span>'; }
      if (date) { eyebrow += '<time class="entry-eyebrow__date">' + date + '</time>'; }
      var eyebrowHtml = eyebrow ? '<p class="entry-eyebrow">' + eyebrow + '</p>' : '';

      var tagsHtml = '';
      if (doc.tags && doc.tags.length) {
        var tagInner = '';
        for (var t = 0; t < Math.min(doc.tags.length, 4); t++) {
          tagInner += '<span class="entry-tags__tag">#' + esc(doc.tags[t]) + '</span>';
        }
        tagsHtml = '<p class="entry-tags">' + tagInner + '</p>';
      }

      var excerpt = esc(doc.excerpt.split(" ").splice(0, 26).join(" ")) + '...';

      listHtml +=
        '<div class="list__item">'+
          '<article class="archive__item" itemscope itemtype="https://schema.org/CreativeWork">'+
            seqHtml +
            '<div class="archive__item-body">'+
              eyebrowHtml +
              '<h2 class="archive__item-title no_toc" itemprop="headline">'+
                '<a href="'+doc.url+'" rel="permalink">'+esc(doc.title)+'</a>'+
              '</h2>'+
              '<p class="archive__item-excerpt" itemprop="description">'+excerpt+'</p>'+
              tagsHtml +
            '</div>'+
          '</article>'+
        '</div>';
    }
    resultdiv.append('<div class="entries-list recent-posts search-results">' + listHtml + '</div>');
  });
});
