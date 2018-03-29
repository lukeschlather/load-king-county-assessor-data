import os
import csv
from itertools import islice
import glob
from pathlib import Path
import pdb
import sqlite3

def main():
    CSV_ROOT = Path(Path.home(), 'king-county-assessor')
    DATABASE = str(Path(Path.home(), 'king-county-assessor.sqlite3'))

    retrieved_dates = glob.glob(str(CSV_ROOT / '*'))

    data_files = {}


    # note that year is really the yyyy-mm-dd when it was fetched
    with sqlite3.connect(DATABASE) as connection:
        create_premises_table = '''
          CREATE TABLE premises (
            multifamily BOOLEAN,
            unit_count INTEGER,
            square_footage INTEGER,
            source STRING,
            date_retrieved STRING,
            year_built INTEGER
          );
        '''
        connection.execute(create_premises_table)

        for retrieved_date in retrieved_dates:
            for filename, average_unit_size_key, unit_count_key in (
                    ('EXTR_ResBldg.csv', 'SqFtTotLiving', None),
                    ('EXTR_CondoUnit2.csv', 'Footage', None),
                    ('EXTR_AptComplex.csv', 'AvgUnitSize', 'NbrUnits'),
                    ('EXTR_CondoComplex.csv', 'AvgUnitSize', 'NbrUnits'),
            ):
                yyyy_mm_dd = os.path.basename(retrieved_date)
                file_path = os.path.join(retrieved_date, filename)
                with open(file_path) as f:
                    rows = csv.DictReader(f)
                    # rows = list(islice(csv.DictReader(f), 100)) # uncomment to quickly test on a small subset of the data
                    print('loading csv: ' + filename + '\n')
                    values = [
                        (
                            bool(unit_count_key),
                            int(row[unit_count_key]) if unit_count_key else 1,
                            int(row[average_unit_size_key]),
                            filename,
                            yyyy_mm_dd,
                            row['YrBuilt']
                        )
                        for row in rows
                    ]
                    print('finished importing csv. loading into database...')
                    connection.executemany(
                        '''
                        INSERT INTO premises
                          (multifamily, unit_count, square_footage, source, date_retrieved, year_built)
                        VALUES
                          (?,?,?,?,?,?)
                        ''',
                        values
                    )

    # It's not well documented, but 'SqFtTotLiving' appears to be the main key.
    # There doesn't appear to be a "total square footage" key.
    # SqFtTotBasement appears to include SqFtFinBasement (Total basement square feet > finished basement square feet)
    # * it's unclear if SqFtTotLiving includes SqFtFinBasement
    # all of the keys other than 'SqFtTotLiving' are frequently 0

    sq_ft_keys = ('SqFt1stFloor', 'SqFtHalfFloor', 'SqFt2ndFloor', 'SqFtUpperFloor', 'SqFtUnfinFull', 'SqFtUnfinHalf', 'SqFtTotLiving', 'SqFtTotBasement', 'SqFtFinBasement', 'SqFtGarageBasement', 'SqFtGarageAttached', 'SqFtOpenPorch', 'SqFtEnclosedPorch', 'SqFtDeck')
