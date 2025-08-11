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
            self.mensajesTxt.insert(tk.END, f"Servidor TCP en ejecución: {socket.gethostname()} ,Puerto {self.PORT}\n")
            while True:
                self.clientSocket, addr = self.serverSocket.accept()
                self.in_buffer = self.clientSocket.makefile('r')
                self.out = self.clientSocket.makefile('w')
                threading.Thread(target=self.handleClient).start()
        except socket.error as e:
            self.mensajesTxt.insert(tk.END, f"Error en el servidor: {e}\n")

    def handleClient(self):
        try:
            while True:
                linea = self.in_buffer.readline()
                if not linea:
                    break
                # Usa after() para actualizar la GUI desde el hilo principal
                self.root.after(0, self.mensajesTxt.insert, tk.END, f"Cliente: {linea}")
                self.root.after(0, self.mensajesTxt.see, tk.END)  # Para hacer scroll automático

                # Respuesta al cliente
                self.out.write("Mensaje recibido en el server\n")
                self.out.flush()
        except socket.error as e:
            self.root.after(0, self.mensajesTxt.insert, tk.END, f"Error al manejar cliente: {e}\n")
        finally:
            self.clientSocket.close()


def main():
    root = tk.Tk()
    app = PrincipalSrv(root)
    root.mainloop()