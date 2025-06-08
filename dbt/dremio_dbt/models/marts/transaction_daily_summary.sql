select 
    f.transaction_date,
    f.transaction_type_id,
    tt.name as transaction_type_name,
    f.payment_method_id,
    pm.name as payment_method_name,
    f.status,
    count(*) as total_transactions,
    sum(f.amount) as total_amount,
    sum(f.fee_amount) as total_fee
from {{ ref('fact_transactions') }} f
left join {{ ref('dim_transaction_type') }} tt on f.transaction_type_id = tt.id
left join {{ ref('dim_payment_method') }} pm on f.payment_method_id = pm.id
group by f.transaction_date, f.transaction_type_id, tt.name, f.payment_method_id, pm.name, f.status 