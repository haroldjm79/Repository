
    
    

select
    name as unique_field,
    count(*) as n_records

from storage.dfb.dim_dfb_nfl_data
where name is not null
group by name
having count(*) > 1


