import os
from yt_dlp import YoutubeDL

def baixar_video(url, nome_arquivo, apenas_audio=False):
    caminho_diretorio = "/home/kali/Videos"
    
    # Define o formato do nome do arquivo com base na entrada do usuário
    ydl_opts = {
        'outtmpl': f'{caminho_diretorio}/{nome_arquivo}.%(ext)s',
    }

    if apenas_audio:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'best'

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f'Download concluído! Arquivo salvo em: {caminho_diretorio}/{nome_arquivo}')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Solicitar a URL do vídeo
video_url = input('Digite a URL do vídeo do YouTube: ')

# Solicitar ao usuário o nome do arquivo
nome_arquivo = input('Digite o nome do arquivo para salvar: ')

# Solicitar ao usuário se ele deseja baixar apenas o áudio
apenas_audio = input('Deseja baixar apenas o áudio? (s/n): ').lower() == 's'

# Baixar o vídeo ou áudio com base na entrada do usuário
baixar_video(video_url, nome_arquivo, apenas_audio)
