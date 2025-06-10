"""Testes unitários para o módulo de instalação de pacotes"""
import sys
import subprocess
from pathlib import Path
from unittest.mock import patch
import pytest

# Adiciona o diretório pai ao PATH do Python
sys.path.append(str(Path(__file__).parent.parent))

from run_time.requirements import install # pylint: disable=wrong-import-position, import-error

# Isto está a funcionar não sei porque razão não encontrava o
# modulo src.file_handlers (Tentei de tudo, mas não consegui resolver)

class TestPackageInstaller:
    """Classe de testes para o instalador de pacotes"""
    @patch('subprocess.check_call')
    def test_install_success(self, mock_check_call):
        """Testa a instalação bem-sucedida de todos os pacotes"""
        print("\n=== Testando instalação bem-sucedida ===")
        mock_check_call.return_value = 0
        install()
        mock_check_call.assert_any_call\
            ([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        expected_packages = [
            "xlrd", "flask", "pandas", "matplotlib", "openpyxl",
            "requests", "python-dotenv", "pylint", "pytest"
        ]
        mock_check_call.assert_any_call\
            ([sys.executable, "-m", "pip", "install"] + expected_packages)
        print("✅ Teste de sucesso passou")

    @patch('subprocess.check_call')
    @patch('sys.exit')
    def test_install_failure(self, mock_exit, mock_check_call):
        """Testa o comportamento quando a instalação falha"""
        print("\n=== Testando falha na instalação ===")
        mock_check_call.side_effect = subprocess.CalledProcessError(1, "pip install")
        install()

        mock_exit.assert_called_once_with(1)
        print("✅ Teste de falha passou")

    @patch('subprocess.check_call')
    @patch('builtins.print')
    def test_output_messages(self, mock_print, mock_check_call):
        """Testa se as mensagens de saída estão corretas"""
        print("\n=== Testando mensagens de saída ===")
        mock_check_call.return_value = 0
        install()
        expected_messages = [
            "📦 Installing required packages...",
            "✅ All packages installed successfully."
        ]
        actual_messages = [args[0] for args, _ in mock_print.call_args_list]
        for msg in expected_messages:
            assert msg in actual_messages, f"Mensagem '{msg}' não encontrada na saída"
        print("✅ Teste de mensagens passou")
    @patch('subprocess.check_call')
    @patch('builtins.print')
    def test_error_message_on_failure(self, mock_print, mock_check_call):
        """Testa se a mensagem de erro é exibida corretamente"""
        print("\n=== Testando mensagem de erro ===")
        error = subprocess.CalledProcessError(1, "pip install")
        mock_check_call.side_effect = error
        try:
            install()
        except SystemExit:
            pass
        mock_print.assert_any_call(f"❌ Installation failed: {error}")
        print("✅ Teste de mensagem de erro passou")

if __name__ == "__main__":
    print("Executando testes diretamente...")
    pytest.main(["-v", __file__])


#Fizemos um teste com pytest para verificar a instalação de pacotes necessários. ehehehehhehehehe
