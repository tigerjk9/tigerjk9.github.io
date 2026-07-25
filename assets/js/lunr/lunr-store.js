---
layout: none
---

{%- comment -%}
  검색 인덱스 스토어.
  포스트는 site.posts 순서(최신순)로 순회하며 홈 리스트와 동일한 넘버링(seq = 전체수 - index)과
  날짜를 함께 담는다 → 검색 결과를 홈 리스트와 같은 에디토리얼 카드로 렌더할 수 있다.
  강의자료(lectures)·페이지는 seq 없이(0) 색인만 한다.
  배열 리터럴 끝의 트레일링 콤마는 JS에서 유효하므로 콤마 처리를 단순화한다.
{%- endcomment -%}
{%- assign total_posts = site.posts | size -%}
var store = [
  {%- for doc in site.posts -%}
    {%- unless doc.search == false -%}
  {
    "title": {{ doc.title | jsonify }},
    "excerpt":
      {%- if site.search_full_content == true -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | jsonify }},
      {%- else -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | truncatewords: 50 | jsonify }},
      {%- endif -%}
    "categories": {{ doc.categories | jsonify }},
    "tags": {{ doc.tags | jsonify }},
    "url": {{ doc.url | relative_url | jsonify }},
    "date": {{ doc.date | date: "%Y.%m.%d" | jsonify }},
    "seq": {{ total_posts | minus: forloop.index0 }}
  },
    {%- endunless -%}
  {%- endfor -%}
  {%- for doc in site.lectures -%}
    {%- unless doc.search == false -%}
  {
    "title": {{ doc.title | jsonify }},
    "excerpt":
      {%- if site.search_full_content == true -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | jsonify }},
      {%- else -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | truncatewords: 50 | jsonify }},
      {%- endif -%}
    "categories": {{ doc.categories | jsonify }},
    "tags": {{ doc.tags | jsonify }},
    "url": {{ doc.url | relative_url | jsonify }},
    "date": "",
    "seq": 0
  },
    {%- endunless -%}
  {%- endfor -%}
  {%- if site.lunr.search_within_pages -%}
  {%- assign pages = site.pages | where_exp: 'doc', 'doc.search != false' | where_exp: 'doc', 'doc.title != null' -%}
  {%- for doc in pages -%}
  {
    "title": {{ doc.title | jsonify }},
    "excerpt":
      {%- if site.search_full_content == true -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | jsonify }},
      {%- else -%}
        {{ doc.content | newline_to_br |
          replace:"<br />", " " |
          replace:"</p>", " " |
          replace:"</h1>", " " |
          replace:"</h2>", " " |
          replace:"</h3>", " " |
          replace:"</h4>", " " |
          replace:"</h5>", " " |
          replace:"</h6>", " "|
        strip_html | strip_newlines | truncatewords: 50 | jsonify }},
      {%- endif -%}
    "url": {{ doc.url | absolute_url | jsonify }},
    "date": "",
    "seq": 0
  },
  {%- endfor -%}
  {%- endif -%}
]
