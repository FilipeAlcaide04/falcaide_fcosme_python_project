# 🇵🇹 Simulação de Eleições Legislativas em Portugal 

Este projeto simula o processo das eleições legislativas em Portugal, incluindo:

1. **Geração de resultados eleitorais simulados por freguesia**, com base nos resultados regionais  
2. **Comparação dos resultados fictícios de 2019 com os de 2024**  
3. **Servidor para receção e processamento de dados**  
4. **Visualização dos resultados num site interativo e de fácil utilização**

---

## 📥 Como Clonar o Repositório

Certifique-se de ter o Git instalado. No terminal, execute:

```bash
git clone https://github.com/FilipeAlcaide04/falcaide_fcosme_python_project
```
```bash
cd falcaide_fcosme_python_project
```

---

## 🐍 Como Executar

1. Execute o script principal para instalar dependências, correr testes e executar os scripts na ordem correta:
```bash
python3 exec_app.py
```

2. **Execução faseada** (caso prefira executar cada etapa manualmente):

- **Instalar dependências:**
    ```bash
    python3 run_time/requirements.py
    ```

- **Executar testes (todos ou um a um):**
    ```bash
    python3 run_all_tests
    ```

- **Executar scripts individuais:**
    - Data Aquisition:
        ```bash
        python3 run_time/data_aquisition.py
        ```
    - Data Cleaning:
        ```bash
        python3 run_time/data_cleaning_etc.py
        ```
    - Iniciar servidor:
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
├── .pytest_cache/
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
