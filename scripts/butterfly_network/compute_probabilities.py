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
def unknowing_adversarial_probability(q, i):
    """Purpose: compute the probability of an agent on level i in a butterfly network guessing
    correctly, when each agent recieves a private signal with probability q of being correct,
    assuming that there is an adversary on the bottom of the network connected to the agent
    in its upward branching binary tree. This case assumes that the original adversary doesn't know the ground truth,
    but rather chooses the action with the smaller probability of being correct."""
    q_i_stars_list = [(1 - q), (q ** 2 * (1 - q)) + (q * (1 - q) ** 2) + q * (1 - q)]
    q_is_list = [q, q * (1 + (2 * q - 1) * (1 - q))]
    while i > len(q_i_stars_list):
        cur_index = len(q_i_stars_list) - 1
        next_q_i_star = q_i_stars_list[cur_index] * (q_is_list[cur_index] - 2 * (q_is_list[cur_index] * q) + q) + q * q_is_list[cur_index]
        q_i_stars_list.append(next_q_i_star)
        q_is_list.append(q_is_list[cur_index] * (1 + (2 * q - 1) * (1 - q_is_list[cur_index])))
    return q_i_stars_list[i - 1]


if __name__ == "__main__":
    q = 0.51
    probabilities_list = [nonadversarial_probability(q, i) for i in range(1, 200)]
    adversarial_probs_list = [adversarial_probability(q, i) for i in range(1, 200)]
    unknowing_adv_probs_list = [unknowing_adversarial_probability(q, i) for i in range(1, 200)]
    print(probabilities_list[:20])
    print(adversarial_probs_list[:20])
    for i in range(1, 100):
        if adversarial_probs_list[i] > q:
            print("greater than q at index", i)
        if probabilities_list[i] - adversarial_probs_list[i] < 0.0001:
            print("Adversarial and non-adversarial sequences become close at index", i)
            break