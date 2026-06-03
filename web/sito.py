from flask import Flask, render_template, jsonify
from datetime import datetime

from app.loader import carica_grafo
from app.sistema import Sistema
from app.database import (
    init_db,
    init_sistema,
    incrementa_partiti,
    incrementa_arrivati
)

sito = Flask(__name__)

nodi = carica_grafo("data/grafo.json")
sistema = Sistema(nodi)

init_db()
init_sistema()


def stato_nodo(nome):
    """Stato attuale di un nodo come dict."""
    nodo = nodi[nome]
    return {
        "nome": nodo.nome,
        "arrivi_10": nodo.in_arrivo(datetime.now(), 10),
        "sul_percorso": sistema.sul_percorso,
        "totale_partiti": sistema.totale_partiti,
        "totale_arrivati": sistema.totale_arrivati,
    }


# ── Pagine ────────────────────────────────────────────────

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


# ── API ───────────────────────────────────────────────────

@sito.get("/api/nodo/<nome>")
def api_nodo(nome):
    return jsonify(stato_nodo(nome))


@sito.post("/api/nodo/<nome>/conta")
def api_conta(nome):
    nodo = nodi[nome]
    ok = nodo.conta(datetime.now())

    if not ok:
        return jsonify({
            "ok": False,
            "errore": "Nessuna persona in transito verso questo nodo"
        }), 400

    if nome == "S":
        incrementa_arrivati()

    return jsonify({"ok": True, **stato_nodo(nome)})


@sito.post("/api/nodo/S/genera")
def api_genera():
    nodi["S"].genera(datetime.now())
    incrementa_partiti()
    return jsonify({"ok": True, **stato_nodo("S")})
