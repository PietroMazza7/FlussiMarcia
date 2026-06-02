from dataclasses import dataclass, field
from datetime import datetime, timedelta
import random

from app.database import (
    aggiungi_persona,
    conta_collegamento,
    rimuovi_piu_vecchio,
    arrivi_entro_collegamento
)

@dataclass
class Collegamento:
    partenza: "Nodo"
    arrivo: "Nodo"
    tempo: int  # minuti medi

    def aggiungi(self, ora: datetime):
        aggiungi_persona(self, ora)

    def arrivi_entro(self, ora: datetime, minuti: int) -> int:
        return arrivi_entro_collegamento(
            self,
            ora,
            minuti
        )

    def rimuovi_piu_vicino_arrivo(self):
        rimuovi_piu_vecchio(
            self
        )

@dataclass
class Nodo:
    nome: str
    probabilita: dict[str, float] = field(default_factory=dict)

    uscenti: list["Collegamento"] = field(default_factory=list)
    entranti: list["Collegamento"] = field(default_factory=list)

    def genera(self, ora: datetime):
        if not self.uscenti:
            return

        pesi = [self.probabilita[c.arrivo.nome] for c in self.uscenti]
        arco = random.choices(self.uscenti, weights=pesi)[0]

        arco.aggiungi(ora)

    def scegli_da_rimuovere(self):
        candidato = None
        miglior_arrivo = None

        for c in self.entranti:
            count = conta_collegamento(c)
            if count == 0:
                continue

            # scegliamo quello con ingresso più “vecchio”
            ingresso = rimuovi_piu_vecchio(c, peek=True)

            if ingresso is None:
                continue

            arrivo = ingresso + timedelta(minutes=c.tempo)

            if miglior_arrivo is None or arrivo < miglior_arrivo:
                miglior_arrivo = arrivo
                candidato = c

        return candidato

    def conta(self, ora: datetime):
        c = self.scegli_da_rimuovere()

        if c:
            c.rimuovi_piu_vicino_arrivo()

        if self.nome != 'S':
            self.genera(ora)

    def in_arrivo(self, ora: datetime, minuti: int) -> int:
        return sum(
            coll.arrivi_entro(ora, minuti)
            for coll in self.entranti
        )