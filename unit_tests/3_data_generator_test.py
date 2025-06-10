""" Unit tests for the data generation module."""
import json
import os
import sys
import tempfile
from pathlib import Path
import unittest
import numpy as np
import pandas as pd

# Adiciona o diretório pai ao PATH do Python
sys.path.append(str(Path(__file__).parent.parent))

from src.data_generator import gen_pop, gen_votes_por_partido # pylint: disable=wrong-import-position, import-error

class TestElectionDataGeneration(unittest.TestCase):
    """Test cases for the election data generation module."""
    def setUp(self):
        self.test_freguesias = pd.DataFrame({
            'ine_id': ['123', '456'],
            'freguesia': ['Freguesia A', 'Freguesia B'],
            'distrito': ['Lisboa', 'Porto'],
            'municipio': ['Lisboa', 'Porto'],
            'inscritos_freguesia': [1000, 2000],
            'votantes_freguesia': [800, 1800],
            'brancos_freguesia': [50, 100]
        })

        self.partidos_19 = ["PS", "PSD", "BE", "CDU", "CDS-PP", "PAN", "IL",
                           "CHEGA", "LIVRE", "R.I.R.", "PCTP/MRPP", "MPT",
                           "PURP", "PPM", "JPP", "PNR", "Nós, Cidadãos!", "Aliança"]
        self.partidos_24 = ["PS", "AD", "CHEGA", "IL", "BE", "LIVRE", "PAN", "CDU",
                            "R.I.R.", "JPP", "ADN", "Volt", "Ergue-te", "MPT",
                            "PPM", "NC", "MAS", "PTP", "PCTP/MRPP"]

        self.temp_dir = tempfile.mkdtemp()
        self.partidos_19_path = os.path.join(self.temp_dir, 'partidos_19.json')
        self.partidos_24_path = os.path.join(self.temp_dir, 'partidos_24.json')

        with open(self.partidos_19_path, 'w', encoding='utf-8') as f:
            json.dump(self.partidos_19, f)
        with open(self.partidos_24_path, 'w', encoding='utf-8') as f:
            json.dump(self.partidos_24, f)

    def tearDown(self):
        """Remove temporary files and directories."""
        for path in [self.partidos_19_path, self.partidos_24_path]:
            if os.path.exists(path):
                os.remove(path)
        os.rmdir(self.temp_dir)

    def test_gen_pop(self):
        """Test population generation."""
        test_size = 10
        input_data = np.zeros(test_size)
        result = gen_pop(input_data)
        self.assertEqual(len(result), test_size)
        self.assertTrue(all(500 <= x <= 5000 for x in result))

    def test_gen_votes_por_partido_file_not_found(self):
        """Test handling of file not found for partidos."""
        result = gen_votes_por_partido(self.test_freguesias, '2019', partidos_path='fake/path.json')
        self.assertEqual(result, [])

    def test_gen_votes_por_partido_2019(self):
        """Test vote generation for 2019 elections."""
        results = gen_votes_por_partido\
            (self.test_freguesias, '2019', partidos_path=self.partidos_19_path)
        self.assertEqual(len(results), len(self.test_freguesias))

        for result in results:
            self.assertIn('ine_id', result)
            self.assertIn('freguesia', result)
            self.assertIn('votos', result)
            row = self.test_freguesias[self.test_freguesias['ine_id'] == result['ine_id']].iloc[0]
            expected_valid = row['votantes_freguesia'] - row['brancos_freguesia']
            actual_valid = sum(result['votos'].values())
            self.assertAlmostEqual(actual_valid, expected_valid, delta=1)

            for partido in self.partidos_19:
                self.assertIn(partido, result['votos'])

    def test_gen_votes_por_partido_2024(self):
        """Test vote generation for 2024 elections."""
        results = gen_votes_por_partido\
            (self.test_freguesias, '2024', partidos_path=self.partidos_24_path)
        self.assertEqual(len(results), len(self.test_freguesias))

        for result in results:
            self.assertIn('ine_id', result)
            self.assertIn('freguesia', result)
            self.assertIn('votos', result)
            row = self.test_freguesias[self.test_freguesias['ine_id'] == result['ine_id']].iloc[0]
            expected_valid = row['votantes_freguesia'] - row['brancos_freguesia']
            actual_valid = sum(result['votos'].values())
            self.assertAlmostEqual(actual_valid, expected_valid, delta=1)

            for partido in self.partidos_24:
                self.assertIn(partido, result['votos'])

    def test_vote_distribution(self):
        """Test if votes are distributed correctly among parties."""
        results = gen_votes_por_partido\
            (self.test_freguesias, '2019', partidos_path=self.partidos_19_path)
        for result in results:
            votes = result['votos']
            self.assertGreaterEqual\
                (votes['PS'], votes['PCTP/MRPP']) # So para ver se os mambos tao balanceados

    def test_negative_votes_handling(self):
        """Test if negative votes are handled correctly."""
        test_df = self.test_freguesias.copy()
        test_df.loc[0, 'brancos_freguesia'] = 1000
        results = gen_votes_por_partido(test_df, '2019', partidos_path=self.partidos_19_path)
        self.assertEqual(sum(results[0]['votos'].values()), 0)

if __name__ == '__main__':
    unittest.main()
