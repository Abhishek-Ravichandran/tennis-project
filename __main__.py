import argparse
from mc_simulator import TennisMonteCarloSimulator as MCS
from collections import Counter

parser = argparse.ArgumentParser(description='Run a Markov monte carlo simulation of a match.')
parser.add_argument('player1', help='The player who serves first serve.')
parser.add_argument('player2', help='The player who receives the first serve.')
parser.add_argument('surface', help='The surface the players play on',
    choices=('Indoor Hard', 'Hard', 'Clay', 'Grass'))
default_sims = 100
parser.add_argument('sets_in_match', nargs='?', type=int, default=3,
    choices=(3, 5), help='The number of sets in a match.')
parser.add_argument('sim_count', nargs='?', type=int, default=default_sims,
    help='The number of simulations to run. default is ' + str(default_sims) + '.')

args = parser.parse_args()

# Generate the player dictionary here
player_data = {}
# TODO

simulator = MCS(args.surface, args.player1, args.player2, args.sets_in_match)

wins = Counter()
for iteration in range(args.sim_count):
    winner = simulator.simulate()
    wins[winner] += 1

print wins.most_common(2)