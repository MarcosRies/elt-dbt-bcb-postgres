SELECT DISTINCT 
    codigo_serie, 
    CASE WHEN codigo_serie = 11 THEN 'Selic' ELSE 'Desconhecida' END AS nome_serie
FROM {{ ref('stg_bcb__selic') }}
