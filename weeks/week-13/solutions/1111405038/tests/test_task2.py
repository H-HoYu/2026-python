from __future__ import annotations

import unittest
from pathlib import Path

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[5]
SOLUTION_DIR = Path(__file__).resolve().parents[1]
if str(SOLUTION_DIR) not in sys.path:
    sys.path.insert(0, str(SOLUTION_DIR))

from task2_zipcode_heatmap import get_top_counties, load_county_counts, zip_to_county


class TestTask2(unittest.TestCase):
    def setUp(self) -> None:
        self.data_dir = PROJECT_ROOT / "assets" / "stu-data"

    def test_zip_to_county_penghu(self) -> None:
        self.assertEqual(zip_to_county("880"), "澎湖縣")

    def test_zip_to_county_unknown(self) -> None:
        self.assertEqual(zip_to_county("999"), "其他")

    def test_load_county_counts_type(self) -> None:
        counts = load_county_counts(112, self.data_dir)
        self.assertIsInstance(counts, dict)

    def test_load_county_counts_penghu_positive(self) -> None:
        counts = load_county_counts(112, self.data_dir)
        self.assertGreater(counts.get("澎湖縣", 0), 0)

    def test_get_top_counties_length(self) -> None:
        all_years = {year: load_county_counts(year, self.data_dir) for year in [109, 110, 111, 112, 113, 114]}
        top_counties = get_top_counties(all_years, top_n=10)
        self.assertLessEqual(len(top_counties), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
