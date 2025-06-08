select 
    id,
    code,
    name,
    description
from {{ ref('transaction_types_intermediate') }} 