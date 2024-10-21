import customtkinter as ctk
from dataset import globe
from menu import Menu

class App(ctk.CTk):
  def __init__(self):
    super().__init__()
    ctk.set_appearance_mode('light')
    ctk.set_default_color_theme('blue')
    self.geometry('500x600')
    self.title('Grafo Aeropuertos')
    self.minsize(300,400)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=4, uniform='a')

    self.graph = globe

    self.menu = Menu(self, self.graph, self)

    self.mainloop()

App() 

