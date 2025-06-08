with tx as (
    select 
        t.transaction_id as id,
        t.transaction_type_id,
        t.payment_method_id,
        t.sender_wallet_id,
        sw.user_id as sender_user_id,
        t.receiver_wallet_id,
        rw.user_id as receiver_user_id,
        t.amount,
        t.currency,
        t.fee_amount,
        t.status,
        t.description,
        t.reference_number,
        t.created_at,
        t.updated_at,
        cast(date_trunc('day', t.created_at) as date) as transaction_date
    from {{ ref('transactions_intermediate') }} t
    left join {{ ref('wallets_intermediate') }} sw on t.sender_wallet_id = sw.wallet_id
    left join {{ ref('wallets_intermediate') }} rw on t.receiver_wallet_id = rw.wallet_id
)
select * from tx