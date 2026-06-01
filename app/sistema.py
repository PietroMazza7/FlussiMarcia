class Sistema:
    def __init__(self, nodi: dict):
        self.nodi = nodi
        self.totale_partiti = 0
        self.totale_arrivati = 0

    @property
    def sul_percorso(self) -> int:
        return self.totale_partiti - self.totale_arrivati
    
    def salva(self, path, grafo):
        import json

        dati = {
            "sistema": {
                "totale_partiti": self.totale_partiti,
                "totale_arrivati": self.totale_arrivati
            },
            "collegamenti": []
        }

        for nodo in grafo.values():
            for c in nodo.uscenti:
                dati["collegamenti"].append({
                    "from": c.partenza.nome,
                    "to": c.arrivo.nome,
                    "ingressi": [x.isoformat() for x in c.ingressi]
                })

        with open(path, "w") as f:
            json.dump(dati, f)