========
Contents
========

{% for filepath, cube_strs, warnings, exceptions in content %}
{{ filepath }}
{{ "-" * filepath | string | length }}

{% for cube_str in cube_strs %}
.. code-block::

{{ cube_str | indent(first=True) }}
{% endfor %}

{% for warning_str in warnings %}
{{ warning_str }}
{% endfor %}

{% for exception_str in exceptions %}
{{ exception_str }}
{% endfor %}
{% endfor %}