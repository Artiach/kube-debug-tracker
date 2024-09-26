import os
import subprocess
import time
from kube_debug_tracker.notion_integration import create_debugging_page, add_debugging_content
from datetime import datetime

# Función para capturar el último número de línea del historial al iniciar debugging
def get_last_history_line(shell="zsh"):
    home = os.path.expanduser("~")
    if shell == "bash":
        history_file = os.path.join(home, ".bash_history")
    else:
        history_file = os.path.join(home, ".zsh_history")

    if not os.path.exists(history_file):
        print(f"No history file found at {history_file}")
        return 0

    with open(history_file, 'r') as file:
        commands = file.readlines()

    return len(commands)  # El número de líneas en el historial

def extract_command(command_line):
    # Separar la línea por el carácter ';' y quedarnos con el último fragmento (el comando real)
    return command_line.split(';')[-1].strip()


# Función para leer el historial de comandos desde zsh o bash y filtrar los comandos de Kubernetes
def get_commands(start_line, shell="zsh"):
    home = os.path.expanduser("~")
    if shell == "bash":
        history_file = os.path.join(home, ".bash_history")
    else:
        history_file = os.path.join(home, ".zsh_history")

    if not os.path.exists(history_file):
        print(f"No history file found at {history_file}")
        return []

    # Leer las líneas desde el historial
    with open(history_file, 'r') as file:
        commands = file.readlines()


    # Filtrar los comandos de Kubernetes desde la línea de inicio
    k8s_commands = [
    extract_command(cmd).strip() for i, cmd in enumerate(commands)
    if i >= start_line
]
    return k8s_commands

# Función para ejecutar los comandos y capturar la salida
def run_command_and_capture_output(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.stderr.decode('utf-8')

# Proceso en segundo plano que monitorea el historial de comandos
def monitor_commands_in_background(debugging_session_id, shell="zsh", start_line=0):
    previous_commands = set()

    # Get the current date and time in the format you want (e.g., YYYY-MM-DD HH:MM)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

# Use the formatted time as part of the page title
    page_id = create_debugging_page(f"Debugging Session - {current_time}", "Initial debugging content")


    while True:
        time.sleep(5)  # Esperar 5 segundos entre lecturas del historial
        new_commands = set(get_commands(start_line, shell=shell))
        diff = new_commands - previous_commands

        for command in diff:
            print(f"Nuevo comando encontrado: {command}")
            output = run_command_and_capture_output(command)
            add_debugging_content(page_id, command, output)

        previous_commands = new_commands
