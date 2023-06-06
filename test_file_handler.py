import unittest
import pytest
from file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    def setUp(self):
        self.file_handler = FileHandler()

    def test_read_csv(self):
        data = self.file_handler.read_csv('test_file.csv')
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], ['Date', 'Time', 'Value'])
        self.assertEqual(data[1], ['01/01/2023', '12:00 AM', '100.0'])
        self.assertEqual(data[2], ['01/01/2023', '1:00 AM', '200.0'])

    def test_read_yaml(self):
        data = self.file_handler.read_yaml('test_file.yaml')
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Plan 1')
        self.assertEqual(data[0]['summer']['on_peak'], 0.22)
        self.assertEqual(data[0]['winter']['super_off_peak'], 0.14)
        self.assertEqual(data[0]['service_fee'], 10.0)
    
    def test_read_csv_no_file(self):
        with pytest.raises(FileNotFoundError):
            self.file_handler.read_csv('non_existent_file.csv')

    def test_read_yaml_no_file(self):
        with pytest.raises(FileNotFoundError):
            self.file_handler.read_yaml('non_existent_file.yml')

if __name__ == "__main__":
    unittest.main()
