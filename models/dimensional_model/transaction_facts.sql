{% docs table_events %}

This table contains clickstream events from the marketing website.

The events in this table are recorded by Snowplow and piped into the warehouse on an hourly basis. The following pages of the marketing site are tracked:
 - /
 - /about
 - /team
 - /contact-us

{% enddocs %}

{{ config(
  materialized='table',
  file_format='delta'
) }}

SELECT
    userId as user_id,
    itemId as item_id,
    currency_id,
    provider_id,
    price,
    date
    -- providerId
-- FROM {{ source('silver_layer', 'transaction_silver') }} t LEFT JOIN {{ ref('currency_dimension') }} c on t.currency = c.currency
FROM {{ source('silver_layer', 'transaction_silver') }}, {{ ref('currency_dimension') }}, {{ ref('transaction_provider_dimension') }}
