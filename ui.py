import tkinter as tk
from tkinter import messagebox
import app
import app.server
import threading 


PORT = None
def aceptar():
    global PORT
    puerto = entry_puerto.get()
    PORT = int(puerto )
    if puerto.isdigit():
        messagebox.showinfo("Información", f"Servidor configurado en el puerto: {puerto}")
        root.destroy()
    else:
        messagebox.showerror("Error", "Por favor, ingrese un número de puerto válido.")

def cancelar():
    root.destroy()

root = tk.Tk()
root.title("Configuración del Servidor")
root.geometry("300x150")    

label_puerto = tk.Label(root, text="Ingrese el puerto del servidor:")
label_puerto.pack(pady=10)

entry_puerto = tk.Entry(root, width=20)
entry_puerto.pack(pady=5)

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

btn_aceptar = tk.Button(frame_botones, text="Aceptar", command=aceptar)
btn_aceptar.pack(side="left", padx=10)

btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=cancelar)
btn_cancelar.pack(side="right", padx=10)



root.mainloop()
root.update()



app.server.run(port=PORT)
