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
  __dificultad =  []

  def __init__(self, nom, lon, dif):
    self.__tipoPistas = nom
    self.__longitud = lon
    self.__dificultad = dif

  def getLongitud(self):
    return self.__longitud

  def getDificultad(self, pista):
    return self.__dificultad[self.__tipoPistas.index(pista)]
  
  def getTipo(self):
    return self.__tipoPistas

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
  def consultar():    #Imprime historico de resultados
    con, cur = Guardar.iniciarDb()
    cur.execute("SELECT * FROM partidas")
    print("Id\tprimero\t\tsegundo\t\ttercero\n")
    [print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}") for row in cur.fetchall()]
    print("\n")


class CarreraCarros():
  __id = 0
  __pistas = Pista(["Asfalto","Arena", "Nieve"], 1500,[1,2,3])
  __pistaUso = ""
  __podio = []

  def __init__(self, jug):    #Crea vehiculos(asigna numero y carril) y jugadores(asigna vehiculo y nombre)
    jugadoresLen = len(jug)   #Cuantos jugadores hay en total
    self.__carros = [Vehiculo(randint(0,99), i) for i in range(jugadoresLen)]
    self.__jugadores = [Jugador(0, "") for i in range(jugadoresLen)]
    for i in range(jugadoresLen):
      self.__jugadores[i].setNombre(jug[i])
      self.__jugadores[i].setVehiculo(self.__carros[i].getNumero())

  def setPista(self, pis):
    self.__pistaUso = self.__pistas.getTipo()[pis-1]
  
  def getPistas(self):
    return self.__pistas.getTipo()

  def getPodio(self):
    return self.__podio

  def jugar(self):                                                          # Asigna de 100m-600m de avance a cada vehiculo
    longitudPista = self.__pistas.getLongitud()
    maxPodios = 3 if len(self.__jugadores) > 3 else len(self.__jugadores)-1 # Verificar si hay 2 o mas jugadores para asignar en podio 
    while len(self.__podio) <= maxPodios:                                   # Iterar para verificar ganadores
      for i in range(len(self.__carros)):                                   # Iterar sobre cada vehiculo (tirar dado)
        if self.__carros[i].getDistancia() >= longitudPista:                # Si vehiculo supero la meta
          if self.__jugadores[i].getNombre() not in self.__podio:           #   Y ademas no esta conductor en podio
            self.__podio.append(self.__jugadores[i].getNombre())            #     LLeve el conductor al podio
        else:                                                               
          self.__carros[i].setDistancia(100*randint(1,self.__pistas.getDificultad(self.__pistaUso)))  # Sino haga avance aleatorio con dificultad
    if len(self.__podio) < 3:                                               # Cuando hay 2 jugadores el 3er lugar se llena con espacio 
      self.__podio.append(" ")
    con, cur = Guardar.iniciarDb()
    Guardar.guardar(con, cur, self.__podio)                                 # El orden de __podio es el orden de llegada

  def ganadores(self):
    print(f''' 
       %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        GANADORES
        ((( 1 )))===\t\t{self.__podio[0]}     
        ((( 2 )))=====\t\t{self.__podio[1]}  
        ((( 3 )))=======\t{self.__podio[2]}
       ==============================================
                    ''')

def validar(valor):
  if valor.isnumeric():
    return 1 if int(valor) not in [1,2,3,4] else int(valor)
  else:
    return 1

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
    jugadorHumanoLen = validar(input("\nIngrese numero de jugadores humanos [1-4]: "))
    #jugadorHumanoLen = 1 if jugadorHumanoLen not in [1,2,3,4] else jugadorHumanoLen
    jugadorHumano = [input(f"Jugador humano {i}: ") for i in range(jugadorHumanoLen)]
    jugadorMaquinaLen = validar(input("Ingrese numero de jugadores maquina [1-4]: "))
    #jugadorMaquinaLen = 4 if jugadorMaquinaLen not in [1,2,3,4] else jugadorMaquinaLen
    jugadorMaquina = ["jugador"+str(i) for i in range(jugadorMaquinaLen)]
    carrera = CarreraCarros(jugadorHumano+jugadorMaquina)
    pistas = carrera.getPistas()
    carrera.setPista(int(input(f"\nSeleccione pista:\n\n(1) {pistas[0]}\n(2) {pistas[1]}\n(3) {pistas[2]}\n")))
    carrera.jugar()
    carrera.ganadores()
  if menu == 2:
    Guardar.consultar()