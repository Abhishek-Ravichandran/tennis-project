import csv
import urllib2
from collections import defaultdict

def init_stats(valid_matches=None):
    
    player_matches = defaultdict(list)
    surfaces = defaultdict(str)
    handedness = defaultdict(str)
    match_players = defaultdict(lambda : defaultdict(str))
    num_matches = defaultdict(lambda : defaultdict(int))
    
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-matches.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    #get player matches, player handedness and match surfaces
    for match in cr:
        player1 = match[1].strip().lower()
        player2 = match[2].strip().lower()
        player_matches[player1].append(match[0])
        player_matches[player2].append(match[0])
        
        match_players[match[0]]['player1'] = player1
        match_players[match[0]]['player2'] = player2
        handedness[player1] = match[3]
        handedness[player2] = match[4]
        surfaces[match[0]] = match[11].strip()
    
    #get valid matches and match counts per surface
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    for match in cr:
        if valid_matches is None or match[0] in valid_matches:
            player1 = match_players[match[0]]['player1']
            player2 = match_players[match[0]]['player2']
        
            num_matches[player1][match[11]] += 1
            num_matches[player2][match[11]] += 1
    
    return match_players, num_matches, surfaces, handedness