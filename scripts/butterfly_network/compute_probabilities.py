def nonadversarial_probability(q, i):
    """Purpose: compute the probability of an agent on level i in a butterfly network guessing
    correctly, when each agent recieves a private signal with probability q of being correct"""
    q_i = q
    for i in range(1, i):
        q_i = q_i * (1 + (2 * q - 1) * (1 - q_i))
    return q_i
def adversarial_probability(q, i):
    """Purpose: compute the probability of an agent on level i in a butterfly network guessing
    correctly, when each agent recieves a private signal with probability q of being correct,
    assuming that there is an adversary on the bottom of the network connected to the agent
    in its upward branching binary tree."""
    q_i_stars_list = [0, q ** 2]
    q_is_list = [q, q * (1 + (2 * q - 1) * (1 - q))]
    while i > len(q_i_stars_list):
        cur_index = len(q_i_stars_list) - 1
        next_q_i_star = q_i_stars_list[cur_index] * (q_is_list[cur_index] - 2 * (q_is_list[cur_index] * q) + q) + q * q_is_list[cur_index]
        q_i_stars_list.append(next_q_i_star)
        q_is_list.append(q_is_list[cur_index] * (1 + (2 * q - 1) * (1 - q_is_list[cur_index])))
    return q_i_stars_list[i - 1]


if __name__ == "__main__":
    q = 2/3
    probabilities_list = [nonadversarial_probability(q, i) for i in range(1, 20)]
    adversarial_probs_list = [adversarial_probability(q, i) for i in range(1, 20)]
    print(probabilities_list)
    print(adversarial_probs_list)
    for i in range(1, 100):
        if probabilities_list[i] - adversarial_probs_list[i] < 0.0001:
            print("Sequences become close at index", i)
            break
