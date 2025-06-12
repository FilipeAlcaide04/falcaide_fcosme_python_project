# 🇵🇹 Simulação de Eleições Legislativas em Portugal

Este projeto simula o processo das eleições legislativas em Portugal, com as seguintes funcionalidades principais:

- 📊 **Geração de resultados eleitorais simulados por freguesia**, com base em resultados regionais.
- 🔁 **Comparação dos resultados fictícios de 2019 com os de 2024**.
- 🌐 **Servidor para receção e processamento de dados**.
- 📈 **Visualização dos resultados num site interativo e intuitivo**.

---

## 📥 Clonagem do Repositório

Certifique-se de que tem o Git instalado. No terminal, execute:

```bash
git clone https://github.com/FilipeAlcaide04/falcaide_fcosme_python_project
cd falcaide_fcosme_python_project

```

---

## 🐍 Como Executar

1. Crie e ative o Virtual Enviroment: (Mandatory)
- **Cria e inicia o ambiente virtual:**
    ```bash
    # Cria um ambiente virtual 
    python3 -m venv nome_do_ambiente 

    # Ativar o ambiente
    Windows: meu_ambiente\Scripts\activate.
    macOS/Linux: source meu_ambiente/bin/activate.

    # Quando quiser desativar o ambiente

    deactivate
    ```

- **Instalar dependências:**
    ```bash
    pip install -r requirements.txt 
    ```

## Execute o script principal para, correr testes e executar os scripts na ordem correta:
```bash
python3 exec_app.py
```

## Execução faseada (caso prefira executar cada etapa manualmente):

- **Executar testes (todos ou um a um):**
    ```bash
    python3 unit_test/run_all_tests
    ```

- **Executar scripts individuais:**
    - 1º- Data Aquisition:
        ```bash
        python3 run_time/data_aquisition.py
        ```
    - 2º- Data Cleaning:
        ```bash
        python3 run_time/data_cleaning_etc.py
        ```
    - 3º- Iniciar servidor:
        ```bash
        python3 server_data/cne_server.py
        ```

---

## 📁 Estrutura do Projeto

```
FALCAIDE_FCOSME_PROJECT/
│
├── exec_app.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── processed/
│   │   ├── leg_19/
│   │   └── leg_24/
│   └── raw/
│       ├── partidos_19.json
│       ├── partidos_24.json
│       └── elections/
│
├── docs/
│   ├── ined_id.txt
│   ├── relatorio.md
│   ├── TODO.md
│   └── Trabalho_Final_enunciado.pdf
│
├── run_time/
│   ├── data_aquisition.py
│   ├── data_cleaning_etc.py
│   ├── requirements.py
│   └── __pycache__/
│
├── server_data/
│   ├── cne_server.py
│   └── __pycache__/
│
├── templates/
│   ├── index.html
│   └── style.css
│
├── src/
│   ├── data_generator.py
│   └── file_handlers.py
│
├── unit_tests/
│   ├── 0_requirements_test.py
│   ├── 1_file_handlers_test.py
│   ├── 2_data_aquisition_test.py
│   ├── 3_data_generator_test.py
│   ├── 4_cne_server_test.py
│   ├── run_all_tests.py
│   ├── run_pylint.py
│   └── __pycache__/
```

---

## 📝 Notas

- Certifique-se de ter o Python 3.13 instalado.
- Os dados simulados são gerados com base nos votantes por freguesia e partidos disponíveis em `partidos_19.json` e `partidos_24.json`.
- O servidor web permite visualizar e interagir com os resultados simulados.
- Para dúvidas ou sugestões, abra uma issue no GitHub.

---

## 👨‍💻 Autores

- Filipe Alcaide
- Fábio Cosme 

---

## 📄 Licença

Este projeto está licenciado sob a [Istec License](LICENSE).
