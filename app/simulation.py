from datetime import datetime, timedelta
from app.graph import Nodo


class Simulazione:
    def __init__(self, nodi: dict[str, Nodo], start_time: datetime | None = None):
        self.nodi = nodi
        self.ora = start_time or datetime.now()

    def step(self):
        self.ora += timedelta(minutes=1)

    def esegui_evento(self, evento: dict):
        tipo = evento["tipo"]
        nodo = self.nodi[evento["nodo"]]

        if tipo == "genera":
            nodo.genera(self.ora)

        elif tipo == "conta":
            nodo.conta(self.ora)

        elif tipo == "in_arrivo":
            minuti = evento["tempo"]
            print(nodo.nome, nodo.in_arrivo(self.ora, minuti))

    def run(self, minuti: int, eventi: list[dict]):
        for i in range(minuti):
            if i < len(eventi):
                self.esegui_evento(eventi[i])
            self.step()

    def visualizza(self):
        for nome, nodo in self.nodi.items():
            print(nome, nodo.in_arrivo(self.ora, 10))