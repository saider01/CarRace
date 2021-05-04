from random import randint
import sqlite3
    
class Vehiculo:   #Vehiculo generico para carreras
  __distancia = 0   #recorrido actual en la carrera
  __carril = 0
  __numero = []

  def __init__(self, num, car):
    self.__carril = car
    self.__numero = num

  def getNumero(self):
    return self.__numero

  def setDistancia(self, dis):
    self.__distancia += dis

  def getDistancia(self):
    return self.__distancia

class Pista:    #Pista generica para careras
  __tipoPistas = ""
  __longitud = 0

  def __init__(self, nom, lon):
    self.__tipoPistas = nom
    self.__longitud = lon

  def getLongitud(self):
    return self.__longitud

class Jugador:    #Jugador generico para carreras
  __vehiculo = 0  #Numero del vehiculo asignado
  __nombre = ""

  def __init__(self, veh, nom):
    self.__vehiculo = veh
    self.__nombre = nom

  def setNombre(self, nom):
    self.__nombre = nom

  def setVehiculo(self, veh):
    self.__vehiculo = veh

  def getNombre(self):
    return self.__nombre

class Guardar:
  @staticmethod
  def iniciarDb():    #retorna conexion y cursor para manejar la db
    try:
      conect = sqlite3.connect('data.db')
      return conect, conect.cursor()
    except:
      print("Database Error")
     

  @staticmethod
  def guardar(con, cur, podio):
    cur.execute("CREATE TABLE IF NOT EXISTS partidas(id integer PRIMARY KEY, primero text, segundo text, tercero text)")
    cur.execute("INSERT INTO partidas(primero, segundo, tercero) VALUES(?, ?, ?)", (podio[0], podio[1], podio[2]))
    con.commit()

  @staticmethod
  def consultar():    #Imprime tabla de resultados
    con, cur = Guardar.iniciarDb()
    cur.execute("SELECT * FROM partidas")
    print("Id\tprimero\t\tsegundo\t\ttercero\n")
    [print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}") for row in cur.fetchall()]
    print("\n")


class CarreraCarros():
  __id = 0
  __pistas = Pista(["Arena","Asfalto", "Nieve"], 1500)
  __podio = []

  def __init__(self, jug):    #Crea vehiculos(asigna numero y carril) y jugadores(asigna vehiculo y nombre)
    jugadoresLen = len(jug)   #Cuantos jugadores hay en total
    self.__vehiculos = [Vehiculo(randint(0,99), i) for i in range(jugadoresLen)]
    self.__jugadores = [Jugador(0, "") for i in range(jugadoresLen)]
    for i in range(jugadoresLen):
      self.__jugadores[i].setNombre(jug[i])
      self.__jugadores[i].setVehiculo(self.__vehiculos[i].getNumero())

  def jugar(self):                                                          # Asigna de 100m-600m de avance a cada vehiculo
    longitudPista = self.__pistas.getLongitud()
    maxPodios = 3 if len(self.__jugadores) > 3 else len(self.__jugadores)-1 # Verificar si hay 2 o mas jugadores para asignar en podio 
    while len(self.__podio) <= maxPodios:                                   # Iterar para verificar ganadores
      for i in range(len(self.__vehiculos)):                                # Iterar sobre cada vehiculo (tirar dado)
        if self.__vehiculos[i].getDistancia() >= longitudPista:             # Si vehiculo supero la meta
          if self.__jugadores[i].getNombre() not in self.__podio:           #   Y ademas no esta conductor en podio
            self.__podio.append(self.__jugadores[i].getNombre())            #     LLeve el conductor al podio
        else:                                                               
          self.__vehiculos[i].setDistancia(100*randint(1,6))                # Sino haga avance aleatorio a vehiculo (100m-600m)
    if len(self.__podio) < 3:                                               # Cuando hay 2 jugadores el 3er lugar se llena con espacio 
      self.__podio.append(" ")
    con, cur = Guardar.iniciarDb()
    Guardar.guardar(con, cur, self.__podio)                                 # El orden de __podio es el orden de llegada

if __name__ == '__main__':
  print(''' 
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
       %%%%%                           */¨\*   %%%%%  
       %%%  */¨\*                       (3)     %%%  
       %%    (7)           */¨\*       *\./*    %%
     %% ====*\./*=|CARRERAS DE CARROS|======== %%
    %%  */¨\*     (4)      *\./*  */¨\*      %%   
   %%%   (1)     *\./*             (9)      %%%         
  %%%%% *\./*                     *\./*  %%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%''')
  menu = int(input(f"\t\t\tMENU\n(1) Jugar\n(2) Ver Ganadores\n"))
  if menu == 1:
    jugadorHumanoLen = int(input("\nIngrese numero de jugadores humanos [1-4]: ")) 
    jugadorHumanoLen = 1 if jugadorHumanoLen not in [1,2,3,4] else jugadorHumanoLen
    jugadorHumano = [input(f"Jugador humano {i}: ") for i in range(jugadorHumanoLen)]
    jugadorMaquinaLen = int(input("Ingrese numero de jugadores maquina [1-4]: "))
    jugadorMaquinaLen = 4 if jugadorMaquinaLen not in [1,2,3,4] else jugadorMaquinaLen
    jugadorMaquina = ["jugador"+str(i) for i in range(jugadorMaquinaLen)]
    carrera = CarreraCarros(jugadorHumano+jugadorMaquina)
    carrera.jugar()
  if menu == 2:
    Guardar.consultar()

  