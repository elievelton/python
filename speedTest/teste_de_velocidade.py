from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
import speedtest

console = Console()

# Tela de carregamento estilo "encanto"
with Progress(
    SpinnerColumn(),
    TextColumn("[bold magenta]Invocando magia da velocidade...[/bold magenta]"),
    transient=True,
) as progress:
    progress.add_task(description="Carregando...", total=None)
    
    st = speedtest.Speedtest()
    st.get_best_server()
    down_speedt = st.download()
    up_speed = st.upload()
    ping = st.results.ping
    best_server = st.get_best_server()

# Convertendo para Mbps
down_speed = down_speedt / 1_000_000
up_speed_mbps = up_speed / 1_000_000

# Exibindo os resultados com estilo
console.print(f"[bold green]Download Speed:[/bold green] {down_speed:.2f} Mbps")
console.print(f"[bold blue]Upload Speed:[/bold blue] {up_speed_mbps:.2f} Mbps")
console.print(f"[bold yellow]Ping:[/bold yellow] {ping} ms")
console.print(f"[bold cyan]Melhor servidor:[/bold cyan] {best_server['sponsor']} em {best_server['name']}, {best_server['country']}")