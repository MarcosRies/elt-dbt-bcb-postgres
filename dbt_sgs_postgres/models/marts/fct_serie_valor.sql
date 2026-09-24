SELECT
    codigo_serie,
    data_referencia,
    valor
FROM {{ ref('stg_bcb__selic') }}