from unittest.mock import patch
from .base_test_redshift_db_driver import BaseTestRedshiftDBDriver
from ...records.format_hints import bluelabs_format_hints
from records_mover.db.redshift.redshift_db_driver import Table
from sqlalchemy_redshift.commands import Encoding, Compression


class TestRedshiftDBDriverImportBlueLabs(BaseTestRedshiftDBDriver):
    @patch('records_mover.db.redshift.loader.CopyCommand')
    def test_load_bluelabs(self,
                           mock_CopyCommand):
        lines_scanned = self.load(bluelabs_format_hints, fail_if=True)

        expected_args = {
            'access_key_id': 'fake_aws_id',
            'compression': Compression.gzip,
            'data_location': 's3://mybucket/myparent/mychild/_manifest',
            'date_format': 'YYYY-MM-DD',
            'delimiter': ',',
            'encoding': Encoding.utf8,
            'escape': True,
            'ignore_header': 0,
            'manifest': True,
            'max_error': 0,
            'quote': '"',
            'remove_quotes': False,
            'secret_access_key': 'fake_aws_secret',
            'session_token': 'fake_aws_token',
            'time_format': 'auto',
            'to': Table('mytable', self.redshift_db_driver.meta, schema='myschema'),
            'region': self.mock_directory.loc.region,
            'empty_as_null': True,
        }

        mock_CopyCommand.assert_called_with(**expected_args)
        self.assertIsNone(lines_scanned)
