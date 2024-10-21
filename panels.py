import customtkinter as ctk

class Panel(ctk.CTkFrame):
  def __init__(self, parent):
    super().__init__(parent, fg_color='#EEEEEE')
    self.pack(fill='x', pady=4, ipady=8)


class GraphInfoPanel(ctk.CTkFrame):
  def __init__(self, parent, isConnected, connectedComponents, weight):
      super().__init__(parent, fg_color='transparent')
      self.pack(expand=True, fill='both')
      self.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)
      self.columnconfigure((0,1), weight=1)
      ctk.CTkLabel(self, text="Información del Grafo", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=0, column=0, padx=4, sticky='w')
      # ¿Es conexo?
      ctk.CTkLabel(self, text=f"¿Es conexo?: {'Sí' if isConnected else 'No'}", font=ctk.CTkFont(family="Roboto", size=14)).grid(row=1, column=0, padx=4, sticky='w')
      if not isConnected:
        ctk.CTkLabel(self, text=f"Número de componentes: {len(connectedComponents)}", font=ctk.CTkFont(family="Roboto", size=14)).grid(row=2, column=0, padx=4, sticky='w')

        # Obtener el peso del árbol de expansión mínima para cada componente
        mst_weights = weight  # Suponiendo que weight es el resultado de findMinimumSpanningTrees()

        for idx, component in enumerate(connectedComponents):
            num_vertices = component[1]  # Número de vértices en la componente
            component_key = tuple(component[0])  # Convertir la lista de vértices a tupla para usar como clave
            mst_weight = mst_weights.get(component_key, 'No disponible')  # Obtener peso del MST

            # Mostrar la información de la componente
            ctk.CTkLabel(self, text=f"Componente {idx + 1}:", font=ctk.CTkFont(family="Roboto", size=14)).grid(row=3 + idx * 3, column=0, padx=4, sticky='w')
            ctk.CTkLabel(self, text=f"Número de vértices: {num_vertices}", font=ctk.CTkFont(family="Roboto", size=12)).grid(row=4 + idx * 3, column=0, padx=4, sticky='w')
            ctk.CTkLabel(self, text=f"Peso del Árbol de Expansión Mínima: {mst_weight}", font=ctk.CTkFont(family="Roboto", size=12)).grid(row=5 + idx * 3, column=0, padx=4, sticky='w')

          


class SimplePanel(Panel):
  def __init__(self, parent, text, text_button, button_command):
    super().__init__(parent)

    #layout
    self.rowconfigure((0,1), weight=1)
    self.columnconfigure((0,1), weight=1)

    ctk.CTkLabel(self, text=text, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=0, padx=4, sticky='w')
    entry = ctk.CTkEntry(self, font=ctk.CTkFont(family="Roboto", size=14))
    entry.grid(row=1, column=0, columnspan=2, sticky='ew', padx=4, pady=4)
    if button_command and text_button:
      ctk.CTkButton(self, text=text_button, font=ctk.CTkFont(family="Roboto", size=14), corner_radius=5, command=button_command(entry)).grid(row=2, column=1, sticky='e', padx=4, pady=4)

class InfoPanel(Panel):
  def __init__(self, parent, name, city, country, latitude, longitude):
    super().__init__(parent)

    #layout
    self.rowconfigure((0,1,2,3,4), weight=1)
    self.columnconfigure((0,1), weight=1)

    ctk.CTkLabel(self, text="Nombre:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=0, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=name, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=0, column=1, padx=4, sticky='w')
    ctk.CTkLabel(self, text="Ciudad:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=1, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=city, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=1, column=1, padx=4, sticky='w')
    ctk.CTkLabel(self, text="País:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=2, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=country, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=2, column=1, padx=4, sticky='w')
    ctk.CTkLabel(self, text="Latitud:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=3, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=latitude, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=3, column=1, padx=4, sticky='w')
    ctk.CTkLabel(self, text="Longitud:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=4, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=longitude, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=4, column=1, padx=4, sticky='w')

class LongestPathPanel(Panel):
  def __init__(self, parent, minPaths, distance):
    super().__init__(parent)

    #layout
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    ctk.CTkLabel(self, text="Camino:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=0, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=minPaths, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=0, column=1, padx=4, sticky='w')
    ctk.CTkLabel(self, text="Distancia:", font=ctk.CTkFont(family="Roboto", size=14, weight="bold")).grid(row=1, column=0, padx=4, sticky='w')
    ctk.CTkLabel(self, text=distance, font=ctk.CTkFont(family="Roboto", size=14)).grid(row=1, column=1, padx=4, sticky='w')