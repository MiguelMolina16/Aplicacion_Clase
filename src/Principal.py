import threading
from Cliente.PrincipalCli import main as cliente_main
from Servidor.PrincipalSrv import main as servidor_main

def run_cliente():
    cliente_main()

def run_servidor():
    servidor_main()

if __name__ == "__main__":
    # Iniciar el servidor en un hilo separado
    servidor_thread = threading.Thread(target=run_servidor)
    servidor_thread.start()

    # Iniciar el cliente en el hilo principal
    run_cliente()
