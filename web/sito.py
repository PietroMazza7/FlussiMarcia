from flask import Flask, jsonify
from datetime import datetime

from app.loader import carica_grafo
from app.graph import Nodo
from app.simulation import Simulazione

sito = Flask(__name__)

nodi = carica_grafo("data/grafo.json")
sim = Simulazione(nodi)

@sito.get("/stato")
def stato():
    output = {}

    for nome, nodo in nodi.items():
        output[nome] = nodo.in_arrivo(sim.ora, 10)

    return jsonify(output)

@sito.post("/conta/<nome>")
def conta(nome):
    nodo = nodi[nome]
    nodo.conta(sim.ora)

    return {"ok": True}

@sito.post("/step")
def step():
    sim.step()
    return {"ora": str(sim.ora)}

if __name__ == "__main__":
    sito.run(debug=True)