
import argparse

def get_args():
    """Obtém os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description='Um script de exemplo de argparse (Calcula o quadrado de um número).'
    )

    parser.add_argument(
    '--numero', '-n', 
    type=float,
    required=True,
    help='Numero para calcular o quadrado.'
    )

    parser.add_argument(
       '--verbose', '-v',
       action='store_true',
       help='Aumentar a verbosidade da saída.'
    )

    return parser.parse_args()


args = get_args()
print(args)