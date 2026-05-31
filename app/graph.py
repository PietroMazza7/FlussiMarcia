from dataclasses import dataclass, field
from collections import deque
from datetime import datetime, timedelta
import random

@dataclass
class Collegamento:
    partenza: "Nodo"
    arrivo: "Nodo"
    tempo: int
    ingressi: deque[datetime] = field(default_factory=deque)

    def aggiungi(self, ora):
        self.ingressi.append(ora)

    def arrivi_entro(self, ora, minuti: int) -> int:
        soglia = ora + timedelta(minutes=minuti)

        return sum(ingresso + timedelta(minutes=self.tempo) <= soglia for ingresso in self.ingressi)

    def rimuovi_piu_vicino_arrivo(self):
        if self.ingressi:
            self.ingressi.popleft()

@dataclass
class Nodo:
    nome: str
    probabilita: dict[str, float] = field(default_factory=dict)

    uscenti: list["Collegamento"] = field(default_factory=list)
    entranti: list["Collegamento"] = field(default_factory=list)

    def genera(self, ora):
        if not self.uscenti:
            return

        pesi = [self.probabilita[c.arrivo.nome] for c in self.uscenti]
        arco = random.choices(self.uscenti, weights=pesi)[0]

        arco.aggiungi(ora)

    def scegli_da_rimuovere(self):
        candidato = None
        miglior_arrivo = None

        for c in self.entranti:
            if not c.ingressi:
                continue

            ingresso = c.ingressi[0]
            arrivo = ingresso + timedelta(minutes=c.tempo)

            if miglior_arrivo is None or arrivo < miglior_arrivo:
                miglior_arrivo = arrivo
                candidato = c

        return candidato

    def conta(self, ora):
        c = self.scegli_da_rimuovere()

        if c:
            c.rimuovi_piu_vicino_arrivo()
            self.genera(ora)

    def in_arrivo(self, ora, minuti):
        return sum(coll.arrivi_entro(ora, minuti) for coll in self.entranti)