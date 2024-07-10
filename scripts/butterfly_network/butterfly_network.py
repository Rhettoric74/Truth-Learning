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
                if i != 0:
                    # flip the i-th most significant bit of j to obtain m.
                    bitmask = 1 << (k - i)
                    m = (j ^ bitmask) % (2 ** k)
                    new_node = ButterflyNode(below_neighbors=[self.nodes_grid[i - 1][j], self.nodes_grid[i - 1][m]], q=q)
                    row.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][j].above_neighbors:
                        self.nodes_grid[i - 1][j].above_neighbors.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][m].above_neighbors:
                        self.nodes_grid[i - 1][m].above_neighbors.append(new_node)
                        
                else:
                    row.append(ButterflyNode(q=q))
            self.nodes_grid.append(row)
            self.flattened_nodes_list += row
        adversarial_sample = random.sample(self.flattened_nodes_list, num_adversaries)
        for node in adversarial_sample:
            node.is_adversary = True
    def __repr__(self):
        string_representation = ""
        for i in range(len(self.nodes_grid) - 1, -1,-1):
            for j in range(len(self.nodes_grid[0])):
                string_representation += "{:.3f}".format(self.nodes_grid[i][j].compute_probability()) + "  "
            string_representation += "\n"
        return string_representation
    def compute_learning_rate(self):
        print(len(self.flattened_nodes_list))
        learning_rates = [node.compute_probability() for node in self.flattened_nodes_list]
        return np.mean(learning_rates)
    def traverse_tree(self, node):
        print(node.compute_probability())
        for n in node.above_neighbors:
            self.traverse_tree(n)
    def percentage_adversaries(self):
        return np.mean([1 if node.is_adversary else 0 for node in self.flattened_nodes_list])
    def print_adversaries(self):
        string_representation = ""
        for i in range(len(self.nodes_grid) - 1, -1,-1):
            for j in range(len(self.nodes_grid[0])):
                if self.nodes_grid[i][j].is_adversary:
                    string_representation +=  "A  "
                else:
                    string_representation += "H  "
            string_representation += "\n"
        return string_representation
    def find_row_with_no_learning(self):
        for i in range(len(self.nodes_grid)):
            all_wrong = True
            for j in range(len(self.nodes_grid[0])):
                if self.nodes_grid[i] != 0:
                    all_wrong = False
                    break
            if all_wrong:
                return i
        return -1


if __name__ == "__main__":
    k = 15
    q = 0.6
    m = 2
    # randomly distribute 1/m*2^-m adversaries
    #network = BinaryButterflyGraph(k, q, int((((k + 1)) / m) * (2 **(k - m))))
    #start with no adversaries
    network = BinaryButterflyGraph(k, q)
    # make every 2^m node on the the bottom row an adversary
    for i in range(1):
        
        for j in range(2 ** (k - m)):
            network.nodes_grid[i][2**(m) * j].is_adversary = True
    # make all of the first 2^m nodes in the first row adversaries
    """ for i in range(1):
        
        for j in range(2 ** (k - m)):
            network.nodes_grid[i][j].is_adversary = True """
    # put adversaries alternating in columns in the bottom 2**m rows:
    """ for i in range(2**m):
        for j in range(2**(k - m)):
            network.nodes_grid[i][2**(m) * j + i].is_adversary = True """
    # put adversaries randomly in first 2 rows such that they cover both columns
    """ first_row =[]
    for i in range(2):
        for j in range(2**(k)):
            if i == 0 and j < 2**(k - 1):
                first_row.append(j)
                network.nodes_grid[i][j].is_adversary = True
            elif i == 1 and j not in first_row:
                network.nodes_grid[i][j].is_adversary = True
 """
    # put adversaries on the first third of the first row
    """ for j in range((2**k) - 16):
        network.nodes_grid[0][j].is_adversary = True """
    # make two adversaries on the bottom row that immediately intersect
    """ network.nodes_grid[0][0].is_adversary = True
    network.nodes_grid[0][2**(k-1)].is_adversary = True """





    # randomly make half 2^{-m} of the columns 2^{-m}-full of adversaries
    """ rows = random.sample([i for i in range(k + 1)], (k + 1) // (2**m))
    for row in rows:
        columns = random.sample([i for i in range(2**k)], 2**(k - 2))
        for col in columns:
            network.nodes_grid[row][col].is_adversary = True """
    #network.traverse_tree(network.nodes_grid[0][1])
    #print(network)
    #print(network.print_adversaries())
    #print(network.percentage_adversaries())
    print(network.compute_learning_rate())
    print(network.nodes_grid[-1][-1].compute_probability())


                
        