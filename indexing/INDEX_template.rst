========
Contents
========

{%  for prefix, data in content.items()%}

.. container:: toggle

    .. container:: header

        {{ prefix }}

    {% for filepath, cube_strs, warnings, exceptions in data %}
    **{{ filepath }}**

    {% for cube_str in cube_strs %}
    .. code-block::

        {{ cube_str | indent(width=8, first=False) }}
    {% endfor %}

    {% for warning_str in warnings %}
    {{ warning_str }}
    {% endfor %}

    {% for exception_str in exceptions %}
    {{ exception_str }}
    {% endfor %}
    {% endfor %}
{% endfor %}