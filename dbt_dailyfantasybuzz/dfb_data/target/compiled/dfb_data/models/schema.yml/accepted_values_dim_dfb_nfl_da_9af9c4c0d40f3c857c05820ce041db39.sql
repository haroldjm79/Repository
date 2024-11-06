
    
    

with all_values as (

    select
        position as value_field,
        count(*) as n_records

    from storage.dfb.dim_dfb_nfl_data
    group by position

)

select *
from all_values
where value_field not in (
    'TE/FLEX','QB','WR/FLEX','RB/FLEX','WR','TE','RB','DST'
)


