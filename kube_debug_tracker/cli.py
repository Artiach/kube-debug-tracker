import click
import os
import psutil
from multiprocessing import Process
from kube_debug_tracker.background_process import monitor_commands_in_background, get_last_history_line

DEBUG_SESSION_PID_FILE = "/tmp/kube_debug_tracker.pid"

@click.group()
def cli():
    """KubeDebugTracker CLI"""
    pass

@cli.command()
@click.option('--bash', is_flag=True, help="Usar el historial de bash en lugar del historial de zsh")
def start_debugging(bash):
    """Inicia el proceso de debugging y monitorea los comandos ejecutados"""
    if os.path.exists(DEBUG_SESSION_PID_FILE):
        print("Ya hay una sesión de debugging en curso. Finaliza primero con --end-debugging")
        return

    # Determinar si usamos zsh (por defecto) o bash
    shell = "bash" if bash else "zsh"

    # Capturamos el último número de línea en el historial antes de iniciar la sesión
    start_line = get_last_history_line(shell)

    # Crea un nuevo proceso que monitoreará los comandos
    p = Process(target=monitor_commands_in_background, args=(1, shell, start_line))  # Pasamos start_line
    p.start()

    # Guardar el PID del proceso en segundo plano
    with open(DEBUG_SESSION_PID_FILE, 'w') as f:
        f.write(str(p.pid))

    print(f"Proceso de debugging iniciado con PID {p.pid}, usando el historial de {shell}")

@cli.command()
def end_debugging():
    """Finaliza el proceso de debugging"""
    if not os.path.exists(DEBUG_SESSION_PID_FILE):
        print("No hay una sesión de debugging en curso")
        return

    # Leer el PID del proceso y terminarlo
    with open(DEBUG_SESSION_PID_FILE, 'r') as f:
        pid = int(f.read())

    if psutil.pid_exists(pid):
        p = psutil.Process(pid)
        p.terminate()
        print(f"Proceso de debugging terminado con PID {pid}")
        os.remove(DEBUG_SESSION_PID_FILE)
    else:
        print(f"El proceso con PID {pid} no existe")
        os.remove(DEBUG_SESSION_PID_FILE)

if __name__ == '__main__':
    cli()
