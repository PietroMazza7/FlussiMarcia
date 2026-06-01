import json
from datetime import datetime
from collections import deque

from app.graph import Nodo, Collegamento


def carica_grafo(path: str) -> dict[str, Nodo]:
    with open(path, "r") as f:
        data = json.load(f)

    nodi: dict[str, Nodo] = {}

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


def carica_eventi(path: str) -> list[dict]:
    with open(path, "r") as f:
        eventi = json.load(f)

    for evento in eventi:
        evento["timestamp"] = datetime.fromisoformat(evento["timestamp"])

    return eventi

def carica_stato(path, nodi):
    import json

    with open(path, "r") as f:
        data = json.load(f)

    sistema_data = data["sistema"]

    collegamenti_map = {
        (c["from"], c["to"]): c["ingressi"]
        for c in data["collegamenti"]
    }

    for nodo in nodi.values():
        for c in nodo.uscenti:
            key = (c.partenza.nome, c.arrivo.nome)

            if key in collegamenti_map:
                c.ingressi = deque(
                    datetime.fromisoformat(x)
                    for x in collegamenti_map[key]
                )

    return sistema_data