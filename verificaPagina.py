import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup  # Biblioteca para fazer web scraping
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime  # Biblioteca para manipular datas e horas

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URL da página web que será monitorada para novos arquivos PDF
url = 'https://ibfc.selecao.net.br/informacoes/466/'

# Nome do arquivo onde serão armazenados os links dos PDFs já conhecidos
pdf_storage_file = 'pdf_links.txt'

# Configurações de email para enviar notificações
email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')
email_send = os.getenv('EMAIL_SEND')

def send_email(new_links):
    """
    Envia um email de notificação com os novos links de PDF encontrados.
    """
    subject = 'Novos Arquivos PDF Encontrados ;)'
    body = f'Novos arquivos PDF encontrados: {", ".join(new_links)}'
    
    # Configura o email com assunto e corpo
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        # Conecta ao servidor SMTP do Gmail e envia o email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Usa TLS para segurança
        server.login(email_user, email_password)  # Faz login com as credenciais fornecidas
        text = msg.as_string()
        server.sendmail(email_user, email_send, text)  # Envia o email
        server.quit()  # Encerra a conexão com o servidor SMTP
        print('Email enviado com sucesso.')
    except Exception as e:
        print(f'Erro ao enviar email: {e}')  # Exibe mensagem de erro em caso de falha

def get_pdf_links():
    """
    Busca todos os links de arquivos PDF na página especificada.
    Returns:
        list: Lista de links de arquivos PDF encontrados.
    """
    response = requests.get(url)  # Faz uma requisição GET para a URL
    soup = BeautifulSoup(response.content, 'html.parser')  # Analisa o conteúdo HTML da página
    
    # Encontra todos os links que terminam com ".pdf" na página
    pdf_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('.pdf')]
    return pdf_links

def load_existing_links():
    """
    Carrega os links de PDFs já conhecidos a partir de um arquivo de armazenamento.
    Returns:
        list: Lista de links de arquivos PDF já conhecidos.
    """
    try:
        with open(pdf_storage_file, 'r') as file:
            existing_links = file.read().splitlines()  # Lê os links do arquivo
    except FileNotFoundError:
        existing_links = []  # Se o arquivo não existir, retorna uma lista vazia
    return existing_links

def save_new_links(new_links):
    """
    Salva os novos links de PDFs no arquivo de armazenamento.
    Args:
        new_links (list): Lista de novos links de arquivos PDF encontrados.
    """
    with open(pdf_storage_file, 'a') as file:
        for link in new_links:
            file.write(link + '\n')  # Escreve cada novo link em uma nova linha

def check_for_new_pdfs():
    """
    Verifica a página em busca de novos arquivos PDF e envia notificações em caso positivo.
    """
    existing_links = load_existing_links()  # Carrega os links já conhecidos
    current_links = get_pdf_links()  # Obtém os links atuais da página
    new_links = [link for link in current_links if link not in existing_links]  # Encontra novos links

    # Obtém a hora atual
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if new_links:
        print(f'[{current_time}] Novos arquivos PDF encontrados: {new_links}')
        save_new_links(new_links)  # Salva os novos links encontrados
        send_email(new_links)  # Envia notificação por email
    else:
        print(f'[{current_time}] Nenhum novo arquivo PDF encontrado :(')

if __name__ == '__main__':
    while True:
        check_for_new_pdfs()  # Verifica a página a cada iteração
        time.sleep(60)  # Aguarda 60 segundos antes de verificar novamente
