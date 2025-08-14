import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

class PrincipalSrv:
    def __init__(self, root):
        self.root = root
        self.root.title("Servidor ...")
        self.PORT = 12345
        self.serverSocket = None
        self.clientSocket = None
        self.in_buffer = None
        self.out = None

        self.bIniciar = tk.Button(root, text="INICIAR SERVIDOR", font=("Segoe UI", 18), command=self.bIniciarActionPerformed)
        self.bIniciar.place(x=100, y=90, width=250, height=40)

        self.jLabel1 = tk.Label(root, text="SERVIDOR TCP : HOEL", font=("Tahoma", 14, "bold"), fg="red")
        self.jLabel1.place(x=150, y=10, width=160, height=17)

        self.mensajesTxt = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=5)
        self.mensajesTxt.place(x=20, y=160, width=410, height=70)

        self.root.geometry("491x290")
        self.root.resizable(False, False)

    def bIniciarActionPerformed(self):
        messagebox.showinfo("Iniciando", "Iniciando servidor")
        self.iniciarServidor()

    def iniciarServidor(self):
        threading.Thread(target=self.runServer).start()

    def runServer(self):
        try:
            self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serverSocket.bind(("", self.PORT))
            self.serverSocket.listen(5)
            self.mensajesTxt.insert(tk.END, f"Servidor TCP en ejecución: {socket.gethostname()} , Puerto {self.PORT}\n")
            while True:
                client_socket, addr = self.serverSocket.accept()
                self.mensajesTxt.insert(tk.END, f"Cliente conectado desde {addr}\n")
                client_thread = threading.Thread(target=self.handleClient, args=(client_socket,))
                client_thread.start()
        except socket.error as e:
            self.mensajesTxt.insert(tk.END, f"Error en el servidor: {e}\n")


    def handleClient(self, client_socket):
        try:
            in_buffer = client_socket.makefile('r')
            out = client_socket.makefile('w')

            # Leer primer mensaje del cliente con su ID y IP destino
            init_line = in_buffer.readline().strip()
            cliente_id = "desconocido"
            cliente_destino = "?"

            if init_line.startswith("ID:") and ";IP:" in init_line:
                try:
                    # Parseo del mensaje: ID:cliente_1;IP:127.0.0.1:12345
                    id_part, ip_part = init_line.split(";")
                    cliente_id = id_part.split(":")[1]
                    ip = ip_part.split(":")[1]
                    port = ip_part.split(":")[2]
                    cliente_destino = f"{ip}:{port}"
                except Exception as e:
                    print(f"[ERROR] al procesar línea inicial: {e}")

            # Mostrar conexión en el servidor
            self.root.after(0, self.mensajesTxt.insert, tk.END,
                            f"Conectado {cliente_id} a {cliente_destino}\n")
            self.root.after(0, self.mensajesTxt.see, tk.END)

            # Bucle para recibir mensajes del cliente
            while True:
                linea = in_buffer.readline()
                if not linea:
                    break
                self.root.after(0, self.mensajesTxt.insert, tk.END,
                                f"{cliente_id}: {linea}")
                self.root.after(0, self.mensajesTxt.see, tk.END)

                out.write("Mensaje recibido en el server\n")
                out.flush()

        except Exception as e:
            self.root.after(0, self.mensajesTxt.insert, tk.END,
                            f"[ERROR] Cliente {cliente_id}: {e}\n")
        finally:
            client_socket.close()





def main():
    root = tk.Tk()
    app = PrincipalSrv(root)
    root.mainloop()