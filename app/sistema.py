class Sistema:
    def __init__(self, nodi: dict):
        self.nodi = nodi
        self.totale_partiti = 0
        self.totale_arrivati = 0

    @property
    def sul_percorso(self) -> int:
        return self.totale_partiti - self.totale_arrivati