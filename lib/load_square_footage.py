import os
import csv
from itertools import islice
import glob
from pathlib import Path
import sqlite3


def main():
    CSV_ROOT = Path(Path.home(), 'king-county-assessor')
    DATABASE = str(Path(Path.home(), 'king-county-assessor.sqlite3'))

    retrieved_dates = glob.glob(str(CSV_ROOT / '*'))

    with sqlite3.connect(DATABASE) as connection:
        create_parcels_footage = '''
          CREATE TABLE parcels_footage (
            major INTEGER,
            minor INTEGER,
            multifamily BOOLEAN,
            unit_count INTEGER,
            square_footage INTEGER,
            source STRING,
            date_retrieved STRING,
            year_built INTEGER
          );
        '''
        connection.execute(create_parcels_footage)

        create_parcels = '''
          CREATE TABLE parcels (
            major INTEGER,
            minor INTEGER,
            date_retrieved STRING,
            current_zoning STRING,
            square_footage_lot INTEGER,
            district_name STRING
          );
        '''
        connection.execute(create_parcels)

        create_parcels_appraisal = '''
          CREATE TABLE parcels_appraisal (
            major INTEGER,
            minor INTEGER,
            appr_land_val INTEGER,
            apr_imps_val INTEGER,
            taxable_imps_val INTEGER,
            taxable_land_val INTEGER,
            date_retrieved INTEGER
          );
        '''
        connection.execute(create_parcels_appraisal)

        for retrieved_date in retrieved_dates:
            yyyy_mm_dd = os.path.basename(retrieved_date)

            for filename, average_unit_size_key, unit_count_key in (
                    ('EXTR_ResBldg.csv', 'SqFtTotLiving', None),
                    ('EXTR_CondoUnit2.csv', 'Footage', None),
                    ('EXTR_AptComplex.csv', 'AvgUnitSize', 'NbrUnits'),
                    # Removing this to simplify queries. Theoretically redundant to EXTR_CondoUnit2.csv
                    # ('EXTR_CondoComplex.csv', 'AvgUnitSize', 'NbrUnits'),
            ):
                file_path = os.path.join(retrieved_date, filename)
                with open(file_path, encoding='Windows-1252') as f:
                    rows = csv.DictReader(f)
                    # rows = list(islice(csv.DictReader(f), 100)) # uncomment to quickly test on a small subset of the data
                    print('loading csv: ' + filename + '\n')
                    values = [
                        (
                            row['Major'],
                            row.get('Minor') or 0,
                            bool(unit_count_key),
                            int(row[unit_count_key]) if unit_count_key else 1,
                            (
                                int(row[average_unit_size_key]) * int(row[unit_count_key])
                                if unit_count_key
                                else
                                int(row[average_unit_size_key])
                            ),
                            filename,
                            yyyy_mm_dd,
                            row['YrBuilt'],
                        )
                        for row in rows
                    ]
                    print('finished importing csv. loading into database...')
                    connection.executemany(
                        '''
                        INSERT INTO parcels_footage
                          (major, minor, multifamily, unit_count, square_footage, source, date_retrieved, year_built)
                        VALUES
                          (?,?,?,?,?,?,?,?)
                        ''',
                        values
                    )

            file_path = os.path.join(retrieved_date, 'EXTR_Parcel.csv')
            with open(file_path, encoding='Windows-1252') as f:
                rows = csv.DictReader(f)
                # rows = list(islice(csv.DictReader(f), 100)) # uncomment to quickly test on a small subset of the data
                print('loading csv: ' + file_path + '\n')
                values = [
                    (
                        row['Major'],
                        row['Minor'],
                        row['CurrentZoning'],
                        row['SqFtLot'],
                        row['DistrictName'],
                        yyyy_mm_dd,
                    )
                    for row in rows
                ]
                print('finished importing csv. loading into database...')
                connection.executemany(
                    '''
                    INSERT INTO parcels
                      (major, minor, current_zoning, square_footage_lot, district_name, date_retrieved)
                    VALUES
                      (?,?,?,?,?,?)
                    ''',
                    values
                )

            file_path = os.path.join(retrieved_date, 'EXTR_RPAcct_NoName.csv')
            with open(file_path, encoding='Windows-1252') as f:
                rows = csv.DictReader(f)
                # rows = list(islice(csv.DictReader(f), 100)) # uncomment to quickly test on a small subset of the data
                print('loading csv: ' + file_path + '\n')
                values = [
                    (
                        row['Major'],
                        row['Minor'],
                        row['ApprLandVal'],
                        row['ApprImpsVal'],
                        row['TaxableImpsVal'],
                        row['TaxableLandVal'],
                        yyyy_mm_dd,
                    )
                    for row in rows
                ]
                print('finished importing csv. loading into database...')
                connection.executemany(
                    '''
                    INSERT INTO parcels_appraisal
                      (major, minor, appr_land_val, apr_imps_val, taxable_imps_val, taxable_land_val, date_retrieved)
                    VALUES
                      (?,?,?,?,?,?,?)
                    ''',
                    values
                )

            file_path = os.path.join(retrieved_date, 'EXTR_RPAcct_NoName.csv')
