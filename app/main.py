from loader import carica_grafo


def main():
    nodi = carica_grafo("grafo.json")

    Start = nodi["S"]

    for _ in range(100):
        Start.genera()

    for c in Start.uscenti:
        print(
            f"{c.partenza.nome} -> {c.arrivo.nome}: "
            f"{len(c.ingressi)} persone"
        )


if __name__ == "__main__":
    main()