select
  year_built,
  sum(unit_count) as yearly_unit_count,
  sum(square_footage) as yearly_square_footage,
  (sum(square_footage) / cast(sum(unit_count) as float)) as average_unit_size
from parcels_footage
where (
  date_retrieved = '2018-01-10'
) 
group by year_built
order by year_built;
