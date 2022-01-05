{%  for prefix, data in content.items()%}

<details>

  <summary>{{ prefix }}</summary>

  {% for filepath, cube_strs, warnings, exceptions in data %}
  # {{ filepath }}
  [Link]({{ filepath }})

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