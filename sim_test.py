from engine import overallSim, Point
from overview import init_stats
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import LeaveOneOut
import csv

correct = 0
total = 0
match_players, num_matches, surfaces, handedness = init_stats()

main_file = "data/match_winner.csv"
all_matches = set([])
with open(main_file, 'r') as f:
    cr = csv.reader(f)
    for row in cr:
        all_matches.add(row[0])

LO_file = "data/match_winner_hard.csv"

LO_matches = []
winners = dict()

with open(LO_file, 'r') as f:
    cr = csv.reader(f)
    for row in cr:
        LO_matches.append(row[0])
        winners[row[0]] = row[3]

loo = LeaveOneOut()

# point = Point(valid_matches, 'Grass')
# print len(all_matches)

for _, test in loo.split(LO_matches):

    to_leave_out = set([LO_matches[test[0]]])
    valid_matches = all_matches - to_leave_out
    point = Point(valid_matches, 'Hard')
    
    to_leave_out = to_leave_out.pop() 
    
    p1 = match_players[to_leave_out]['player1']
    p2 = match_players[to_leave_out]['player2']
    # surface = surfaces[to_leave_out].strip()
    # point.surface = surface
    
    res = overallSim(p1, p2, point)
    winner = winners[to_leave_out]
    if res == winner: correct += 1
    total += 1
    
    if total % 10 == 0: print total, correct/float(total)
    print p1, p2, winner, res

print correct/float(total)

# X_train, X_test, y_train, y_test = train_test_split(all_matches, winners, test_size=0.2)
# valid_matches = set(X_train)

# point = Point(valid_matches, 'Grass')

# print X_test

# for match_id, winner in zip(X_test, y_test):
    # p1 = match_players[match_id]['player1']
    # p2 = match_players[match_id]['player2']
    # surface = surfaces[match_id]
    # point.surface = surface
    
#     res = overallSim(p1, p2, point)
#     if res == winner: correct += 1
#     total += 1
    
#     print p1, p2, winner, res
    
# print correct/float(total)