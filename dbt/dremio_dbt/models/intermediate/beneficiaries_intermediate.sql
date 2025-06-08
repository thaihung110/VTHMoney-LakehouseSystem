select 
    b.id as beneficiary_id,
    b.user_id,
    u.full_name as user_full_name,
    b.beneficiary_name,
    b.beneficiary_phone,
    b.beneficiary_bank_code,
    b.beneficiary_bank_account,
    b.beneficiary_bank_branch,
    b.is_favorite,
    b.created_at,
    b.updated_at
from lakehouse."staging.db"."beneficiaries_iceberg".data b
left join lakehouse."staging.db"."users_iceberg".data u on b.user_id = u.id