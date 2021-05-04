from random import randint
import sqlite3
class JuegoCarreras:
  __id=0
  __vehiculos = []
  __jugadores = []
  __pistas = []
  __podio = []

  def iniciarJuego(self, str):
    print(str)
    
class Vehiculo:
  __distancia = 0
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

class Pista:
  __nombrePistas = ""
  __longitud = 0

  def __init__(self, nom, lon):
    self.__nombrePistas = nom
    self.__longitud = lon

  def getLongitud(self):
    return self.__longitud

class Jugador:
  __vehiculo = 0
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
  def iniciarDb():    #retorna conexion y cursor de la conexion a la db
    try:
      conect = sqlite3.connect('data.db')
      cursor = conect.cursor()
    except:
      print("Database Error")
    return cursor, conect 

  @staticmethod
  def guardar(cur, con, podio):
    cur.execute("CREATE TABLE IF NOT EXISTS partidas(id integer PRIMARY KEY, primero text, segundo text, tercero text)")
    cur.execute("INSERT INTO partidas(primero, segundo, tercero) VALUES(?, ?, ?)", (podio[0], podio[1], podio[2]))
    con.commit()

  @staticmethod
  def consultar(cur):
    cur.execute("SELECT * FROM partidas")
    print("Id\tprimero\t\tsegundo\t\ttercero\n\t")
    [print(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3]}") for row in cur.fetchall()]


class CarreraCarros(JuegoCarreras):
  __id = 0
  __pistas = Pista(["Arena","Asfalto", "Nieve"], 1500)
  __podio = []

  def __init__(self, jug):
    jugadoresLen = len(jug)
    self.__vehiculos = [Vehiculo(randint(0,99), i) for i in range(jugadoresLen)]
    self.__jugadores = [Jugador(0, "") for i in range(jugadoresLen)]
    for i in range(jugadoresLen):
      self.__jugadores[i].setNombre(jug[i])
      self.__jugadores[i].setVehiculo(self.__vehiculos[i].getNumero())

  def jugar(self):
    longitudPista = self.__pistas.getLongitud()
    podios = 3 if len(self.__jugadores) > 3 else len(self.__jugadores)-1
    while len(self.__podio) <= podios:
      for i in range(len(self.__jugadores)):
        if self.__vehiculos[i].getDistancia() >= longitudPista:
          if self.__jugadores[i].getNombre() not in self.__podio:
            self.__podio.append(self.__jugadores[i].getNombre())
        else:    
          self.__vehiculos[i].setDistancia(100*randint(1,6))
    if len(self.__podio) < 3:
      self.__podio.append("null")
    cur, con = Guardar.iniciarDb()
    Guardar.guardar(cur, con, self.__podio)
    Guardar.consultar(cur)



    


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
  jugadorHumanoLen = int(input("\nIngrese numero de jugadores humanos [1-4]: ")) 

  jugadorHumanoLen = 1 if jugadorHumanoLen not in [1,2,3,4] else jugadorHumanoLen
  jugadorHumano = [input(f"Jugador humano {i}: ") for i in range(jugadorHumanoLen)]
  jugadorMaquinaLen = int(input("Ingrese numero de jugadores maquina [1-4]: "))
  jugadorMaquinaLen = 4 if jugadorMaquinaLen not in [1,2,3,4] else jugadorMaquinaLen
  jugadorMaquina = ["jugador"+str(i) for i in range(jugadorMaquinaLen)]
  carreraLocal = CarreraCarros(jugadorHumano+jugadorMaquina)
  carreraLocal.jugar()


  