import folium as fm
from numpy import infty
import webbrowser
from panels import *
import customtkinter as ctk
from tkinter import messagebox


class Menu(ctk.CTkTabview):
  def __init__(self, parent, graph, app):
    super().__init__(parent)
    self.grid(row=0, column=0, sticky='nsew')

    #tabs
    self.add('Grafo de Aeropuertos')
    self.add('Información de un Aeropuerto')
    self.add('Caminos Mínimos Más Largos')
    self.add('Camino Mínimo')

    #frames
    GraphPanel(self.tab('Grafo de Aeropuertos'), graph, app)
    InfoFrame(self.tab('Información de un Aeropuerto'),graph, app)
    self.longestPathFrame = LongestPathFrame(self.tab('Caminos Mínimos Más Largos'), graph, app)
    MinPathFrame(self.tab('Camino Mínimo'), graph, app) 

  
class GraphPanel(ctk.CTkFrame):
  def __init__(self, parent, graph, app):
      super().__init__(parent, fg_color='transparent')
      self.pack(expand=True, fill='both')

      
      self.graphInfo(graph)

  def graphInfo(self, graph):

      # Utilizar el graph guardado en el panel
      isConnected = graph.isConnected()
      connectedComponents = graph.connectedComponents()
      weight = graph.findMinimumSpanningTrees()

      # Crear un nuevo panel o mostrar información
      GraphInfoPanel(self, isConnected, connectedComponents, weight)

   
class InfoFrame(ctk.CTkFrame):
  def __init__(self, parent, graph, app):
    super().__init__(parent, fg_color='transparent')
    self.pack(expand=True, fill='both')

    def searchCommand(entry):
      return lambda: self.searchAirport(entry, graph) 
    
    self.infoPanel = None
    SimplePanel(self, 'Ingrese el código del aeropuerto a buscar: ', 'Buscar Aeropuerto', searchCommand)
  
  def searchAirport(self, entry, graph):
    code = entry.get().upper()
    if self.infoPanel: self.infoPanel.destroy()
    vertex = graph.getVertex(code)
    if vertex:
      self.infoPanel = InfoPanel(self, vertex.data['Name'], vertex.data['City'], vertex.data['Country'], vertex.data['Latitude'], vertex.data['Longitude']  )
    else:
      messagebox.showerror('Error', 'El aeropuerto no existe en la base de datos.')
      entry.delete(0, 'end')

class LongestPathFrame(ctk.CTkFrame):
  def __init__(self, parent, graph, app):
    super().__init__(parent, fg_color='transparent')
    self.pack(expand=True, fill='both')

     # Layout
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    # Scrollable Frame
    self.scroll_frame = ctk.CTkScrollableFrame(self)
    self.scroll_frame.pack(fill='both', expand=True)


    def searchCommand(entry):
      return lambda: self.searchLongestPath(entry, graph) 
    
    self.infoPanel = None
    SimplePanel(self.scroll_frame, 'Ingrese el código del aeropuerto de origen: ', 'Ver Rutas', searchCommand)

  def searchLongestPath(self, entry, graph):
    code = entry.get().upper()
    vertex = graph.getVertex(code)
    if self.infoPanel: self.infoPanel.destroy()
    minPaths = graph.dijkstra(vertex)
    minPaths = {
      key: minPaths[key]
      for key in sorted( minPaths, key=lambda x: minPaths[x][0], reverse = True)
      if not minPaths[key][0] == infty
    }
  
    i = 0
    for airport in minPaths:
      pathAux = graph.getPath(minPaths, vertex, airport)
      path = pathAux[pathAux.index('(') + 1:pathAux.index(')')].split('->')
      LongestPathPanel(self.scroll_frame, graph.getPath(minPaths, vertex, airport), float(path[0]))
      InfoPanel(self.scroll_frame, airport.data['Name'], airport.data['City'], airport.data['Country'], airport.data['Latitude'], airport.data['Longitude'])
      i += 1
      if i>=10:
        break

class MinPathFrame(ctk.CTkFrame):
  def __init__(self, parent, graph, app):
    super().__init__(parent, fg_color='transparent')
    self.pack(expand=True, fill='both')

    def minPathCommand(entry):
      return lambda: self.minPath(entry, graph)
  
    self.infoPanel = None
    self.panel1 = SimplePanel(self, 'Ingrese el código del aeropuerto de origen: ', None, None)
    SimplePanel(self, 'Ingrese el código del aeropuerto de destino: ', 'Ver Camino Mínimo', minPathCommand)
  
  def generateMap(self, graph, airportCodes, code):
    airports = graph.data
    map = fm.Map(location=[20, 0], zoom_start=2)
    startLocation = None
    for code in airportCodes:
      for airport in airports:
        if airport['Code'] == code:
          location = [airport['Latitude'], airport['Longitude']]
          if not startLocation:
            startLocation = location
          fm.Marker(location, popup=airport['Name']).add_to(map)
          actualLocation = location
          if startLocation and actualLocation:
            fm.PolyLine([startLocation, actualLocation], color='blue').add_to(map)
            startLocation = actualLocation

    map.save('map.html')
    webbrowser.open_new_tab('map.html')

  def minPath(self, entry, graph):
    codeDestination = entry.get().upper()
    codeSource = self.panel1.winfo_children()[1].get().upper()
    if not codeSource or not codeDestination:
      messagebox.showerror('Error', 'Debe ingresar dos códigos de aeropuertos.')
      entry.delete(0, 'end')
      return
    source = graph.getVertex(codeSource)
    destination = graph.getVertex(codeDestination)
    if not source or not destination:
      messagebox.showerror('Error', 'Uno o ambos aeropuertos no existen en la base de datos.')
      entry.delete(0, 'end')
      return
    if self.infoPanel: self.infoPanel.destroy()
    self.infoPanel = InfoPanel(self, destination.data['Name'], destination.data['City'], destination.data['Country'], destination.data['Latitude'], destination.data['Longitude']  )
    minPaths = graph.dijkstra(source)
    minPaths = {
      key: minPaths[key]
      for key in sorted( minPaths, key=lambda x: minPaths[x][0], reverse = True)
      if not minPaths[key][0] == infty
    }
    pathAux = graph.getPath(minPaths, source, destination)
    path = pathAux[pathAux.index('(') + 1:pathAux.index(')')].split('->')
    LongestPathPanel(self,  graph.getPath(minPaths, source, destination), float(path[0]))
    minPath = graph.getPath(minPaths, source, destination)
    airportCodes = []
    if '(' in minPath:
      minPath = minPath[minPath.index('): ') + 3:]
      airportCodes = minPath.split(' -> ')
    self.generateMap(graph, airportCodes, codeSource)
    