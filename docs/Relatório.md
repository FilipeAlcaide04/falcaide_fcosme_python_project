# 📊 Relatório Detalhado do Projeto: Simulação de Eleições Legislativas em Portugal

## 1. Introdução

O presente relatório descreve o desenvolvimento do projeto de simulação de eleições legislativas em Portugal, realizado no âmbito da unidade curricular de Programação 4. O projeto visa criar uma plataforma capaz de gerar, processar, comparar e visualizar resultados eleitorais fictícios, baseando-se em dados reais e técnicas de simulação (Dirichlet).

---

## 2. Motivação e Objetivos

### 2.1. Motivação

A análise de resultados eleitorais é fundamental para compreender dinâmicas políticas e sociais. No entanto, a obtenção de dados detalhados por freguesia e a simulação de cenários alternativos são tarefas complexas e pouco acessíveis. Este projeto pretende colmatar essa lacuna, fornecendo uma ferramenta flexível e extensível para simulação e análise de eleições.

### 2.2. Objetivos Específicos

- **Simular resultados eleitorais por freguesia**, respeitando o número real de votantes e a lista de partidos concorrentes.
- **Permitir a comparação entre diferentes anos eleitorais** (2019 e 2024), facilitando a análise de tendências e variações.
- **Desenvolver um servidor web** para disponibilização dos dados e interação com o utilizador.
- **Criar uma interface web intuitiva** para visualização dos resultados, acessível a utilizadores técnicos e não técnicos.
- **Garantir a robustez e fiabilidade do sistema** através de testes automatizados.

---

## 3. Arquitetura e Estrutura do Projeto

### 3.1. Estrutura de Pastas

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

### 3.2. Componentes Principais

- **Aquisição e limpeza de dados:** Scripts para recolha e preparação dos dados de base.
- **Geração de votos simulados:** Algoritmos para distribuição dos votos por partido em cada freguesia, com base em métodos probabilísticos e/ou históricos.
- **Processamento e armazenamento:** Estruturas de dados otimizadas para guardar e aceder rapidamente aos resultados simulados.
- **Servidor web:** Backend em Python (Flask) para servir os dados e responder a pedidos do frontend.
- **Frontend:** Interface web desenvolvida em HTML/CSS, permitindo visualização interativa dos resultados.
- **Testes automatizados:** Scripts de teste para garantir a integridade e fiabilidade do sistema.

---

## 4. Metodologia de Simulação

### 4.1. Fontes de Dados

- **Regiões organizadas em json:** `dados_regionais.processed.json`
- **Lista de partidos:** `partidos_19.json` e `partidos_24.json`
- **Resultados regionais:** Dados reais e/ou simulados para parametrização dos algoritmos.

### 4.2. Algoritmo de Geração de Votos

1. **Leitura dos dados de base:** Para cada freguesia, obtém-se o número total de votantes e a lista de partidos.
2. **Distribuição dos votos:** 
    - Utiliza-se uma abordagem probabilística, atribuindo a cada partido um peso (baseado em resultados históricos, tendências ou aleatoriedade controlada).
    - Os votos são distribuídos proporcionalmente aos pesos, garantindo que a soma corresponde ao total de votantes.
    - Pequenos ajustes são feitos para garantir integridade (ex: arredondamentos).
3. **Armazenamento dos resultados:** Os votos por partido e freguesia são guardados em `votos_freguesia_24` ou `votos_freguesia_24`.

### 4.3. Comparação de Resultados

- Implementação de scripts para comparar os resultados simulados de diferentes anos, permitindo identificar variações por partido, freguesia ou região.

---

## 5. Visualização e Interação

- **Servidor web:** Implementado em Flask, expõe endpoints para consulta dos dados simulados.
- **Frontend:** Página web interativa que permite ao utilizador selecionar freguesias, partidos e anos, visualizando os resultados em tabelas e gráficos.
- **Exportação de dados:** Possibilidade de exportar resultados para análise externa.

---

## 6. Testes e Validação

- **Testes unitários:** Cobrem funções de leitura, processamento e geração de votos.
- **Testes de integração:** Garantem o correto funcionamento do pipeline completo, desde a aquisição de dados até à visualização.
- **Validação manual:** Comparação dos resultados simulados com dados reais para aferir plausibilidade.

---

## 7. Resultados Obtidos

- **Geração eficiente de resultados simulados** para todas as freguesias e partidos.
- **Comparação clara entre diferentes anos eleitorais**, permitindo análise de tendências.
- **Interface web funcional e intuitiva**, facilitando o acesso aos dados por qualquer utilizador.

---

## 8. Dificuldades e Aprendizagens

- **Desafios na normalização dos dados** devido a diferentes formatos e fontes.
- **Gestão de arredondamentos e integridade dos totais** na distribuição dos votos.
- **Integração entre backend e frontend** para garantir performance e usabilidade.
- **Importância dos testes automatizados** para evitar regressões e garantir fiabilidade.

---

## 9. Conclusão

O projeto atingiu os objetivos propostos, fornecendo uma solução robusta e flexível para simulação e análise de eleições legislativas em Portugal. A arquitetura modular permite fácil manutenção e expansão, e a interface web torna os resultados acessíveis a um público alargado. O trabalho realizado contribui para a literacia eleitoral e pode ser base para projetos futuros de análise política e social.

---

## 10. Autores

- Filipe Alcaide
- Fábio Cosme

---

## 11. Licença

Este projeto está licenciado sob a [Istec License](LICENSE)