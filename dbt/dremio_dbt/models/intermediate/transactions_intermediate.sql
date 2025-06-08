select 
    t.id as transaction_id,
    t.transaction_type_id,
    tt." name" as transaction_type_name,
    t.payment_method_id,
    pm." name" as payment_method_name,
    t.sender_wallet_id,
    sw.balance as sender_wallet_balance,
    sw.currency as sender_wallet_currency,
    sender_user.full_name as sender_user_name,
    t.receiver_wallet_id,
    rw.balance as receiver_wallet_balance,
    rw.currency as receiver_wallet_currency,
    receiver_user.full_name as receiver_user_name,
    t.amount,
    t.currency,
    t.fee_amount,
    t.status,
    t.description,
    t.reference_number,
    t.created_at,
    t.updated_at
from lakehouse."staging.db"."transactions_iceberg".data t
left join lakehouse."staging.db"."wallets_iceberg".data sw on t.sender_wallet_id = sw.id
left join lakehouse."staging.db"."users_iceberg".data sender_user on sw.user_id = sender_user.id
left join lakehouse."staging.db"."wallets_iceberg".data rw on t.receiver_wallet_id = rw.id
left join lakehouse."staging.db"."users_iceberg".data receiver_user on rw.user_id = receiver_user.id
left join lakehouse."staging.db"."payments_method".data pm on t.payment_method_id = pm."id"
left join lakehouse."staging.db"."transaction_types".data tt on t.transaction_type_id = tt."id"