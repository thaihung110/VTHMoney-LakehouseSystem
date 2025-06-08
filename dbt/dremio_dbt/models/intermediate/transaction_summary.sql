select 
    t.transaction_type_name,
    t.payment_method_name,
    t.status,
    count(*) as total_count,
    sum(t.amount) as total_amount
from {{ ref('transactions_intermediate') }} t
group by t.transaction_type_name, t.payment_method_name, t.status