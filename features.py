import sys
import csv
import urllib2
from collections import defaultdict
from overview import init_stats

def get_return_effectiveness(match_players, valid_matches, num_matches, surfaces):
    
    return_effectiveness = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(float)))))
    
    #get return winner %s per serve style
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-stats-ReturnOutcomes.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    serve_styles = { 
                    '4D': { 'side': 'deuce', 'style': 'wide' },
                    '4A': { 'side': 'ad',    'style': 'wide' },
                    '5D': { 'side': 'deuce', 'style': 'body' },
                    '5A': { 'side': 'ad',    'style': 'body' },
                    '6D': { 'side': 'deuce', 'style': 't'    },
                    '6A': { 'side': 'ad',    'style': 't'    }
                   }
    
    for match in cr:
        if match[0] not in valid_matches: continue
        if match[1] == '1':
            player = match_players[match[0]]['player1']
        else:
            player = match_players[match[0]]['player2']
        surface = surfaces[match[0]]
        
        #only pick rows with serve style information
        if match[2] in serve_styles.keys() and float(match[3]) != 0:
            return_effectiveness[player][surface][serve_styles[match[2]]['side']][serve_styles[match[2]]['style']]['w'] += float(match[9]) / float(match[3])
    
    #get return ufe %s per serve style
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-stats-ReturnDepth.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    for match in cr:
        if match[0] not in valid_matches: continue
        if match[1] == '1':
            player = match_players[match[0]]['player1']
        else:
            player = match_players[match[0]]['player2']
        surface = surfaces[match[0]]
        
        #only pick rows with serve style information
        if match[2] in serve_styles.keys() and float(match[3]) != 0:
            return_effectiveness[player][surface][serve_styles[match[2]]['side']][serve_styles[match[2]]['style']]['ufe'] += float(match[7]) / float(match[3])
    
    #normalize w% and ufe%
    for player in return_effectiveness.keys():
        for surface in return_effectiveness[player].keys():
            for serve_style in serve_styles.keys():
                return_effectiveness[player][surface][serve_styles[serve_style]['side']][serve_styles[serve_style]['style']]['w'] /= num_matches[player][surface]
                return_effectiveness[player][surface][serve_styles[serve_style]['side']][serve_styles[serve_style]['style']]['ufe'] /= num_matches[player][surface]
    
    return return_effectiveness
    
def get_shot_dir_proc(match_players, valid_matches, num_matches, surfaces):
    
    shot_dir_proclivity = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(float))))
    
    #get shot dir proclivities
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-stats-ShotDirOutcomes.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    shot_styles = {
                    'F-XC':  { 'style': 'fh', 'direction': 'CC' },
                    'F-DTM': { 'style': 'fh', 'direction': 'DTM'},
                    'F-DTL': { 'style': 'fh', 'direction': 'DTL'},
                    'F-IO':  { 'style': 'fh', 'direction': 'IO' },
                    'F-II':  { 'style': 'fh', 'direction': 'II' },
                    'B-XC':  { 'style': 'bh', 'direction': 'CC' },
                    'B-DTM': { 'style': 'bh', 'direction': 'DTM'},
                    'B-DTL': { 'style': 'bh', 'direction': 'DTL'},
                    'B-IO':  { 'style': 'bh', 'direction': 'IO' },
                    'B-II':  { 'style': 'bh', 'direction': 'II' },
                    'S-XC':  { 'style': 'sl', 'direction': 'CC' },
                    'S-DTM': { 'style': 'sl', 'direction': 'DTM'},
                    'S-DTL': { 'style': 'sl', 'direction': 'DTL'},
                    'S-IO':  { 'style': 'sl', 'direction': 'IO' },
                    'S-II':  { 'style': 'sl', 'direction': 'II' }
                  }
    
    current_match_id = None
    current_match_stats = defaultdict(lambda : defaultdict(int))
    for match in cr:
        if match[0] not in valid_matches: continue
        if match[0] != current_match_id:
            for player in current_match_stats.keys():
                total = sum(int(shot_dir) for shot_dir in current_match_stats[player].values())
                for shot_dir in current_match_stats[player].keys():
                    shot_dir_proclivity[match_players[current_match_id][player]][surfaces[current_match_id]][shot_styles[shot_dir]['style']][shot_styles[shot_dir]['direction']] += float(current_match_stats[player][shot_dir]) / float(total)
            current_match_id = match[0]
            current_match_stats = defaultdict(lambda : defaultdict(int))
        else:
            if match[1] == '1':
                current_match_stats['player1'][match[2]] = match[3]
            else:
                current_match_stats['player2'][match[2]] = match[3]
    
    for player in current_match_stats.keys():
        total = sum(int(shot_dir) for shot_dir in current_match_stats[player].values())
        for shot_dir in current_match_stats[player].keys():
            shot_dir_proclivity[match_players[current_match_id][player]][surfaces[current_match_id]][shot_styles[shot_dir]['style']][shot_styles[shot_dir]['direction']] += float(current_match_stats[player][shot_dir]) / float(total)
    
    #normalize shot_dir_proclivity
    for player in shot_dir_proclivity.keys():
        for surface in shot_dir_proclivity[player].keys():
            for style in shot_dir_proclivity[player][surface].keys():
                for direction in shot_dir_proclivity[player][surface][style].keys():
                    shot_dir_proclivity[player][surface][style][direction] /= num_matches[player][surface]
    
    return shot_dir_proclivity

def get_shot_type_stats(match_players, valid_matches, num_matches, surfaces):
    
    shot_type_proclivity = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(float))))
    shot_type_effectiveness = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict(float)))))
    
    #get shot type proclivity and effectiveness
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_MatchChartingProject/master/charting-m-stats-ShotTypes.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    
    current_player_stats = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))
    current_player = None
    current_surface = None
    for match in cr:
        if match[0] not in valid_matches: continue
        if match[2] == 'Total':
            for style in current_player_stats.keys():
                total_sum = sum(int(current_player_stats[style][style_type]['total']) for style_type in current_player_stats[style].keys())
                for style_type in current_player_stats[style].keys():
                    shot_type_proclivity[current_player][current_surface][style][style_type] += float(current_player_stats[style][style_type]['total']) / float(total_sum)
                    shot_type_effectiveness[current_player][current_surface][style][style_type]['w'] += float(current_player_stats[style][style_type]['w']) / float(current_player_stats[style][style_type]['total'])
                    shot_type_effectiveness[current_player][current_surface][style][style_type]['ife'] += float(current_player_stats[style][style_type]['ife']) / float(current_player_stats[style][style_type]['total'])
                    shot_type_effectiveness[current_player][current_surface][style][style_type]['ufe'] += float(current_player_stats[style][style_type]['ufe']) / float(current_player_stats[style][style_type]['total'])
            current_player_stats = defaultdict(lambda : defaultdict(lambda : defaultdict(float)))
            if match[1] == '1': current_player = match_players[match[0]]['player1']
            else: current_player = match_players[match[0]]['player2']
            current_surface = surfaces[match[0]]
        elif match[2] in ['F', 'U', 'L', 'V', 'O', 'H', 'J', 'T']:
            current_player_stats['fh'][match[2]]['total'] = match[3]
            current_player_stats['fh'][match[2]]['w'] = match[5]
            current_player_stats['fh'][match[2]]['ife'] = match[6]
            current_player_stats['fh'][match[2]]['ufe'] = match[7]
        elif match[2] in ['B', 'Y', 'M', 'Z', 'P', 'I', 'K', 'T']:
            current_player_stats['bh'][match[2]]['total'] = match[3]
            current_player_stats['bh'][match[2]]['w'] = match[5]
            current_player_stats['bh'][match[2]]['ife'] = match[6]
            current_player_stats['bh'][match[2]]['ufe'] = match[7]
        elif match[2] in ['R', 'S']:
            current_player_stats['slc'][match[2]]['total'] = match[3]
            current_player_stats['slc'][match[2]]['w'] = match[5]
            current_player_stats['slc'][match[2]]['ife'] = match[6]
            current_player_stats['slc'][match[2]]['ufe'] = match[7]
    
    for style in current_player_stats.keys():
        total_sum = sum(int(current_player_stats[style][style_type]['total']) for style_type in current_player_stats[style].keys())
        for style_type in current_player_stats[style].keys():
            shot_type_proclivity[current_player][current_surface][style][style_type] += float(current_player_stats[style][style_type]['total']) / float(total_sum)
            shot_type_effectiveness[current_player][current_surface][style][style_type]['w'] += float(current_player_stats[style][style_type]['w']) / float(current_player_stats[style][style_type]['total'])
            shot_type_effectiveness[current_player][current_surface][style][style_type]['ife'] += float(current_player_stats[style][style_type]['ife']) / float(current_player_stats[style][style_type]['total'])
            shot_type_effectiveness[current_player][current_surface][style][style_type]['ufe'] += float(current_player_stats[style][style_type]['ufe']) / float(current_player_stats[style][style_type]['total'])
    
    #normalize proc and effectiveness
    for player in shot_type_proclivity.keys():
        for surface in shot_type_proclivity[player].keys():
            for style in shot_type_proclivity[player][surface].keys():
                for shot_type in shot_type_proclivity[player][surface][style].keys():
                    shot_type_proclivity[player][surface][style][shot_type] /= num_matches[player][surface]
                    shot_type_effectiveness[player][surface][style][shot_type]['w'] /= num_matches[player][surface]
                    shot_type_effectiveness[player][surface][style][shot_type]['ife'] /= num_matches[player][surface]
                    shot_type_effectiveness[player][surface][style][shot_type]['ufe'] /= num_matches[player][surface]
    
    return shot_type_proclivity, shot_type_effectiveness

if __name__ == "__main__":
    
    #lower limit for number of matches per player
    limit = 0

    match_players, valid_matches, num_matches, surfaces, handedness = init_stats(0)
    
    return_effectiveness = get_return_effectiveness(match_players, valid_matches, num_matches, surfaces)
    
    shot_dir_proclivity = get_shot_dir_proc(match_players, valid_matches, num_matches, surfaces)
    
    shot_type_proclivity, shot_type_effectiveness = get_shot_type_stats(match_players, valid_matches, num_matches, surfaces)
    
    ofile  = open('features.csv', "wb")
    writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
    
    serve_side_keys = ["deuce", "ad"]
    serve_type_keys = ["wide", "body", "t"]
    serve_stat_keys = ["w", "ufe"]
    
    shot_style_keys = ["fh", "bh", "slc"]
    direction_keys = {
                        "fh": ["CC", "DTM", "DTL", "IO", "II"],
                        "bh": ["CC", "DTM", "DTL", "IO"],
                        "slc": ["CC", "DTM", "DTL", "IO"]
                    }
    
    shot_type_keys = {
                        "fh": ["F", "H", "J", "L", "O", "U", "T", "V"],
                        "bh": ["B", "I", "K", "M", "P", "Y", "Z"],
                        "slc": ["S", "R"]
                    }
    
    shot_stat_keys = ["ife", "ufe", "w"]
    
    with open('data/match_winner.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            player1 = match_players[row[0]]['player1']
            player2 = match_players[row[0]]['player2']
            surface = surfaces[row[0]]
            
            if surface not in ['Grass', 'Clay', 'Hard']: continue
            if len(row) < 4: print row
            
            new_row = [row[0], row[3]]
            for serve_side in serve_side_keys:
                for serve_type in serve_type_keys:
                    for stat_type in serve_stat_keys:
                        new_row.append(return_effectiveness[player1][surface][serve_side][serve_type][stat_type] - return_effectiveness[player2][surface][serve_side][serve_type][stat_type])
            
            for shot_style in shot_style_keys:
                for direction in direction_keys[shot_style]:
                    new_row.append(shot_dir_proclivity[player1][surface][shot_style][direction] - shot_dir_proclivity[player2][surface][shot_style][direction])
            
            for shot_style in shot_style_keys:
                for shot_type in shot_type_keys[shot_style]:
                    new_row.append(shot_type_proclivity[player1][surface][shot_style][shot_type] - shot_type_proclivity[player2][surface][shot_style][shot_type])
            
            for shot_style in shot_style_keys:
                for shot_type in shot_type_keys[shot_style]:
                    for stat_type in shot_stat_keys:
                        new_row.append(shot_type_effectiveness[player1][surface][shot_style][shot_type][stat_type] - shot_type_effectiveness[player2][surface][shot_style][shot_type][stat_type])
            
            print len(new_row)
            writer.writerow(new_row)