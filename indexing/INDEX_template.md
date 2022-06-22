{% for prefix, data in content.items() %}

<details>

  <summary>{{ prefix }}</summary>

  {% for filepath, link_path, items, is_png, warnings, exceptions in data|sort(attribute="path") %}
  #### [{{ filepath }}]({{ link_path }})

  {% if is_png %}
  ![{{ link_path }}]({{ link_path }})
  {% else %}
  {% for item in items %}
  ```
      {{ item | indent(first=False) }}
  ```
  {% endfor %}
  {% endif %}
  {%if warnings %}
  ```
  {% for warning_str in warnings %}
  {{ warning_str }}
  {% endfor %}
  ```
  {% endif %}
  {% if exceptions%}
  ```
  {% for exception_str in exceptions %}
  {{ exception_str }}
  {% endfor %}
  ```
  {% endif %}
{% endfor %}
</details>

{% endfor %}