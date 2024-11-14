import yt_dlp

def baixar_video(url, apenas_audio=False):
    caminho_diretorio = "/home/kali/Videos"
    
    ydl_opts = {
        'outtmpl': f'{caminho_diretorio}/%(title)s.%(ext)s',  # Define o formato do nome do arquivo
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
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f'Download concluído! Arquivo salvo em: {caminho_diretorio}')
    except Exception as e:
        print(f'Ocorreu um erro: {e}')

# Solicitar a URL do vídeo
video_url = input('Digite a URL do vídeo do YouTube: ')

# Solicitar ao usuário se ele deseja baixar apenas o áudio
apenas_audio = input('Deseja baixar apenas o áudio? (s/n): ').lower() == 's'

# Baixar o vídeo ou áudio com base na entrada do usuário
baixar_video(video_url, apenas_audio)
