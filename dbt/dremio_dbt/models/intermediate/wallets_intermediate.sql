with wallet_base as (
    select 
        id as wallet_id,
        user_id,
        balance,
        currency,
        status,
        created_at,
        updated_at
    from lakehouse."staging.db"."wallets_iceberg".data
),
transaction_agg as (
    select 
        wallet_id,
        count(*) as total_transactions
    from (
        select sender_wallet_id as wallet_id from lakehouse."staging.db"."transactions_iceberg".data
        union all
        select receiver_wallet_id as wallet_id from lakehouse."staging.db"."transactions_iceberg".data
    ) t
    group by wallet_id
)
select 
    w.*, 
    u.full_name as user_full_name,
    coalesce(t.total_transactions, 0) as total_transactions
from wallet_base w
left join lakehouse."staging.db"."users_iceberg".data u on w.user_id = u.id
left join transaction_agg t on w.wallet_id = t.wallet_id