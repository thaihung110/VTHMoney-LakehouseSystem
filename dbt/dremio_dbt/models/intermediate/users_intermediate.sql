with user_base as (
    select 
        id as user_id,
        phone_number,
        email,
        full_name,
        date_of_birth,
        gender,
        status,
        password_hash,
        created_at,
        updated_at
    from lakehouse."staging.db"."users_iceberg".data
),
wallet_agg as (
    select 
        user_id, 
        count(*) as total_wallets,
        sum(balance) as total_balance
    from lakehouse."staging.db"."wallets_iceberg".data
    group by user_id
),
transaction_agg as (
    select 
        user_id,
        count(*) as total_transactions
    from (
        select sender_id as user_id from lakehouse."staging.db"."transactions_iceberg".data
        union all
        select receiver_id as user_id from lakehouse."staging.db"."transactions_iceberg".data
    ) t
    group by user_id
)
select 
    u.*, 
    coalesce(w.total_wallets, 0) as total_wallets,
    coalesce(w.total_balance, 0) as total_balance,
    coalesce(t.total_transactions, 0) as total_transactions
from user_base u
left join wallet_agg w on u.user_id = w.user_id
left join transaction_agg t on u.user_id = t.user_id 