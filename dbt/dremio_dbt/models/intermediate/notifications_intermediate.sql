select 
    n.id as notification_id,
    n.user_id,
    u.full_name as user_full_name,
    n.transaction_id,
    t.description as transaction_description,
    n.title,
    n.message,
    n.is_read,
    n.created_at
from lakehouse."staging.db"."notifications_iceberg".data n
left join lakehouse."staging.db"."users_iceberg".data u on n.user_id = u.id
left join lakehouse."staging.db"."transactions_iceberg".data t on n.transaction_id = t.id 