with source as (

    {#-
    Normally we would select from the table here, but we are using seeds to load
    our data in this project
    #}
    select * from {{ ref('src_dfb_nfl_data') }}

)

    select *
    from source

