from typing import Any, Dict, List, NoReturn, Optional

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pylab import rcParams


class CognitiveModel:
    def __init__(self, adjacency_matrix: np.ndarray, nodes_names: Optional[Dict[int, str]] = None):
        self.graph = nx.DiGraph(data=adjacency_matrix)
        self.nodes_names = nodes_names
        if nodes_names:
            nx.set_node_attributes(self.graph, "name", nodes_names)

    @property
    def adjacency_matrix(self) -> np.ndarray:
        return nx.adjacency_matrix(self.graph).todense()

    @property
    def graph_weights(self) -> Dict[Any, Any]:
        return nx.get_edge_attributes(self.graph, "weight")

    @staticmethod
    def get_spectral_radius(matrix: np.ndarray) -> float:
        return np.max(np.absolute(np.linalg.eigvals(matrix)))

    def check_perturbation_stability(self) -> bool:
        if self.get_spectral_radius(self.adjacency_matrix) <= 1:
            return True
        else:
            return False

    def check_numerical_stability(self) -> bool:
        if self.get_spectral_radius(self.adjacency_matrix) < 1:
            return True
        else:
            return False

    def is_even(self, cycle: List[int]) -> bool:
        negative_count = np.count_nonzero(
            np.less([self.graph_weights[edge] for edge in nx.find_cycle(self.graph, cycle)], 0)
        )
        return not negative_count & 0x1

    def check_structural_stability(self) -> List[List[int]]:
        return [cycle for cycle in nx.simple_cycles(self.graph) if self.is_even(cycle)]

    def calculate_eigenvalues(self) -> np.ndarray:
        return np.linalg.eigvals(self.adjacency_matrix)

    def draw_graph(self) -> NoReturn:
        rcParams["figure.figsize"] = 10, 8
        colors = ["g" if self.graph_weights[edge] > 0 else "r" for edge in self.graph.edges_iter()]
        nx.draw_networkx(
            self.graph,
            pos=nx.circular_layout(self.graph),
            arrows=True,
            with_labels=True,
            edge_color=colors,
            font_size=10,
            font_color="#ffffff",
            node_color="k",
            labels=self.nodes_names,
            node_size=2400,
        )
        plt.title("Когнітивна карта")
        plt.show()


# if __name__ == "__main__":
#     # A  B  C  D  E  F  G  H
#     matrix = np.array(
#         [
#             [0, -1, 1, 0, 0, 1, 0, 0],  # A
#             [0, 0, 0, 0, 1, 0, 0, 0],  # B
#             [0, 0, 0, 1, 0, 0, 0, 0],  # C
#             [1, 0, 0, 0, 0, 0, 0, 1],  # D
#             [0, 0, 0, 0, 0, 1, 1, 1],  # E
#             [0, 1, 0, 0, 0, 0, 1, 0],  # F
#             [0, 0, 0, 0, 0, 0, 0, 0],  # G
#             [0, 0, 0, 0, 0, 0, -1, 0],
#         ]  # H
#     )

#     nodes_names = {0: "Фактор 1", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}

#     model = CognitiveModel(matrix, nodes_names=nodes_names)
#     print(model.check_structural_stability())
#     model.draw_graph()
