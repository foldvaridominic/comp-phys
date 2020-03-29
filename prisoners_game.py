# Valamiert nalam a dobogo az ALLD, GRIM, TFT sorrend mindig.
# Nem tudom esetleg van-e valami hiba, amiert nem a TFT nyer.

import numpy as np
import itertools
import operator

class Strategy:
    def __init__(self, initial, depend, random, stubborn):
        self.initial = initial
        self.depend  = depend
        self.random = random
        self.stubborn = stubborn
        self.round = 0
        self.score = 0
        self.last_choice = None
        self.last_opp_choice = None
        if depend:
            self.initial = "C"
        if self.stubborn:
            self.initial = "C"
        if random:
            if np.random.random() < random:
                self.initial =  "C"
            else:
                self.initial = "D"

    @property
    def strategy_type(self):
        if self.random:
            name = "RANDOM"
        elif self.depend == "maybe":
            name = "GTFT"
        elif self.depend == "yes":
            name = "TFT"
        elif self.stubborn:
            name = "GRIM"
        elif self.initial == "C":
            name = "ALLC"
        elif self.initial == "D":
            name = "ALLD"
        return name

    @property
    def choice(self):
        if self.round > 1:
            if self.random:
                if np.random.random() < self.random:
                    choice = "C"
                else:
                    choice = "D"
            elif self.depend == "yes":
                choice = self.last_opp_choice
            elif self.depend == "maybe":
                choice = self.last_opp_choice
                if np.random.random() < 0.2: # GTFT, probability is 0.2 for generousness
                    choice = "C"
            elif self.stubborn:
                if self.last_choice == "D":
                    choice = "D"
                elif self.last_opp_choice == "D":
                    choice = "D"
                else:
                    choice = self.last_choice
            else:
                choice = self.initial
        else:
            choice = self.initial
        return choice

    def play(self, opponent):
        if self.choice == "C":
            if opponent.choice == "C":
                self.score += 4
                opponent.score += 4
            elif opponent.choice == "D":
                self.score += 1
                opponent.score += 5
        elif self.choice == "D":
            if opponent.choice == "D":
                self.score += 2
                opponent.score += 2
            elif opponent.choice == "C":
                self.score += 5
                opponent.score += 1

        self.last_choice = self.choice
        self.last_opp_choice = opponent.choice
        opponent.last_choice = opponent.choice
        opponent.last_opp_choice = self.choice
        self.round += 1
        opponent.round += 1

INITIALS = ("C", "D")
INITIALS_PROB = (0.5, 0.5)
DEPENDS = (None, "yes", "maybe")
DEPENDS_PROB = (0.6, 0.2, 0.2)
STUBBORNS = (False, True)
STUBBORNS_PROB = (0.67, 0.33)
PLAYER_TYPES = ('RANDOM', 'TFT', 'GTFT', 'GRIM', 'ALLC', 'ALLD')

players = {}
player_type_count = dict.fromkeys(PLAYER_TYPES, 0)
for i in range(50):
    initial = np.random.choice(INITIALS, p=INITIALS_PROB)
    depend = np.random.choice(DEPENDS, p=DEPENDS_PROB)
    random = np.random.choice((None, np.random.random()), p=(0.83, 0.17))
    stubborn = np.random.choice(STUBBORNS, p=STUBBORNS_PROB)
    player = Strategy(initial, depend, random, stubborn)
    player_name = player.strategy_type
    player_type_count[player_name] += 1
    count = player_type_count[player_name]
    player_name = player_name + '_' + str(count)
    players[player_name] = player

# Double round, even with itself
matches = itertools.chain(itertools.product(players.values(), players.values()), ((_player, _player) for _player in players.values()))
matches = np.random.permutation(list(matches))
for game in range(1000):
    home_player = matches[game][0]
    away_player = matches[game][1]
    home_player.play(away_player)

print("Player types and their occurances:")
for name, count in player_type_count.items():
    print('\t'+name+': '+str(count))

player_type_scores = dict.fromkeys(PLAYER_TYPES, 0)
player_scores = {}
for name, player in players.items():
    player_type_scores[player.strategy_type] += player.score
    player_scores[name] = player.score
average_scores_by_type = {key: value/player_type_count[key] for key, value in player_type_scores.items()}
average_scores_by_type = sorted(average_scores_by_type.items(), key=operator.itemgetter(1), reverse=True)
scores_by_player= sorted(player_scores.items(), key=operator.itemgetter(1), reverse=True)

print("Average scores by type:")
for name, score in average_scores_by_type:
    print('\t'+name+': '+str(score))

print("Players finishing on podium:")
for name, score in scores_by_player[:3]:
    print('\t'+name+': '+str(score))
