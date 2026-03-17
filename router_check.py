from rich.console import Console
from rich.table import Table

def main():
    console = Console()
    routers = []
    
    console.print("[bold blue]Gestor de Hostnames de Routers[/bold blue]\n")
    
    while True:
        hostname = input("Ingrese el hostname del router (o presione Enter para finalizar): ").strip()
        if not hostname:
            break
        routers.append(hostname)
    
    if not routers:
        console.print("[yellow]No se ingresaron hostnames.[/yellow]")
        return

    table = Table(title="Lista de Routers")
    table.add_column("Índice", justify="right", style="cyan", no_wrap=True)
    table.add_column("Hostname", style="magenta")

    for i, host in enumerate(routers, 1):
        table.add_row(str(i), host)

    console.print(table)

if __name__ == "__main__":
    main()
