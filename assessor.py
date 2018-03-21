import os
import csv
from itertools import islice
import glob
from pathlib import Path
import pdb

CSV_ROOT = Path(Path.home(), 'king-county-assessor')

years = glob.glob(str(CSV_ROOT / '*'))

data_files = {}

# note that year is really the yyyy-mm-dd when it was fetched
for year in years:
    data_files[os.path.basename(year)] = {}

    csvs = glob.glob(str(CSV_ROOT / year / '*.csv'))

    for filename in csvs:
        with open(filename) as f:
            rows = csv.DictReader(f)
            head = list(islice(rows, 100))

        basename = os.path.basename(filename)
        data_files[os.path.basename(year)][basename] = head

sq_ft_keys = ('SqFt1stFloor', 'SqFtHalfFloor', 'SqFt2ndFloor', 'SqFtUpperFloor', 'SqFtUnfinFull', 'SqFtUnfinHalf', 'SqFtTotLiving', 'SqFtTotBasement', 'SqFtFinBasement', 'SqFtGarageBasement', 'SqFtGarageAttached', 'SqFtOpenPorch', 'SqFtEnclosedPorch', 'SqFtDeck')

for building in data_files['2016-12-30']['EXTR_ResBldg.csv']:
    for key in sq_ft_keys:
        print(building['Address'], key, building[key])

import pdb
pdb.set_trace()
