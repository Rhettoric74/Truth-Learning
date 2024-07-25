from compute_probabilities import *
import random
import numpy as np
import copy
import json
class ButterflyNode:
    def __init__(self, above_neigbors = [], below_neighbors = [], is_adversary = False, q = 2 / 3, know_truth = False):
        self.above_neighbors = copy.copy(above_neigbors)
        self.below_neighbors = copy.copy(below_neighbors)
        self.is_adversary = is_adversary
        self.probability = None
        self.q = q
        self.adversaries_know_truth = know_truth
    def compute_probability(self):
        if self.probability != None:
            return self.probability
        elif self.below_neighbors == []:
            if self.is_adversary and not self.adversaries_know_truth:
                self.probability = 1 - self.q
                return 1 - self.q
            elif self.is_adversary:
                self.probability = 0
                return 0
            else:
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
            if self.is_adversary and not self.adversaries_know_truth:
                self.probability = 1 - prob
                return 1 - prob
            elif self.is_adversary:
                self.probability = 0
                return 0
            else:
                self.probability = prob
                return prob
class BinaryButterflyGraph:
    def __init__(self, k, q, num_adversaries = 0, adversaries_know_truth = False):
        self.flattened_nodes_list = []
        self.nodes_grid = []
        for i in range(k + 1):
            row = []
            for j in range(2 ** k):
                if i != 0:
                    # flip the i-th most significant bit of j to obtain m.
                    bitmask = 1 << (k - i)
                    m = (j ^ bitmask) % (2 ** k)
                    new_node = ButterflyNode(below_neighbors=[self.nodes_grid[i - 1][j], self.nodes_grid[i - 1][m]], q=q, know_truth=adversaries_know_truth)
                    row.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][j].above_neighbors:
                        self.nodes_grid[i - 1][j].above_neighbors.append(new_node)
                    if new_node not in self.nodes_grid[i - 1][m].above_neighbors:
                        self.nodes_grid[i - 1][m].above_neighbors.append(new_node)
                        
                else:
                    row.append(ButterflyNode(q=q, know_truth=adversaries_know_truth))
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
    def print_averages_per_row(self):
        averages_per_row = ""
        for i in range(len(self.nodes_grid)):
            row_average = np.mean([self.nodes_grid[i][j].compute_probability() for j in range(len(self.nodes_grid[i]))])
            averages_per_row += "{:.3f}".format(row_average) + "\n"
        print(averages_per_row)
    def compute_average_on_top_row(self):
        return np.mean([self.nodes_grid[-1][j].compute_probability() for j in range(len(self.nodes_grid[-1]))])
            
    
class RandomFourRegularGraph(BinaryButterflyGraph):
    def __init__(self, k, q, num_adversaries = 0, adversareis_know_truth=False):
        self.flattened_nodes_list = []
        self.nodes_grid = []
        for i in range(k + 1):
            row = [ButterflyNode(q=q, know_truth=adversareis_know_truth) for j in range(2**k)]
            vertex_match_counts = {row[j]:0 for j in range(2**k)}
            if i >= 1:
                for j in range(2**k):
                    cur_node = self.nodes_grid[i - 1][j]
                    child_nodes = None
                    if len(list(vertex_match_counts.keys())) < 4:
                        unmatched_node = None
                        for key in vertex_match_counts.keys():
                            if vertex_match_counts[key] == 0:
                                unmatched_node = key
                        if unmatched_node != None:
                            other_nodes = copy.copy(list(vertex_match_counts.keys()))
                            other_nodes.remove(unmatched_node)
                            child_nodes = [unmatched_node, random.choice(other_nodes)]
                    if child_nodes == None:
                        child_nodes = random.sample(list(vertex_match_counts.keys()), 2)
                    cur_node.above_neighbors = child_nodes
                    child_nodes[0].below_neighbors.append(cur_node)
                    child_nodes[1].below_neighbors.append(cur_node)
                    vertex_match_counts[child_nodes[0]] += 1
                    vertex_match_counts[child_nodes[1]] += 1
                    if vertex_match_counts[child_nodes[0]] > 1:
                        vertex_match_counts.pop(child_nodes[0])
                    if vertex_match_counts[child_nodes[1]] > 1:
                         vertex_match_counts.pop(child_nodes[1])
            self.nodes_grid.append(row)
            self.flattened_nodes_list += row


        adversarial_sample = random.sample(self.flattened_nodes_list, num_adversaries)
        for node in adversarial_sample:
            node.is_adversary = True


if __name__ == "__main__":
    q_values = [0.5 + 0.05 * i for i in range(1, 10)]
    beta_values = [0.05 * i for i in range(1, 10)]
    results = []
    for q in q_values:
        for beta in beta_values:
            adv_know_truth = True
            k = 15
            #q = 2 / 3
            m = 1
            predicted_last_row_learning_value = 1 - beta / ((1 - beta) * (2 * q - 1))
            # randomly distribute 1/m*2^-m adversaries
            #network = BinaryButterflyGraph(k, q, int((((k + 1)) / m) * (2 **(k - m))))
            #start with no adversaries
            number_adversaries= int((k + 1) * (2**k) * (beta))
            random_adversaries = 0
            network = BinaryButterflyGraph(k, q, num_adversaries=number_adversaries, adversaries_know_truth=adv_know_truth)
            # make every 2^m node on the the bottom row an adversary
            """ for i in range(1):
                
                for j in range(2 ** (k - m)):
                    network.nodes_grid[i][2**(m) * j].is_adversary = True """
            # make all of the first 2^(k - m) nodes in the first row adversaries
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
            print(network.percentage_adversaries())
            print(network.compute_learning_rate())
            network.print_averages_per_row()
            results_dict = {"k_value":k,
                            "q_value":q,
                            "beta_value":beta,
                            "predicted_last_row_learning_rate":predicted_last_row_learning_value,
                            "simulated_last_row_learning_rate":network.compute_average_on_top_row()
                            }
            results.append(results_dict)
            """ randomly_linked_network = RandomFourRegularGraph(k, q, random_adversaries, adversareis_know_truth=adv_know_truth)
            for i in range(1):
                for j in range(2 ** (k - m)):
                    randomly_linked_network.nodes_grid[i][2**(m) * j].is_adversary = True
            print(randomly_linked_network.compute_learning_rate())
            print(randomly_linked_network)
            print(randomly_linked_network.print_adversaries()) """
    print(results)
    with open("simulation_results.json", "w") as f:
        json.dump(results, f)


                        
                