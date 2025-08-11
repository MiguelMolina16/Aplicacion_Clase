import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

class PrincipalCli:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente")
        self.socket = None
        self.out = None
        self.in_buffer = None

        # Campo para IP
        self.label_ip = tk.Label(root, text="IP del servidor:", font=("Verdana", 10))
        self.label_ip.place(x=30, y=10, width=120, height=25)

        self.entry_ip = tk.Entry(root, font=("Verdana", 10))
        self.entry_ip.place(x=160, y=10, width=150, height=25)
        self.entry_ip.insert(0, "localhost")  # valor por defecto

        # Campo para Puerto
        self.label_port = tk.Label(root, text="Puerto:", font=("Verdana", 10))
        self.label_port.place(x=30, y=45, width=120, height=25)

        self.entry_port = tk.Entry(root, font=("Verdana", 10))
        self.entry_port.place(x=160, y=45, width=150, height=25)
        self.entry_port.insert(0, "12345")  # valor por defecto

        self.bConectar = tk.Button(root, text="CONECTAR", font=("Segoe UI", 12), command=self.bConectarActionPerformed)
        self.bConectar.place(x=320, y=10, width=130, height=60)

        self.jLabel1 = tk.Label(root, text="CLIENTE TCP : DFRACK", font=("Tahoma", 14, "bold"), fg="red")
        self.jLabel1.place(x=110, y=80, width=250, height=17)

        self.mensajesTxt = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=5, state=tk.DISABLED)
        self.mensajesTxt.place(x=30, y=210, width=410, height=110)

        self.mensajeTxt = tk.Entry(root, font=("Verdana", 14))
        self.mensajeTxt.place(x=40, y=120, width=350, height=30)

        self.jLabel2 = tk.Label(root, text="Mensaje:", font=("Verdana", 14))
        self.jLabel2.place(x=20, y=90, width=120, height=30)

        self.btEnviar = tk.Button(root, text="Enviar", font=("Verdana", 14), command=self.btEnviarActionPerformed)
        self.btEnviar.place(x=327, y=160, width=120, height=27)

        self.root.geometry("491x375")
        self.root.resizable(False, False)

    def bConectarActionPerformed(self):
        ip = self.entry_ip.get()
        port_text = self.entry_port.get()
        if not ip or not port_text:
            messagebox.showerror("Error", "Debes ingresar IP y puerto")
            return
        try:
            port = int(port_text)
            self.connect_to_server(ip, port)
            messagebox.showinfo("Conectado", f"Conectado a {ip}:{port}")
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
        except socket.error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar: {e}")

    def btEnviarActionPerformed(self):
        self.enviarMensaje()

    def connect_to_server(self, ip, port):
        if self.socket is None or self.socket.fileno() == -1:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((ip, port))
            self.out = self.socket.makefile('w')
        self.in_buffer = self.socket.makefile('r')
        threading.Thread(target=self.recibirMensajes, daemon=True).start()

    def recibirMensajes(self):
        try:
            while True:
                fromServer = self.in_buffer.readline()
                if not fromServer:
                    break
                self.mensajesTxt.config(state=tk.NORMAL)
                self.mensajesTxt.insert(tk.END, "Servidor: " + fromServer + "\n")
                self.mensajesTxt.see(tk.END)
                self.mensajesTxt.config(state=tk.DISABLED)
        except socket.error as e:
            print(f"Error al recibir mensajes: {e}")

    def enviarMensaje(self):
        if self.out:
            self.out.write(self.mensajeTxt.get() + "\n")
            self.out.flush()
            self.mensajeTxt.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = PrincipalCli(root)
    root.mainloop()
