import feedparser
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from time import sleep
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# URL do feed RSS que será monitorado
FEED_URL = "https://concursosnobrasil.com/concursos/feed"
# Intervalo de verificação em segundos (600 segundos = 10 minutos)
CHECK_INTERVAL = 600
# Nome do banco de dados SQLite
DATABASE = "rss_feed.db"

# Obter variáveis do arquivo .env
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_SEND = os.getenv('EMAIL_SEND')

def setup_database():
    """
    Configura o banco de dados SQLite criando a tabela 'posts' se ela não existir.
    A tabela armazenará os links dos posts já verificados para evitar notificações duplicadas.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (link TEXT)''')
    conn.commit()
    conn.close()

def is_new_post(link):
    """
    Verifica se o link do post já foi processado. 
    Se for um link novo, insere no banco de dados e retorna True. 
    Caso contrário, retorna False.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM posts WHERE link=?", (link,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO posts (link) VALUES (?)", (link,))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def send_email(subject, body):
    """
    Envia um e-mail com o assunto e corpo fornecidos.
    """
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_SEND
    msg['Subject'] = subject

    # Adiciona o corpo do e-mail
    msg.attach(MIMEText(body, 'plain'))

    # Configura e envia o e-mail usando o servidor SMTP do Gmail
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)

def check_feed():
    """
    Verifica o feed RSS e envia um e-mail para novos posts.
    """
    print("Verificando o feed RSS por novos concursos...")
    # Faz o parsing do feed RSS
    feed = feedparser.parse(FEED_URL)
    for entry in feed.entries:
        # Se o post for novo, envia um e-mail com as informações do post
        if is_new_post(entry.link):
            # Remove tags HTML da descrição
            soup = BeautifulSoup(entry.description, 'html.parser')
            clean_description = soup.get_text()

            subject = f"Novo Concurso: {entry.title}"
            body = f"Link: {entry.link}\n\nDescrição: {clean_description}\n\nPublicado em: {entry.published}"
            send_email(subject, body)
            print(f"Novo concurso encontrado e e-mail enviado: {entry.title}")

if __name__ == "__main__":
    # Configura o banco de dados na primeira execução
    setup_database()
    while True:
        # Verifica o feed RSS periodicamente
        check_feed()
        sleep(CHECK_INTERVAL)
