select 
    wallet_id as id,
    user_id,
    currency,
    status,
    created_at
from lakehouse.intermediate."wallets_intermediate"