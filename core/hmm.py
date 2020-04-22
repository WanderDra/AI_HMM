from utils.file_manager import FileManager

class Customer:
    def __init__(self):
        self.stage = ''

class Hmm:
    def __init__(self):
        self.stage_table = {}
        self.emission_table = {}
        self.emission_keys = []
        self.emission_probabilities = []
        self.states = []
        self.state_keys = []
        self.emissions = {}
        self.emissions_list = []

        pass

    class State:
        def __init__(self, state):
            self.state = state
            self.next_state = []
            self.probabilities = []

        def add_next_state(self, next_state, probability):
            self.next_state.append(next_state)
            self.probabilities.append(probability)

        def get_probability(self, next_state):
            return self.probabilities[self.next_state.index(next_state)]

    def append_stage_table(self, init_state, new_state, probability):
        flag = False
        for s in self.states:
            if s.state == init_state:
                state = s
                flag = True

        if flag is False:
            state = self.State(init_state)
            self.states.append(state)
            self.state_keys.append(init_state)
        state.add_next_state(new_state, probability)

    def get_stage_table(self):
        self.stage_table = self.stage_table.fromkeys(self.state_keys)
        i = 0
        for stage in self.stage_table:
            self.stage_table[self.state_keys[i]] = self.states[i]
            i += 1
        return self.stage_table

    def append_emission_table(self, stage, probabilities):
        self.emission_keys.append(stage)
        self.emission_probabilities.append(probabilities)

    def get_emission_table(self):
        self.emission_table = self.emission_table.fromkeys(self.emission_keys)
        i = 0
        for probability in self.emission_probabilities:
            self.emission_table[self.emission_keys[i]] = probability
            i += 1
        return self.emission_table

    def init_emissions(self, emission_list):
        self.emissions.fromkeys(emission_list)
        i = 0
        for emission in emission_list:
            self.emissions[emission] = i
            i += 1
        self.emissions_list = emission_list

    def assume(self, init_stage, emission_list):
        current_prob = 1.0
        possible_list = []
        current_stage = self.stage_table[init_stage]
        possible_list.append(init_stage)
        for emissions in emission_list:
            s_i = 0
            prob_list = []
            for possible_state in current_stage.next_state:
                possible_prob = current_prob
                i = 0
                for e in self.emission_table[possible_state]:
                    if self.emissions_list[i] in emissions:
                        possible_prob *= e
                        # print(e)
                    else:
                        possible_prob *= 1 - e
                        # print(1 - e)
                    i += 1
                possible_prob *= current_stage.probabilities[s_i]
                # print(current_stage.probabilities[s_i])
                prob_list.append(possible_prob)
                s_i += 1
            if max(prob_list) != 0.0:
                max_pos_stage = current_stage.next_state[prob_list.index(max(prob_list))]
                possible_list.append(max_pos_stage)
                current_stage = self.stage_table[max_pos_stage]
                current_prob = max(prob_list)
                print(prob_list)
            else:
                possible_list.append(current_stage.state)
        return possible_list


def import_table():
    hmm = Hmm()
    hmm.append_stage_table('ZERO', 'AWARE', 0.4)
    hmm.append_stage_table('ZERO', 'ZERO', 0.6)
    hmm.append_stage_table('AWARE', 'CONSIDERING', 0.3)
    hmm.append_stage_table('AWARE', 'READY', 0.01)
    hmm.append_stage_table('AWARE', 'LOST', 0.2)
    hmm.append_stage_table('AWARE', 'AWARE', 0.49)
    hmm.append_stage_table('CONSIDERING', 'EXPERIENCING', 0.2)
    hmm.append_stage_table('CONSIDERING', 'READY', 0.02)
    hmm.append_stage_table('CONSIDERING', 'LOST', 0.3)
    hmm.append_stage_table('CONSIDERING', 'CONSIDERING', 0.48)
    hmm.append_stage_table('EXPERIENCING', 'READY', 0.3)
    hmm.append_stage_table('EXPERIENCING', 'LOST', 0.3)
    hmm.append_stage_table('EXPERIENCING', 'EXPERIENCING', 0.4)
    hmm.append_stage_table('READY', 'LOST', 0.2)
    hmm.append_stage_table('READY', 'SATISFIED', 0.8)
    hmm.append_stage_table('LOST', 'SATISFIED', 0.0)
    hmm.append_stage_table('SATISFIED', 'LOST', 0.0)
    hmm.get_stage_table()

    hmm.init_emissions(['DEMO', 'VIDEO', 'TESTIMONIAL', 'PRICING', 'BLOG', 'PAYMENT'])
    hmm.append_emission_table('ZERO', [0.1, 0.01, 0.05, 0.3, 0.5, 0.0])
    hmm.append_emission_table('AWARE', [0.1, 0.01, 0.15, 0.3, 0.4, 0.0])
    hmm.append_emission_table('CONSIDERING', [0.2, 0.3, 0.05, 0.4, 0.4, 0.0])
    hmm.append_emission_table('EXPERIENCING', [0.4, 0.6, 0.05, 0.3, 0.4, 0.0])
    hmm.append_emission_table('READY', [0.05, 0.75, 0.35, 0.2, 0.4, 0.0])
    hmm.append_emission_table('LOST', [0.01, 0.01, 0.03, 0.05, 0.2, 0.0])
    hmm.append_emission_table('SATISFIED', [0.4, 0.4, 0.01, 0.05, 0.5, 1.0])
    hmm.get_emission_table()

    return hmm


def test():
    hmm = import_table()
    print(hmm.stage_table['AWARE'].next_state)
    print(hmm.emission_table)

    fm = FileManager("D:\\PyProject\\AI_HMM\\AI_HMM\\examples\\hmm_customer_1586733277027.txt")
    print(fm.read_emissions())
    emission_list = fm.read_emissions()
    print(hmm.assume('ZERO', emission_list))


test()