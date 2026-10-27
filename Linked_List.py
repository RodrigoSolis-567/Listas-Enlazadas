import tkinter as tk
from tkinter import messagebox, simpledialog
from MyLinkedList import MyLinkedList

class DialogoOpciones(tk.Toplevel):
    def __init__(self, parent, titulo, opciones):
        super().__init__(parent)
        self.title(titulo)
        self.geometry("320x260")
        self.config(bg="#1e1e2f")
        self.resizable(False, False)
        
        self.transient(parent)
        self.lift()
        self.attributes('-topmost', True)
        self.grab_set()

        # Centrar la ventana en la pantalla
        self.update_idletasks()
        ancho_ventana = 320
        alto_ventana = 260
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        self.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

        self.resultado = None
        self.opcion_var = tk.StringVar(value=opciones[0])

        tk.Label(self, text=titulo, font=("Arial", 12, "bold"), fg="white", bg="#1e1e2f").pack(pady=15)

        for op in opciones:
            rb = tk.Radiobutton(
                self, text=op.capitalize(), variable=self.opcion_var, value=op,
                font=("Arial", 10, "bold"), fg="white", bg="#1e1e2f", 
                selectcolor="#3182ce",
                activebackground="#1e1e2f", activeforeground="white",
                highlightthickness=0
            )
            rb.pack(anchor="w", padx=60, pady=5)

        btn_aceptar = tk.Button(
            self, text="Aceptar", bg="#4e73df", fg="white", font=("Arial", 10, "bold"),
            width=12, command=self.on_aceptar, relief="flat"
        )
        btn_aceptar.pack(pady=20)
        
        self.focus_force()

    def on_aceptar(self):
        self.resultado = self.opcion_var.get()
        self.destroy()


class VisualLinkedListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de MyLinkedList")
        self.root.geometry("1050x680")
        self.root.config(bg="#1e1e2f")

        self.lista = MyLinkedList()
        self.indice_buscado = -1

        titulo = tk.Label(root, text="Visualizador Gráfico de MyLinkedList", font=("Arial", 18, "bold"), fg="white", bg="#1e1e2f")
        titulo.pack(pady=10)

        frame_controles = tk.Frame(root, bg="#1e1e2f")
        frame_controles.pack(pady=10)

        btn_insertar = tk.Button(frame_controles, text="Insertar Valor", bg="#4e73df", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.menu_insertar)
        btn_insertar.grid(row=0, column=0, padx=5)

        btn_buscar = tk.Button(frame_controles, text="Buscar Casilla", bg="#1cc88a", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.menu_buscar)
        btn_buscar.grid(row=0, column=1, padx=5)

        btn_eliminar = tk.Button(frame_controles, text="Eliminar Casilla", bg="#e74a3b", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.menu_eliminar)
        btn_eliminar.grid(row=0, column=2, padx=5)

        btn_enlazar = tk.Button(frame_controles, text="Modificar Enlace", bg="#f6c23e", fg="black", font=("Arial", 10, "bold"), padx=10, command=self.menu_enlazar)
        btn_enlazar.grid(row=0, column=3, padx=5)

        btn_reiniciar = tk.Button(frame_controles, text="Actualizar Vista", bg="#858796", fg="white", font=("Arial", 10, "bold"), padx=10, command=self.actualizar_canvas)
        btn_reiniciar.grid(row=0, column=4, padx=5)

        # Contenedor con soporte de Scrollbar horizontal
        self.canvas_frame = tk.Frame(root, bg="#1e1e2f")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.canvas = tk.Canvas(self.canvas_frame, bg="#2d3748", highlightthickness=0)
        self.h_scrollbar = tk.Scrollbar(self.canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.h_scrollbar.set)

        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.actualizar_canvas()

    def menu_insertar(self):
        dialogo = DialogoOpciones(self.root, "Selecciona tipo de inserción", ["inicio", "final", "medio"])
        self.root.wait_window(dialogo)

        if not dialogo.resultado:
            return

        tipo = dialogo.resultado
        valor = simpledialog.askstring("Valor", "Ingresa el valor del nodo:", parent=self.root)
        if valor is None:
            return

        try:
            if tipo == 'inicio':
                self.lista.insertFront(valor)
            elif tipo == 'final':
                self.lista.insertEnd(valor)
            elif tipo == 'medio':
                idx = simpledialog.askinteger("Posición", "Ingresa el número de casilla (ej. 1, 2...):", parent=self.root)
                if idx is not None:
                    self.lista.insertAt(idx - 1, valor)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)
        
        self.actualizar_canvas()

    def menu_buscar(self):
        idx = simpledialog.askinteger("Buscar Casilla", "Ingresa el número de casilla a buscar:", parent=self.root)
        if idx is None:
            return

        try:
            internal_idx = idx - 1
            nodo = self.lista.LinkSearch[internal_idx]
            self.indice_buscado = internal_idx
            self.actualizar_canvas()

            val_str = "None" if nodo is None else str(nodo.valor)
            messagebox.showinfo("Casilla Encontrada", f"Posición: [{idx}]\nValor Asignado: {val_str}", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)
            self.indice_buscado = -1
            self.actualizar_canvas()

    def menu_eliminar(self):
        dialogo = DialogoOpciones(self.root, "Selecciona método de eliminación", ["borrar", "none"])
        self.root.wait_window(dialogo)

        if not dialogo.resultado:
            return

        opcion = dialogo.resultado
        idx = simpledialog.askinteger("Posición", "Ingresa el número de casilla:", parent=self.root)
        if idx is None:
            return

        try:
            internal_idx = idx - 1
            if opcion == 'borrar':
                self.lista.delete(internal_idx)
            elif opcion == 'Vaciar':
                self.lista.deleteNull(internal_idx)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

        self.indice_buscado = -1
        self.actualizar_canvas()

    def menu_enlazar(self):
        pos_origen = simpledialog.askinteger("Modificar Enlace", "Ingresa el número de la casilla origen:", parent=self.root)
        if pos_origen is None:
            return
        pos_destino = simpledialog.askinteger("Modificar Enlace", "Ingresa el número de la casilla destino a enlazar:", parent=self.root)
        if pos_destino is None:
            return

        try:
            self.lista.linkPositions(pos_origen - 1, pos_destino - 1)
            messagebox.showinfo("Éxito", f"¡La casilla [{pos_origen}] ahora conecta con la casilla [{pos_destino}]!", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

        self.actualizar_canvas()

    def actualizar_canvas(self):
        self.canvas.delete("all")
        secuencia = self.lista.secuencia_lineal()

        if not secuencia:
            self.canvas.create_text(500, 250, text="La lista enlazada está vacía.", font=("Arial", 14), fill="#a0aec0")
            self.canvas.config(scrollregion=(0, 0, 1000, 500))
            return

        x_inicial = 60
        y_inicial = 280
        ancho_bloque = 90
        alto_bloque = 80
        espacio = 60

        # Ancho total dinámico para la barra de desplazamiento horizontal
        ancho_total = max(1000, x_inicial + len(secuencia) * (ancho_bloque + espacio) + 100)
        self.canvas.config(scrollregion=(0, 0, ancho_total, 550))

        coordenadas_bloques = []

        # 1. Dibujar bloques de la lista
        for i, nodo in enumerate(secuencia):
            num_visual = i + 1
            x1 = x_inicial + i * (ancho_bloque + espacio)
            y1 = y_inicial
            x2 = x1 + ancho_bloque
            y2 = y1 + alto_bloque

            coordenadas_bloques.append((x1, y1, x2, y2))

            color_borde = "#3182ce" if self.indice_buscado != i else "#4fd1c5"

            # Contorno general de la caja
            self.canvas.create_rectangle(x1, y1, x2, y2, outline=color_borde, width=3)
            
            # Cabecera superior
            self.canvas.create_rectangle(x1, y1, x2, y1 + 30, fill="#3182ce", outline=color_borde, width=1)
            self.canvas.create_text((x1 + x2) / 2, y1 + 15, text=f"[{num_visual}]", font=("Arial", 9, "bold"), fill="white")

            # Centro de la caja (blanco)
            self.canvas.create_rectangle(x1, y1 + 30, x2, y2, fill="white", outline=color_borde, width=1)

            # Valor dentro del cuadro
            val_texto = "None" if nodo is None else str(nodo.valor)
            color_texto = "#e53e3e" if nodo is None else "#1a202c"
            self.canvas.create_text((x1 + x2) / 2, (y1 + 30 + y2) / 2, text=val_texto, font=("Arial", 12, "bold"), fill=color_texto)

        # 2. Dibujar conexiones predeterminadas y enlaces personalizados múltiples
        for idx, nodo in enumerate(secuencia):
            x1, y1, x2, y2 = coordenadas_bloques[idx]
            centro_x = (x1 + x2) / 2
            centro_y = (y1 + y2) / 2

            # Recopilar todos los destinos personalizados activos de este nodo
            destinos_activos = []
            if nodo is not None and hasattr(nodo, "siguientes") and len(nodo.siguientes) > 0:
                for destino_nodo in nodo.siguientes:
                    if destino_nodo in secuencia:
                        destinos_activos.append(secuencia.index(destino_nodo))

            # Si tiene enlaces personalizados, se dibujan como puentes cuadrados blancos
            if len(destinos_activos) > 0:
                for i_dest, idx_destino in enumerate(destinos_activos):
                    dest_x1, _, dest_x2, _ = coordenadas_bloques[idx_destino]
                    destino_px = (dest_x1 + dest_x2) / 2
                    
                    altura_puente = y1 - 35 - (abs(idx - idx_destino) * 12) - (i_dest * 15)
                    
                    self.canvas.create_line(
                        centro_x, y1,
                        centro_x, altura_puente,
                        destino_px, altura_puente,
                        destino_px, y1,
                        arrow=tk.LAST, fill="white", width=2, smooth=False
                    )
            else:
                # Si NO tiene enlaces personalizados, dibujar flecha lineal SOLO si el nodo actual y el siguiente NO son None
                if idx < len(secuencia) - 1:
                    sig_nodo = secuencia[idx + 1]
                    if nodo is not None and sig_nodo is not None:
                        sig_x1, _, _, _ = coordenadas_bloques[idx + 1]
                        self.canvas.create_line(x2, centro_y, sig_x1, centro_y, arrow=tk.LAST, fill="#cbd5e0", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualLinkedListApp(root)
    root.mainloop()