from app.database import (
    get_totale_partiti,
    get_totale_arrivati
)


class Sistema:
    def __init__(self, nodi: dict):
        self.nodi = nodi

    @property
    def totale_partiti(self) -> int:
        return get_totale_partiti()

    @property
    def totale_arrivati(self) -> int:
        return get_totale_arrivati()

    @property
    def sul_percorso(self) -> int:
        return self.totale_partiti - self.totale_arrivati