select 
    u.user_id,
    u.full_name,
    u.total_wallets,
    u.total_balance,
    u.total_transactions,
    coalesce(b.total_beneficiaries, 0) as total_beneficiaries
from {{ ref('users_intermediate') }} u
left join (
    select user_id, count(*) as total_beneficiaries
    from lakehouse."staging.db"."beneficiaries_iceberg".data
    group by user_id
) b on u.user_id = b.user_id