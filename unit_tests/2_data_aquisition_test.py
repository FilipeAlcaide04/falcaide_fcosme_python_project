""" Unit tests for the data acquisition module."""
import unittest
from unittest.mock import ANY
from unittest.mock import patch, mock_open
import os
import io
import zipfile
import sys
from pathlib import Path
from requests.exceptions import RequestException

# Adiciona o diretório pai ao PATH do Python
sys.path.append(str(Path(__file__).parent.parent))

# Now import the module (after renaming the file to data_aquisition.py)
from run_time import data_aquisition  # pylint: disable=wrong-import-position, import-error

class TestDataAcquisition(unittest.TestCase):
    """Test cases for the data acquisition module."""
    @patch('os.makedirs')
    @patch('requests.get')
    @patch('builtins.open', new_callable=mock_open)
    def test_csv_downloads(self, mock_file, mock_get, mock_makedirs):
        """Test downloading CSV files and writing them to disk."""
        # Setup mock response for CSV downloads
        mock_response = unittest.mock.Mock()
        mock_response.content = b"test,data\n1,2"
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Run the main function
        data_aquisition.main()

        # Check if directories were created
        mock_makedirs.assert_any_call("data/raw", exist_ok=True)

        # Check if requests were made for each CSV
        expected_csv_urls = [
            "https://raw.githubusercontent.com/mapaslivres/"\
                "divisoes-administrativas-pt/master/data/districts.csv",
            "https://raw.githubusercontent.com/mapaslivres/"\
                "divisoes-administrativas-pt/master/data/municipalities.csv",
            "https://raw.githubusercontent.com/mapaslivres/"\
                "divisoes-administrativas-pt/master/data/freguesias.csv",
                ]

        for url in expected_csv_urls:
            mock_get.assert_any_call(url, timeout=ANY)

        # Check if files were written
        self.assertGreaterEqual(mock_file.call_count, 3)

    @patch('requests.get')
    def test_download_and_extract_zip_success(self, mock_get):
        """Test downloading and extracting a zip file successfully."""
        # Mock the requests.get method to simulate a zip file download
        # Create a mock zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            zip_file.writestr('test.txt', 'test content')
        zip_buffer.seek(0)

        # Setup mock response
        mock_response = unittest.mock.Mock()
        mock_response.content = zip_buffer.getvalue()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Test the function
        output_path = "test_output"
        os.makedirs(output_path, exist_ok=True)
        result = data_aquisition.download_and_extract_zip\
            ("http://example.com/test.zip", output_path)

        # Check results
        self.assertTrue(result)
        self.assertTrue(os.path.exists(os.path.join(output_path, 'test.txt')))
        # Cleanup
        os.remove(os.path.join(output_path, 'test.txt'))
        os.rmdir(output_path)
    @patch('requests.get')
    def test_download_and_extract_zip_failure(self, mock_get):
        """Test downloading and extracting a zip file that fails."""
        # Simulate a failed request
        mock_get.side_effect = RequestException("Connection error")
        # Test the function
        result = data_aquisition.download_and_extract_zip\
            ("http://example.com/test.zip", "test_output")
        # Check results
        self.assertFalse(result)
    @patch('os.remove')
    @patch('os.path.exists')
    def test_file_cleanup(self, mock_exists, mock_remove):
        """Test the cleanup of specific files after data acquisition."""
        # Setup mock for file removal
        mock_exists.return_value = True
        # Run the main function
        data_aquisition.main()
        # Check if remove was called for the expected files
        expected_files = [
            os.path.join("data", "raw", "elections", "2024_ar_quadro_resultados.ods"),
            os.path.join("data", "raw", "elections", "ar2019-quadro-resultados.ods")
        ]
        for file_path in expected_files:
            mock_remove.assert_any_call(file_path)

if __name__ == '__main__':
    unittest.main()
