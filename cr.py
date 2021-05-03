from random import randint
class JuegoCarreras:
  __id=0
  def iniciarJuego():
    pass
    
class Vehiculo:
  __distancia = 0
  __carril = 0
  __numero = []

  def __init__(self, num, car):
    self.__carril = car
    self.__numero = num

  def getNumero(self):
    return self.__numero

  def setgetDistancia(self, dis):
    self.__distancia += dis
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
    print(f"nombre  {self.__nombre} carro  {self.__vehiculo}")

  def getNombre(self):
    return self.__nombre

class CarreraCarros:
  __id = 0
  __pistas = Pista(["Arena","Asfalto", "Nieve"], 1500)
  __jugadores = []
  __carros = []
  __podio = []
  def __init__(self, jug):
    jugadoresLen = len(jug)
    self.__carros = [Vehiculo(randint(0,99), i) for i in range(jugadoresLen)]
    self.__jugadores = [Jugador(0, "") for i in range(jugadoresLen)]
    for i in range(jugadoresLen):
      self.__jugadores[i].setNombre(jug[i])
      self.__jugadores[i].setVehiculo(self.__carros[i].getNumero())
    

  def jugar(self):
    longitudPista = self.__pistas.getLongitud()
    while len(self.__podio) < 3:
      for i in range(len(self.__jugadores)):
        if self.__carros[i].setgetDistancia(100*randint(1,6)) >= longitudPista:
          
    print(self.__podio)



if __name__ == '__main__':
  '''jugadorHumanoLen = int(input("Ingrese numero de jugadores humanos [1-4]: ")) 
  jugadorHumanoLen = 1 if jugadorHumanoLen not in [1,2,3,4] else jugadorHumanoLen
  #print(jugadorHumanoLen)
  jugadorHumano = [input(f"Jugador humano {i}: ") for i in range(jugadorHumanoLen)]
  #print(jugadorHumano[0])
  jugadorMaquinaLen = input("Ingrese numero de jugadores maquina [1-4]: ")
  jugadorMaquinaLen = 4 if jugadorMaquinaLen not in [1,2,3,4] else jugadorMaquinaLen
  carreralocal = [CarreraCarros() for i in range(3)]
  pistas = carreralocal[0].getPistas()
  pista = input(f"Seleccione la pista donde quiere jugar\n(1) {pistas[0][0]} \t{pistas[0][1]}Km \n(2) {pistas[1][0]} \t{pistas[1][1]}Km \n(3) {pistas[2][0]} \t{pistas[2][1]}Km \n")
  carreralocal[0].Iniciarjuego(["h1","h2"],3, pista)
'''
carreraLocal = CarreraCarros(["h1","h2","m1", "m2"])
carreraLocal.jugar()

  