select distinct
    cast(date_trunc('day', created_at) as date) as date_day
from lakehouse.intermediate."transactions_intermediate"