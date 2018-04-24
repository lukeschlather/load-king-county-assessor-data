with yearly_counts as (
  select
    year_built,
    sum(unit_count) as yearly_unit_count,
    sum(square_footage) as yearly_square_footage,
    (sum(square_footage) / cast(sum(unit_count) as float)) as average_unit_size
  from parcels_view
  where (
    date_retrieved = '2018-01-10'
  ) 
  group by year_built
  order by year_built
)

select
  year_built,
  yearly_unit_count,
  yearly_square_footage,
  average_unit_size,
  king_county as population
from yearly_counts
left join population on year_built = population.year;
