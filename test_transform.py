"""Run with: python -m unittest -v test_transform.py"""
import csv
import unittest
from pathlib import Path
from transform import clean_rows

DATA_DIR = Path(__file__).parent / 'test_data'


def load_csv(filename):
    with (DATA_DIR / filename).open(newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader), reader.fieldnames


class TestTransform(unittest.TestCase):
    def test_messy_students(self):
        rows, headers = load_csv('messy_students.csv')
        cleaned, duplicates, changes = clean_rows(rows, headers)
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(duplicates, 1)
        self.assertEqual(cleaned[0], {
            'Name': 'John Doe', 'Email': 'john.doe@example.com',
            'City': 'Port Harcourt', 'Country': 'Nigeria',
            'Registration_Date': '2026-10-22',
        })
        self.assertGreater(changes, 0)

    def test_duplicates_after_normalization(self):
        rows, headers = load_csv('duplicate_records.csv')
        cleaned, duplicates, changes = clean_rows(rows, headers)
        self.assertEqual(len(cleaned), 2)
        self.assertEqual(duplicates, 2)
        self.assertEqual(cleaned[0]['Name'], 'Ada')

    def test_date_formats_and_invalid_dates(self):
        rows, headers = load_csv('date_formats.csv')
        cleaned, duplicates, changes = clean_rows(rows, headers)
        self.assertEqual([r['Start_Date'] for r in cleaned[:5]], ['2026-10-22'] * 5)
        self.assertEqual(cleaned[5]['Start_Date'], 'not-a-date')
        self.assertEqual(cleaned[6]['Start_Date'], '31/02/2026')
        self.assertEqual(duplicates, 0)

    def test_empty_values(self):
        rows, headers = load_csv('empty_values.csv')
        cleaned, duplicates, changes = clean_rows(rows, headers)
        self.assertEqual(len(cleaned), 3)
        self.assertEqual(cleaned[0]['Name'], '')
        self.assertEqual(cleaned[1]['Email'], '')
        self.assertEqual(cleaned[2]['Email'], 'bob@example.com')
        self.assertEqual(cleaned[2]['Join_Date'], 'bad-date')


if __name__ == '__main__':
    unittest.main()
