from compute_probabilities import *
import random
import numpy as np
import copy
class ButterflyNode:
    def __init__(self, above_neigbors = [], below_neighbors = [], is_adversary = False, q = 2 / 3):
        self.above_neighbors = copy.copy(above_neigbors)
        self.below_neighbors = copy.copy(below_neighbors)
        self.is_adversary = is_adversary
        self.probability = None
        self.q = q
    def compute_probability(self):
        if self.probability != None:
            return self.probability
        elif self.is_adversary:
            self.probability = 0
            return 0
        elif self.below_neighbors == []:
            self.probability = self.q
            return self.q
        else:
            # compute the probability of guessing correctly
            # from your below neighbors
            # probability that both below neighbors are correct
            left_prob = self.below_neighbors[0].compute_probability()
            right_prob = self.below_neighbors[1].compute_probability()
            prob = left_prob * right_prob
            prob += self.q * (left_prob * (1 - right_prob) + right_prob * (1 - left_prob))
            self.probability = prob
            return prob
class BinaryButterflyGraph:
    def __init__(self, k, q, num_adversaries = 0):
        self.flattened_nodes_list = []
        self.nodes_grid = []
        for i in range(k + 1):
            row = []
            for j in range(2 ** k):
                # flip the i-th most significant bit of j to obtain m.
                bitmask = 1 << (i)
                m = (j ^ bitmask) % (2 ** k)
                if i != 0:
                    new_node = ButterflyNode(below_neighbors=[self.nodes_grid[i - 1][j], self.nodes_grid[i - 1][m]], q=q)
                    row.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][j].above_neighbors:
                        self.nodes_grid[i - 1][j].above_neighbors.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][m].above_neighbors:
                        self.nodes_grid[i - 1][m].above_neighbors.append(new_node)
                        
                else:
                    row.append(ButterflyNode())
            self.nodes_grid.append(row)
            self.flattened_nodes_list += row
        adversarial_sample = random.sample(self.flattened_nodes_list, num_adversaries)
        for node in adversarial_sample:
            node.is_adversary = True
    def compute_learning_rate(self):
        print(len(self.flattened_nodes_list))
        learning_rates = [node.compute_probability() for node in self.flattened_nodes_list]
        return np.mean(learning_rates)
    def traverse_tree(self, node):
        print(node.compute_probability())
        for n in node.above_neighbors:
            self.traverse_tree(n)

if __name__ == "__main__":
    k = 15
    q = 2 / 3
    network = BinaryButterflyGraph(k, q, 2 ** (k - 1))
    # make every other node on the bottom row an adversary
    """ for j in range(2 ** (k - 2)):
        network.nodes_grid[0][4 * j].is_adversary = True """
    #network.traverse_tree(network.nodes_grid[0][0])
    print(network.compute_learning_rate())


                
        