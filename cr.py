#import sqlite3
#con = sqlite3.connect("db")
class JuegoCarreras:    #Clase padre para juegos de carreras, contiene datos privados y su inicializacion
  __id=0
  __jugadores = []
  __pistas = []
  __vehiculos = []
  __recorrido = []

  def Iniciarjuego(self):
    pass

class CarreraCarros(JuegoCarreras):   #Heredando de JuegoCarreras, crea una carrera de carros
  def __init__(self):
    self.__pistas = [["Arena",1], ["Asfalto", 1.5], ["Nieve", 2]]

class JugarCarrera:   #Operacion de un juego de carreras
  def moverVehiculo(self):
    pass

  def evaluarGanador(self):
    pass

class Imprimir:   #Impresiones genericas para un juego de carreras
  __DATA = [''' 
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       %%%%%                           */¨\*   %%%%%  
       %%%  */¨\*                       (3)     %%%  
       %%    (7)           */¨\*       *\./*    %%
     %% ====*\./*==|WELCOME TO RECE|========== %%
    %%  */¨\*     (4)      *\./*  */¨\*      %%   
   %%%   (1)     *\./*             (9)      %%%         
  %%%%% *\./*                     *\./*  %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%''']


  def imprimir(self):
    print(self.__DATA[0])

if __name__ == '__main__':
  imp=Imprimir()
  imp.imprimir() 
 