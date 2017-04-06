"""
Script for getting the match winners and outputting them to a CSV. Please do not
run as it will overwrite the various winner files which will delete the manual updates
- Takes a number as a parameter indicating the minimum matches on a surface required of
  both players for a match to be considered for simulation.
"""

import argparse
import urllib2
import csv
import collections

parser = argparse.ArgumentParser(description='Make lists of match winners subject to a threshold')
parser.add_argument('threshold', type=int, default=3, nargs='?', \
    help='The minimum games on a surface required to include a player\'s match')
args = parser.parse_args()
print 'Using threshold', args.threshold
debug = False

def match_qualified(match_id, matches_to_players, player_to_surface_to_count, count_threshold):
    player_1 = matches_to_players[match_id]['player1']
    player_2 = matches_to_players[match_id]['player2']
    return player_to_surface_to_count[player_1][surface] >= count_threshold and \
        player_to_surface_to_count[player_2][surface] >= count_threshold

overrides = {
    '20150127-M-Australian_Open-QF-Stanislas_Wawrinka_-Kei_Nishikori' : 'stanislas wawrinka',
    '20151022-M-Vienna-R16-Jo_Wilfried_Tsonga-Lukas_Rosol'            : 'lukas rosol',
    '20140122-M-Australian_Open-QF-Novak_Djokovic-Stanislas_Wawrinka_': 'stanislas wawrinka',
    '20130125-M-Australian_Open-SF-Roger_Federer-Andy_Murray_'        : 'andy murray',
    '20110911-M-US_Open-F-Rafael_Nadal_-Novak_Djokovic'               : 'novak djokovic',
    '20101121-M-Tour_Finals-RR-Andy_Murray_-Roger_Federer'            : 'roger federer',
    '20080125-M-Australian_Open-SF-Jo_Wilfried_Tsonga_-Rafael_Nadal'  : 'jo wilfried tsonga'
}

# GET for all match IDs
url = "https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-matches.csv"

# Want to build a file of matches where both players have enough games for each surface 
# First build a dict of surface -> [match_ids] and a dict of player -> surface -> match count
surface_to_matches = collections.defaultdict(list)
player_to_surface_to_count = collections.defaultdict(collections.Counter)
matches_to_players = collections.defaultdict(dict)

response = urllib2.urlopen(url)
cr = csv.reader(response)
next(cr) # throw away header line
for match_record in cr:
    match_id = match_record[0]
    player_1 = match_record[1].lower().strip()
    player_2 = match_record[2].lower().strip()
    surface  = match_record[11].lower().strip()
    
    surface_to_matches[surface].append(match_id)
    player_to_surface_to_count[player_1][surface] += 1
    player_to_surface_to_count[player_2][surface] += 1
    matches_to_players[match_id]['player1'] = player_1
    matches_to_players[match_id]['player2'] = player_2

# Then, iterate over each match list and include in the surface csv only if both players have enough matches on the surface
for surface, match_ids in surface_to_matches.iteritems():
    qualifying_match_ids = [match_id for match_id in match_ids if match_qualified(match_id, matches_to_players, player_to_surface_to_count, args.threshold)]
    print 'ignoring', len(match_ids) - len(qualifying_match_ids), 'matches for surface', surface
    with open('../data/match_winner_' + surface.replace(' ', '_') + '.csv', 'wb') as f:
        csvfile = csv.writer(f)
        for match_id in qualifying_match_ids:
            # Scrape the winner
            url = "http://www.tennisabstract.com/charting/" + match_id + ".html"
            player_1 = matches_to_players[match_id]['player1']
            player_2 = matches_to_players[match_id]['player2']
            try:
                response = urllib2.urlopen(url).read().lower()
                if (player_1 + " d. " + player_2).lower() in response:
                    csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), player_1.lower().strip()])
                    if debug:
                        print 'player 1', player_1, 'won match', match_id, 'on surface', surface
                elif (player_2 + " d. " + player_1).lower() in response:
                    csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), player_2.lower().strip()])
                    if debug:
                        print 'player 2', player_2, 'won match', match_id, 'on surface', surface
                else:
                    # To signify an error. Shouldn't happen.
                    if match_id in overrides:
                        print 'Used override for match', match_id
                        csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), overrides[match_id]])
                    else:
                        print 'failed to find a winner for match', match_id, 'on surface', surface
                        csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), 'unknown'])
            except urllib2.HTTPError:
                if match_id in overrides:
                    print 'Used override for match', match_id
                    csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), overrides[match_id]])
                else:
                    print 'httperror finding a winner for match', match_id, 'on surface', surface
                    csvfile.writerow([match_id, player_1.lower().strip(), player_2.lower().strip(), 'unknown'])
