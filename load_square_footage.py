import os
import csv
from itertools import islice
import glob
from pathlib import Path
import pdb

CSV_ROOT = Path(Path.home(), 'king-county-assessor')

years = glob.glob(str(CSV_ROOT / '*'))

data_files = {}


def calculate_stats(rows, key):
    values = sorted([
        int(row[key])
        for row in rows
    ])

    count = len(values)
    median = values[int(count / 2)]
    total = sum(values)

    return {
        'total': total,
        'median': median,
        'count': count,
        'average': total / count,
    }


def calculate_stats_for_complex(rows, unit_count_key, average_unit_size_key):
    unit_count_and_size = sorted([
        (
            int(row[unit_count_key]),
            int(row[average_unit_size_key])
        )
        for row in rows
    ])

    total_livable_square_footage = sum(
        unit_count * unit_size
        for unit_count, unit_size in unit_count_and_size
    )

    total_unit_count = sum(
        unit_count
        for unit_count, unit_size in unit_count_and_size
    )

    average_livable_square_footage = total_livable_square_footage / total_unit_count

    return {
        'total': total_livable_square_footage,
        'median': 'N/A',
        'count': total_unit_count,
        'average': average_livable_square_footage,
    }


# note that year is really the yyyy-mm-dd when it was fetched
for year in years:
    yyyy_mm_dd = os.path.basename(year)
    data_files[yyyy_mm_dd] = {}

    for filename, stats_function, args in (
            ('EXTR_ResBldg.csv', calculate_stats, ('SqFtTotLiving',)),
            ('EXTR_CondoUnit2.csv', calculate_stats, ('Footage',)),
            ('EXTR_AptComplex.csv', calculate_stats_for_complex, ('NbrUnits', 'AvgUnitSize')),
            ('EXTR_CondoComplex.csv', calculate_stats_for_complex, ('NbrUnits', 'AvgUnitSize')),
    ):
        path = str(CSV_ROOT / year / filename)
        data_files[yyyy_mm_dd][filename] = {}

        with open(path) as f:
            all_rows = csv.DictReader(f)
            # all_rows = list(islice(csv.DictReader(f), 100)) # uncomment to quickly test on a small subset of the data

            data_files[yyyy_mm_dd][filename]['livable_square_footage'] = stats_function(all_rows, * args)

print(data_files)

pdb.set_trace()

# It's not well documented, but 'SqFtTotLiving' appears to be the main key.
# There doesn't appear to be a "total square footage" key.
# SqFtTotBasement appears to include SqFtFinBasement (Total basement square feet > finished basement square feet)
# * it's unclear if SqFtTotLiving includes SqFtFinBasement
# all of the keys other than 'SqFtTotLiving' are frequently 0

sq_ft_keys = ('SqFt1stFloor', 'SqFtHalfFloor', 'SqFt2ndFloor', 'SqFtUpperFloor', 'SqFtUnfinFull', 'SqFtUnfinHalf', 'SqFtTotLiving', 'SqFtTotBasement', 'SqFtFinBasement', 'SqFtGarageBasement', 'SqFtGarageAttached', 'SqFtOpenPorch', 'SqFtEnclosedPorch', 'SqFtDeck')

