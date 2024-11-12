# Projeto de Monitoramento de Novos Arquivos PDF

Este projeto tem como objetivo monitorar uma página web em busca de novos arquivos PDF. Quando novos arquivos PDF são encontrados, o sistema envia uma notificação por e-mail.

## Funcionalidades

- **Monitoramento Web**: Verifica periodicamente uma página específica em busca de novos arquivos PDF.
- **Notificação por E-mail**: Envia um e-mail notificando os novos arquivos PDF encontrados.

## Tecnologias Utilizadas

- Python
- BeautifulSoup
- Requests
- smtplib (para envio de e-mails)
- dotenv (para gerenciamento de variáveis de ambiente)

## Configuração do Projeto

### Pré-requisitos

- Python 3.x instalado
- Pip (gerenciador de pacotes do Python)

### Passos para Configuração

1. **Clone o Repositório**:
   ```sh
   git clone https://github.com/elievelton/python.git
   cd python

2. **Crie e Ative um Ambiente Virtual**:
    python -m venv myenv
    source myenv/bin/activate  # No Windows: myenv\Scripts\activate
3. **Instale as Dependências**:
    pip install -r requirements.txt
4. **Configure as Variáveis de Ambiente**:
    - Crie um arquivo .env na raiz do projeto e adicione suas credenciais de e-mail:
        EMAIL_USER=seu_email@gmail.com
        EMAIL_PASSWORD=sua_senha_de_app
        EMAIL_SEND=destinatario@example.com

## Executando o Projeto
Para iniciar o monitoramento da página e enviar notificações por e-mail quando novos arquivos PDF forem encontrados, execute:
 .python3 verificaPagina.py

## Estrutura do Código
verificaPagina.py: Script principal que realiza o monitoramento e envio de e-mails.

pdf_links.txt: Arquivo de armazenamento de links de PDFs já conhecidos.

## Notas
Certifique-se de que a senha utilizada no .env é uma senha de aplicativo, especialmente se você estiver usando o Gmail com autenticação de dois fatores ativada.