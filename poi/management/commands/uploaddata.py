"""
Management utility to upload PoI data.
"""
import os
from functools import partial
import zipfile
import pandas as pd
from django.core.management.base import BaseCommand
import tempfile
from ...models import PoI


class Command(BaseCommand):
    help = 'Used to upload PoI data.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('path', help='Specifies the path to a file (or files).')

    def handle(self, path, **options):
        filepaths = []
        if not os.path.exists(path):
            self.stderr.write("The specified file or directory doesn't exist")
            return
        if os.path.isfile(path):
            filepaths.append(path)
        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                filepaths.extend([os.path.join(root, file) for file in files])
        for filepath in filepaths:
            print(filepath)
            if zipfile.is_zipfile(filepath):
                tempdir = tempfile.gettempdir()
                with zipfile.ZipFile(filepath, 'r') as zip_ref:
                    zip_ref.extractall(tempdir)
                    for root, dirs, files in os.walk(tempdir):
                        filepath = os.path.join(root, files[0])
                        break
            for method in (pd.read_csv, pd.read_json, partial(pd.read_xml, parser='etree')):
                print(method)
                try:
                    df = method(filepath)
                    break
                except pd.errors.ParserError as e:
                    print(e)
                except ValueError as e:
                    print(e)
            else:
                continue
            df = df.rename(columns={
                'pname': 'name',
                'poi_name': 'name',
                'id': 'external_id',
                'pid': 'external_id',
                'poi_id': 'external_id',
                'plongitude': 'lon',
                'poi_longitude': 'lon',
                'platitude': 'lat',
                'poi_latitude': 'lat',
                'pcategory': 'category',
                'poi_category': 'category',
                'pratings': 'ratings',
                'poi_ratings': 'ratings',
            })
            if 'coordinates' in df:
                df['lon'] = df['coordinates'].apply(lambda x: x['longitude'])
                df['lat'] = df['coordinates'].apply(lambda x: x['latitude'])
                df = df.drop('coordinates', axis=1)
            df['ratings'] = df['ratings'].apply(lambda x: x if isinstance(x, list) else x.strip('{}').split(','))
            df = df[['name', 'external_id', 'lon', 'lat', 'category', 'ratings']]
            print(df)
            PoI.objects.bulk_create([
                PoI(**row) for index, row in df.iterrows()
            ], 1000)
