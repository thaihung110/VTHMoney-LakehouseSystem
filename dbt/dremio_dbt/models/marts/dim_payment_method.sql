select 
    id,
    code,
    name,
    description
from {{ ref('payment_methods_intermediate') }} 