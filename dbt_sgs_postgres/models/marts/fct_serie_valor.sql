{{ config(materialized='incremental', unique_key=['codigo_serie', 'data_referencia']) }}

SELECT
    codigo_serie,
    data_referencia,
    valor
FROM {{ ref('stg_bcb__selic') }}
{% if is_incremental() %}
WHERE data_referencia > (SELECT MAX(data_referencia) FROM {{ this }})
{% endif %}