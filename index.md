---
layout: page
title: Home
---

# Hi, I'm Lina!

I'm Lina L. Faller, a computational biologist passionate about data democratization and biotech innovation.

## Recent Posts
{% for post in site.posts limit: 3 %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%B %d, %Y" }}
{% endfor %}

[About me](about) | [All posts](blog) | [Work With Me](services)