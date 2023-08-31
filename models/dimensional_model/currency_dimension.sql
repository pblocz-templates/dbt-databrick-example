{{ config(
  materialized='incremental',
  file_format='delta',
  unique_key='currency_id',
  incremental_strategy='merge',
  post_hook=[
        "OPTIMIZE {{ this }} ZORDER BY currency_id;",
        "ANALYZE TABLE {{ this }} COMPUTE STATISTICS FOR ALL COLUMNS;"
  ]
) }}

with currencies_dedup as (
    select
        currency,
        max(loadTime) as load_time
    from {{ source('silver_layer', 'transaction_silver') }}

    {% if is_incremental() %}
      where loadTime > (select max(load_time) from {{ this }})
    {% endif %}
    group by currency
)
select
     {{ dbt_utils.generate_surrogate_key(
      ['currency',]
    ) }} as currency_id,
    currency,
    load_time
from currencies_dedup