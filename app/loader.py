import json

from graph import Nodo, Collegamento


def carica_grafo(path):
    with open(path, "r") as f:
        data = json.load(f)

    nodi = {}

    # crea nodi
    for n in data["nodi"]:
        nodo = Nodo(
            nome=n["nome"],
            probabilita=n.get("probabilita", {})
        )

        nodi[n["nome"]] = nodo

    # crea collegamenti
    for c in data["collegamenti"]:
        partenza = nodi[c["from"]]
        arrivo = nodi[c["to"]]

        collegamento = Collegamento(
            partenza=partenza,
            arrivo=arrivo,
            tempo=c["tempo"]
        )

        partenza.uscenti.append(collegamento)
        arrivo.entranti.append(collegamento)

    return nodi