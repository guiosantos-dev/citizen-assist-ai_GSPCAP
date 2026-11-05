# Citizen Assist AI

## 1. Sobre o projeto

O **Citizen Assist AI** é um assistente desenvolvido em Python para ajudar jovens que estão em busca do primeiro emprego ou começando sua trajetória profissional.

O sistema funciona pelo terminal e oferece orientações sobre temas como documentação, preparação profissional e oportunidades de trabalho.

As informações são armazenadas em uma base de conhecimento no formato JSON, permitindo que o assistente pesquise respostas de acordo com as palavras-chave digitadas pelo usuário.

## 2. Público-alvo

Jovens que estão procurando o primeiro emprego, participando de processos seletivos ou iniciando sua experiência no mercado de trabalho.

## 3. Objetivo

Facilitar o acesso a informações úteis e confiáveis sobre o mundo do trabalho, oferecendo orientações simples, organizadas e acessíveis.

## 4. Funcionalidades

- Pesquisa de orientações por meio de perguntas digitadas pelo usuário.
- Busca baseada em palavras-chave e pontuação de relevância.
- Exibição de orientações organizadas por categorias.
- Apresentação de fontes e datas de verificação das informações.
- Identificação de perguntas sem respostas cadastradas.
- Proteção contra o envio de dados pessoais, como CPF, telefone e e-mail.
- Registro dos atendimentos em arquivo JSON.
- Cálculo de indicadores de desempenho do assistente.
- Avaliação da facilidade de uso pelo usuário.
- Exportação do histórico de atendimentos para CSV.

## 5. Tecnologias utilizadas

- **Python:** linguagem utilizada no desenvolvimento do sistema.
- **JSON:** armazenamento da base de conhecimento, histórico e avaliação.
- **CSV:** exportação dos atendimentos.
- **Git e GitHub:** controle de versão e armazenamento do projeto.

## 6. Estrutura do projeto

```text
citizen-assist-ai/
│
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
│
├── data/
│   ├── base_conhecimento.json
│   ├── historico.json
│   ├── avaliacao.json
│   └── atendimentos.csv
│
└── README.md
```

## 7. Como executar o projeto

1. Tenha o Python instalado no computador.
2. Baixe ou clone o repositório do GitHub.
3. Abra a pasta do projeto no PyCharm ou em outro editor.
4. Execute o arquivo `main.py`.
5. Utilize o menu apresentado no terminal para fazer perguntas, navegar pelas categorias, consultar indicadores e exportar o histórico.
