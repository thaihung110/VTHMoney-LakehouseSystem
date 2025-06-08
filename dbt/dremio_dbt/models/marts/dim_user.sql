select 
    user_id as id,
    full_name,
    email,
    phone_number,
    gender,
    status,
    created_at
from {{ ref('users_intermediate') }} 