{% macro ppg_value(model) %}
SELECT
 *
FROM
 {{ model }}
WHERE
 PPG > 100
{% endmacro %}
