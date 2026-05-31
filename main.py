from app.loader import carica_grafo, carica_eventi
from app.simulation import Simulazione

def main():
    nodi = carica_grafo("data/grafo.json")
    eventi = carica_eventi("data/eventi.json")

    sim = Simulazione(nodi)
    sim.run(20, eventi)

if __name__ == "__main__":
    main()