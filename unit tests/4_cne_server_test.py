""" Unit tests for the CNE server application."""
import unittest
import json
import sys
from pathlib import Path
from unittest.mock import patch

# Adiciona o diretório pai ao PATH do Python
sys.path.append(str(Path(__file__).parent.parent))

import server_data.cne_server as app # pylint: disable=wrong-import-position, import-error


class TestCneServer(unittest.TestCase):
    """Test cases for the CNE server application."""
    def setUp(self):
        app.app.config['TESTING'] = True
        self.client = app.app.test_client()

    def test_calcular_resultados_nacionais(self):
        """Test the calcular_resultados_nacionais function."""
        dados_mock = [
            {
                "freguesia": "F1",
                "distrito": "D1",
                "municipio": "M1",
                "inscritos": 100,
                "votantes": 80,
                "brancos": 5,
                "votos": {"A": 40, "B": 35},
            }
        ]
        resultado = app.calcular_resultados_nacionais(dados_mock)
        self.assertEqual(resultado['total'], {"A": 40, "B": 35})
        self.assertEqual(resultado['estatisticas']['total_eleitores'], 100)
        self.assertEqual(resultado['estatisticas']['votos_validos'], 75)
        self.assertEqual(resultado['vencedor'], "A")
        self.assertAlmostEqual(resultado['percentagens']['A'], 53.33, places=2)
        self.assertAlmostEqual(resultado['percentagens']['B'], 46.67, places=2)

    def test_index(self):
        """Test the index route."""
         # Test the index route
         # This should return a 200 OK response
         # and render the index.html template
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    @patch('server_data.cne_server.dados_2024', new=[
        {"distrito": "Lisboa"},
        {"distrito": "Porto"},
        {"distrito": "Lisboa"}
    ])
    def test_get_distritos(self):
        """Test the /api/distritos route."""
        response = self.client.get('/api/distritos')
        self.assertEqual(response.status_code, 200)
        distritos = json.loads(response.data)
        self.assertCountEqual(distritos, ["Lisboa", "Porto"])

    @patch('server_data.cne_server.dados_2024', new=[
        {"distrito": "Lisboa", "freguesia": "F1"},
        {"distrito": "Lisboa", "freguesia": "F2"},
        {"distrito": "Porto", "freguesia": "F3"},
    ])
    def test_get_freguesias(self):
        """Test the /api/freguesias route."""
        response = self.client.get('/api/freguesias?distrito=Lisboa')
        self.assertEqual(response.status_code, 200)
        freguesias = json.loads(response.data)
        self.assertCountEqual(freguesias, ["F1", "F2"])

    @patch('server_data.cne_server.dados_2024', new=[
        {
            "freguesia": "F1",
            "distrito": "D1",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ])
    @patch('server_data.cne_server.dados_2019', new=[
        {
            "freguesia": "F1",
            "distrito": "D1",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ])
    @patch('server_data.cne_server.resultados_nacionais_2024',\
           new=app.calcular_resultados_nacionais([
        {
            "freguesia": "F1",
            "distrito": "D1",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ]))
    @patch('server_data.cne_server.resultados_nacionais_2019',\
           new=app.calcular_resultados_nacionais([
        {
            "freguesia": "F1",
            "distrito": "D1",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ]))
    def test_get_resultados_nacionais(self):
        """Test the /api/resultados route for national results."""
        response = self.client.get('/api/resultados')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['tipo'], "nacional")
        self.assertIn("vencedor", data)

    @patch('server_data.cne_server.dados_2024', new=[
        {
            "freguesia": "F1",
            "distrito": "Lisboa",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ])
    @patch('server_data.cne_server.resultados_nacionais_2024',\
           new=app.calcular_resultados_nacionais([
        {
            "freguesia": "F1",
            "distrito": "Lisboa",
            "municipio": "M1",
            "inscritos": 100,
            "votantes": 80,
            "brancos": 5,
            "Abstenção": 20,
            "votos": {"A": 40, "B": 35}
        }
    ]))
    def test_get_resultados_freguesia(self):
        """Test the /api/resultados route for freguesia results."""
        response = self.client.get('/api/resultados?distrito=Lisboa&freguesia=F1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['tipo'], "freguesia")
        self.assertEqual(data['info']['freguesia'], "F1")
        self.assertEqual(data['vencedor'], "A")

if __name__ == '__main__':
    unittest.main()
