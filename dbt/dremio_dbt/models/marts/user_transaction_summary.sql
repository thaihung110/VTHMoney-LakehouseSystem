select 
    u.id as user_id,
    u.full_name,
    f.status,
    count(*) as total_transactions,
    sum(f.amount) as total_amount
from {{ ref('fact_transactions') }} f
left join {{ ref('dim_user') }} u on f.sender_user_id = u.id or f.receiver_user_id = u.id
group by u.id, u.full_name, f.status 