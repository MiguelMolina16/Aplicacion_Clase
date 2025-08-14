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
    servidor_thread.start() # inicia

    # Iniciar el primer cliente en un hilo separado
    cliente_thread_1 = threading.Thread(target=run_cliente)
    cliente_thread_1.start()

    # Iniciar el segundo cliente en otro hilo separado
    cliente_thread_2 = threading.Thread(target=run_cliente)
    cliente_thread_2.start()

    # Esperar a que todos los hilos terminen
    servidor_thread.join() # cada join impide que el programa se cierre y solo hasta que se terminen todos éste acaba
    cliente_thread_1.join()
    cliente_thread_2.join()
