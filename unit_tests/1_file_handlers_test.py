"""Testes unitários para o módulo de manipulação de ficheiros e dados."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
from unittest import mock
import pandas as pd
import numpy as np

# Adiciona o diretório pai ao PATH do Python para importar o módulo
sys.path.append(str(Path(__file__).parent.parent))

from src import file_handlers as modulo  # pylint: disable=wrong-import-position, import-error


class TestDataProcessing(unittest.TestCase):
    """Testes para o módulo de manipulação de ficheiros e dados."""

    @patch("os.path.exists", return_value=False)
    def test_carregar_csv_ficheiro_inexistente(self, mock_exists):
        """Testa se carrega_csv lança FileNotFoundError para ficheiro inexistente."""
        with self.assertRaises(FileNotFoundError) as context:
            modulo.carregar_csv("caminho/falso.csv")
        self.assertIn("O ficheiro 'caminho/falso.csv' não existe.", str(context.exception))
        mock_exists.assert_called_once_with("caminho/falso.csv")

    @patch("src.file_handlers.os.path.exists", return_value=True)
    @patch("src.file_handlers.pd.read_csv", side_effect=Exception("Erro ao ler CSV"))
    def test_carregar_csv_erro_leitura(self, mock_read_csv, mock_exists):
        """Testa se carrega_csv lança RuntimeError em caso de erro na leitura do CSV."""
        with self.assertRaises(RuntimeError) as context:
            modulo.carregar_csv("ficheiro.csv")
        self.assertIn("Erro ao carregar o ficheiro 'ficheiro.csv'", str(context.exception))
        mock_exists.assert_called_once_with("ficheiro.csv")
        mock_read_csv.assert_called_once_with("ficheiro.csv")

    @patch("os.path.exists", return_value=True)
    @patch("pandas.read_csv")
    def test_carregar_csv_sucesso(self, mock_read, mock_exists):
        """Testa se carrega_csv retorna DataFrame correto quando o ficheiro existe."""
        df_mock = pd.DataFrame({"col": [1, 2]})
        mock_read.return_value = df_mock
        resultado = modulo.carregar_csv("teste.csv")
        pd.testing.assert_frame_equal(resultado, df_mock)
        mock_exists.assert_called_once_with("teste.csv")
        mock_read.assert_called_once_with("teste.csv")

    @patch("pandas.read_excel")
    @patch("pandas.read_csv")
    @patch("src.data_generator.gen_pop", return_value=np.array([1000, 2000]))
    @patch(
        "src.data_generator.gen_votes_por_partido",
        return_value=[{"ine_id": "0101", "votos": 123}, {"ine_id": "0202", "votos": 456}],
    )
    def test_sec_main_estrutura_dados(self, _mock_votes, _mock_pop, mock_read_csv, mock_read_excel):
        """Testa se sec_main gera a estrutura de dados correta."""
        # Mock CSV com freguesias
        df_freg = pd.DataFrame(
            {
                "ine_id": ["0101", "0202"],
                "distrito": ["Lisboa", "Porto"],
                "municipio": ["Lisboa", "Porto"],
                "freguesia": ["Campo Grande", "Boavista"],
            }
        )
        mock_read_csv.return_value = df_freg

        # Mock Excel com dados por distrito
        dados_excel = pd.DataFrame(0, index=range(10), columns=range(20))
        distritos_mock = [f"Distrito_{i}" for i in range(18)]
        pop_mock = [100_000 + i * 1000 for i in range(18)]
        eleitores_mock = [80_000 + i * 1000 for i in range(18)]
        votos_mock = [2000 + i * 100 for i in range(18)]

        dados_excel.iloc[2, 2:] = distritos_mock      # linha 2: nomes dos distritos
        dados_excel.iloc[3, 2:] = pop_mock            # linha 3: população total
        dados_excel.iloc[4, 2:] = eleitores_mock      # linha 4: eleitores registados
        dados_excel.iloc[7, 2:] = votos_mock          # linha 7: votos válidos

        mock_read_excel.return_value = dados_excel

        with patch("builtins.open", mock.mock_open()), patch("json.dump") as mock_json:
            modulo.sec_main("2024")
            self.assertTrue(mock_json.called)
            args, _ = mock_json.call_args
            self.assertIsInstance(args[0], list)
            self.assertTrue(any("Abstenção" in freg for freg in args[0]))


if __name__ == "__main__":
    unittest.main()
