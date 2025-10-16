---
layout: page
title: Blog
permalink: /blog
---

# Blog

Thoughts on data democratization, software engineering, and biotech innovation.

---

{% assign categories_list = "data-science,software-engineering,career-development,data-engineering,research,biotech,project-management" | split: "," %}

{% for category in categories_list %}
  {% assign category_posts = site.posts | where_exp: "post", "post.categories contains category" %}
  {% if category_posts.size > 0 %}

## {{ category | replace: "-", " " | capitalize }} ({{ category_posts.size }})

{% for post in category_posts %}
- **[{{ post.title }}]({{ post.url }})** - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

---

  {% endif %}
{% endfor %}