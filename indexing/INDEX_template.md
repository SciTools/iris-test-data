{%  for prefix, data in content.items()%}

<details>

  <summary>{{ prefix }}</summary>

  {% for filepath, link_path, cube_strs, warnings, exceptions in data %}
  # [{{ filepath }}]({{ link_path }})

  {% for cube_str in cube_strs %}
  ```
      {{ cube_str | indent(first=False) }}
  ```
  {% endfor %}

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