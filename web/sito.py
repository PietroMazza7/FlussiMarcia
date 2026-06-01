from flask import Flask, render_template, redirect, url_for

from datetime import datetime

from app.loader import carica_grafo
from app.sistema import Sistema

sito = Flask(__name__)

nodi = carica_grafo("data/grafo.json")
sistema = Sistema(nodi)


@sito.get("/")
def index():
    return render_template(
        "index.html",
        nodi=nodi.keys(),
        sistema=sistema
    )


@sito.get("/nodo/<nome>")
def pagina_nodo(nome):
    nodo = nodi[nome]

    return render_template(
        "nodo.html",
        nodo=nodo,
        arrivi=nodo.in_arrivo(datetime.now(), 10),
        sistema=sistema
    )


@sito.post("/nodo/<nome>/conta")
def conta(nome):
    nodi[nome].conta(datetime.now())

    if nome == "S":
        sistema.totale_arrivati += 1

    return redirect(
        url_for("pagina_nodo", nome=nome)
    )


@sito.post("/nodo/S/genera")
def genera():
    nodi["S"].genera(datetime.now())
    sistema.totale_partiti += 1

    return redirect(
        url_for("pagina_nodo", nome="S")
    )


if __name__ == "__main__":
    sito.run(debug=True)