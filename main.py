import matplotlib.pyplot as plt
import random
from matplotlib.lines import Line2D


class Graf:
    graph: dict

    def __init__(self):
        self.graph = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, edge: str):
        source, target = edge.split("-")
        source = int(source)
        target = int(target)
        if source == target:
            raise ValueError("pętle są zabronione")
        if target not in self.graph[source]:
            self.graph[source].append(target)
        if source not in self.graph[target]:
            self.graph[target].append(source)

    def print_graph(self):
        L = []
        for source in self.graph:
            L.append("{} : ".format(source))
            for target in self.graph[source]:
                L.append("{} ".format(target))
            L.append("\n")
        print("".join(L))

    def dfs(self, start):
        visit = list()
        stack = [(start, None)]  # Dodawanie do stosu (wierzchołek, poprzednik)
        paths = []

        while stack:
            vertex, predecessor = stack.pop()

            if vertex not in visit:
                visit.append(vertex)
                neighbours = list(set(self.graph[vertex]) - set(visit))
                random.shuffle(neighbours)  # Mieszanie listy sąsiadów
                stack.extend([(neighbour, vertex) for neighbour in set(self.graph[vertex]) - set(visit)])
                paths.append((vertex, predecessor))

        return visit, paths


def one_side(square1, square2):
    x1, y1 = square1
    x2, y2 = square2
    return (x1 == x2 and abs(y1 - y2) == 1) or (y1 == y2 and abs(x1 - x2) == 1)


if __name__ == "__main__":
    x_input = input("Podaj długość labiryntu: ")
    y_input = input("Podaj szerokość labiryntu: ")
    rozmiar_x, rozmiar_y = int(x_input), int(y_input)
    graf = Graf()
    fig, ax = plt.subplots(figsize=(rozmiar_x, rozmiar_y))

    number = 1
    numbers = {}
    for x in range(rozmiar_x):
        for y in range(rozmiar_y):
            ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=None, edgecolor='black'))
            numbers[number] = (x + 0.5, y + 0.5)
            graf.add_node(number)
            number += 1

    ax.set_xlim([0, rozmiar_x])
    ax.set_ylim([0, rozmiar_y])
    ax.axis('off')

    for key, value in numbers.items():
        for key1, value1 in numbers.items():
            if value != value1 and one_side(value, value1):
                graf.add_edge(str(key) + "-" + str(key1))
    graf.print_graph()
    rand = random.Random()
    rndInt = rand.randint(1, len(graf.graph))
    print(rndInt)
    visited, path = graf.dfs(rndInt)
    print(path)

    for i in range(1, len(path)):
        start, pred = path[i]
        if pred is not None:  # Sprawdzenie, czy istnieje poprzednik
            start_pos = numbers[pred]
            end_pos = numbers[start]
            if one_side(start_pos, end_pos):  # Sprawdzenie, czy kwadraty sąsiadują ze sobą, by móć usunąć wspólną krawędź
                line = Line2D([start_pos[0], end_pos[0]], [start_pos[1], end_pos[1]], linewidth=52, color='white')
                ax.add_line(line)
                plt.savefig(f'path_{i}.png')
