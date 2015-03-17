{% for host in hostvars %}
Host: {{ host }}
{% for hostarg in host %}
{{ hostarg }}
{% endfor %}
{% endfor %}
