from overview import init_stats
from features import get_return_effectiveness, get_shot_dir_proc, get_shot_type_stats
from featureExtraction import getStats
import numpy as np
import sys

class Point:
    
    def __init__(self, valid_matches, surface):
        self.surface = surface
        self.player1 = None
        self.player2 = None
        self.serveSide = None

        self.serveStyleProbs, self.serveInProb, self.serveQuality = getStats(valid_matches)
        self.match_players, self.num_matches, self.surfaces, self.handedness = init_stats(valid_matches)
        self.return_effectiveness = get_return_effectiveness(self.match_players, valid_matches, self.num_matches, self.surfaces)
        self.shot_dir_proclivity = get_shot_dir_proc(self.match_players, valid_matches, self.num_matches, self.surfaces)
        self.shot_type_proclivity, self.shot_type_effectiveness = get_shot_type_stats(self.match_players, valid_matches, self.num_matches, self.surfaces)
    
    def serve(self):
        Player = self.player1
        Surface = self.surface
        Side = self.serveSide
        OtherPlayer = self.player2
        
        diceRoll = np.random.ranf()
        
        #wide,body,T probabilities
        sProbs = self.serveStyleProbs[Player][Surface][Side]
        
        if diceRoll <= sProbs[0]:
            serveStyle = 'wide'
        elif diceRoll <= sProbs[0] + sProbs[1]:
            serveStyle = 'body'
        else:
            serveStyle = 't'
        
        inProbs = self.serveInProb[Player][Surface][Side][serveStyle]
        
        diceRoll = np.random.ranf()
        
        if diceRoll <= inProbs[0]:
            serveIn = '1st'
        elif diceRoll <= inProbs[0] + inProbs[1]:
            serveIn = '2nd'
        else:
            serveIn = 'df'
        
        #end the game point goes to other player
        if serveIn == 'df':
            # print 'other player won the point: double fault'
            return OtherPlayer
        
        qualityProbs = self.serveQuality[Player][Surface][Side][serveStyle][serveIn]
        
        ace = qualityProbs[0]
        forcedError = qualityProbs[1]
        
        diceRoll = np.random.ranf()
        
        #end game point goes to you
        
        if diceRoll <= ace+forcedError:
            # print 'player won the point: ace or forced error'
            return Player
            
        return self.returnServe(serveStyle)

    def returnServe(self, serveStyle):
        
        diceRoll = np.random.ranf()
        
        if self.serveSide == 'adv':
            serveSide = "ad"
        else:
            serveSide = "deuce"
        
        returnProbs = self.return_effectiveness[self.player2][self.surface][serveSide][serveStyle]
        
        returnDir = np.random.randint(low=0, high=3)
        if returnDir == 0:
            return self.Rally(self.player1, 'left', returnProbs['w'], returnProbs['ufe'], 0, self.player2)
        elif returnDir == 1:
            return self.Rally(self.player1, 'mid', returnProbs['w'], returnProbs['ufe'], 0, self.player2)
        else:
            return self.Rally(self.player1, 'right', returnProbs['w'], returnProbs['ufe'], 0, self.player2)
    
    def Rally(self, player, returnDir, winnerPercentage, unforcedError, inducedForced, otherPlayer):
        
        diceRoll = np.random.ranf()
        
        #check if winner or unforced or inducedForced here
        if diceRoll <= winnerPercentage+inducedForced:
            #end game other player gets point
            # print otherPlayer + ' gets a point. ' + otherPlayer + ' hit winner or induced forced error'
            return otherPlayer
            
        elif diceRoll <= winnerPercentage+inducedForced+unforcedError:
            #end game current player gets point
            # print player + ' gets a point. ' + otherPlayer + ' committed unforced error'
            return player
        
        shotDirProbs = self.shot_dir_proclivity[player][self.surface]

        if self.handedness[player] == 'L' and returnDir == 'left':
            #sample from fh CC, fh DTM, fh DTL, bh IO, bh II, fh-sl CC, fh-sl DTM, fh-sl DTL, bh-sl IO
            relevantProbs = [shotDirProbs['fh']['CC'], shotDirProbs['fh']['DTM'], shotDirProbs['fh']['DTL'], shotDirProbs['bh']['IO'], shotDirProbs['bh']['II'], shotDirProbs['sl']['CC'], shotDirProbs['sl']['DTM'], shotDirProbs['sl']['DTL'], shotDirProbs['sl']['IO']]
        
        elif self.handedness[player] == 'L' and returnDir == 'right':
            #sample from fh IO, fh II, bh CC, bh DTM, bh DTL, bh-sl CC, bh-sl DTM, bh-sl DTL, fh-sl IO
            relevantProbs = [shotDirProbs['fh']['IO'], shotDirProbs['fh']['II'], shotDirProbs['bh']['CC'], shotDirProbs['bh']['DTM'], shotDirProbs['bh']['DTL'], shotDirProbs['sl']['CC'], shotDirProbs['sl']['DTM'], shotDirProbs['sl']['DTL'], shotDirProbs['sl']['IO']]
            
        elif self.handedness[player] == 'R' and returnDir == 'left':
            #sample from fh IO, fh II, bh CC, bh DTM, bh DTL, bh-sl CC, bh-sl DTM, bh-sl DTL, fh-sl IO
            relevantProbs = [shotDirProbs['fh']['IO'], shotDirProbs['fh']['II'], shotDirProbs['bh']['CC'], shotDirProbs['bh']['DTM'], shotDirProbs['bh']['DTL'], shotDirProbs['sl']['CC'], shotDirProbs['sl']['DTM'], shotDirProbs['sl']['DTL'], shotDirProbs['sl']['IO']]
        
        elif self.handedness[player] == 'R' and returnDir == 'right':
            #sample from fh CC, fh DTM, fh DTL, bh IO, bh II, fh-sl CC, fh-sl DTM, fh-sl DTL, bh-sl IO
            relevantProbs = [shotDirProbs['fh']['CC'], shotDirProbs['fh']['DTM'], shotDirProbs['fh']['DTL'], shotDirProbs['bh']['IO'], shotDirProbs['bh']['II'], shotDirProbs['sl']['CC'], shotDirProbs['sl']['DTM'], shotDirProbs['sl']['DTL'], shotDirProbs['sl']['IO']]   
            
        else:
            #sample from fh CC, fh DTM, bh CC, bh DTM, fh IO, bh IO, sl CC, sl DTM, sl IO
            relevantProbs = [shotDirProbs['fh']['CC'], shotDirProbs['fh']['DTM'], shotDirProbs['bh']['CC'], shotDirProbs['bh']['DTM'], shotDirProbs['fh']['IO'], shotDirProbs['bh']['IO'], shotDirProbs['sl']['CC'], shotDirProbs['sl']['DTM'], shotDirProbs['sl']['IO']]
        
        diceRoll = np.random.ranf()
        
        #normalize it
        summation = np.sum(relevantProbs)
        for x in range(len(relevantProbs)):
            relevantProbs[x] /= summation
        
        cummulativeSum = 0
        for x in range(len(relevantProbs)):
            cummulativeSum += relevantProbs[x] 
            if diceRoll <= cummulativeSum:
                style = x
                break
        
        if self.handedness[player] == 'L' and returnDir == 'left':
            if style == 0:
                shotStyle = 'fh'
                newReturnDir = 'left'
            elif style == 1:
                shotStyle = 'fh'
                newReturnDir = 'mid'
            elif style == 2:
                shotStyle = 'fh'
                newReturnDir = 'right'
            elif style == 3:
                shotStyle = 'bh'
                newReturnDir = 'left'
            elif style == 4:
                shotStyle = 'bh'
                newReturnDir = 'right'
            elif style == 5:
                shotStyle = 'slc'
                newReturnDir = 'left'
            elif style == 6:
                shotStyle = 'slc'
                newReturnDir = 'mid'
            elif style == 7:
                shotStyle = 'slc'
                newReturnDir = 'right'
            elif style == 8:
                shotStyle = 'slc'
                newReturnDir = 'left'
                
        elif self.handedness[player] == 'L' and returnDir == 'right':
            if style == 0:
                shotStyle = 'fh'
                newReturnDir = 'right'
            elif style == 1:
                shotStyle = 'fh'
                newReturnDir = 'left'
            elif style == 2:
                shotStyle = 'bh'
                newReturnDir = 'right'
            elif style == 3:
                shotStyle = 'bh'
                newReturnDir = 'mid'
            elif style == 4:
                shotStyle = 'bh'
                newReturnDir = 'left'
            elif style == 5:
                shotStyle = 'slc'
                newReturnDir = 'right'
            elif style == 6:
                shotStyle = 'slc'
                newReturnDir = 'mid'
            elif style == 7:
                shotStyle = 'slc'
                newReturnDir = 'left'
            elif style == 8:
                shotStyle = 'slc'
                newReturnDir = 'right'
            
        elif self.handedness[player] == 'R' and returnDir == 'left':
            if style == 0:
                shotStyle = 'fh'
                newReturnDir = 'left'
            elif style == 1:
                shotStyle = 'fh'
                newReturnDir = 'right'
            elif style == 2:
                shotStyle = 'bh'
                newReturnDir = 'left'
            elif style == 3:
                shotStyle = 'bh'
                newReturnDir = 'mid'
            elif style == 4:
                shotStyle = 'bh'
                newReturnDir = 'right'
            elif style == 5:
                shotStyle = 'slc'
                newReturnDir = 'left'
            elif style == 6:
                shotStyle = 'slc'
                newReturnDir = 'mid'
            elif style == 7:
                shotStyle = 'slc'
                newReturnDir = 'right'
            elif style == 8:
                shotStyle = 'slc'
                newReturnDir = 'left'
        
        elif self.handedness[player] == 'R' and returnDir == 'right':
            if style == 0:
                shotStyle = 'fh'
                newReturnDir = 'right'
            elif style == 1:
                shotStyle = 'fh'
                newReturnDir = 'mid'
            elif style == 2:
                shotStyle = 'fh'
                newReturnDir = 'left'
            elif style == 3:
                shotStyle = 'bh'
                newReturnDir = 'right'
            elif style == 4:
                shotStyle = 'bh'
                newReturnDir = 'left'
            elif style == 5:
                shotStyle = 'slc'
                newReturnDir = 'right'
            elif style == 6:
                shotStyle = 'slc'
                newReturnDir = 'mid'
            elif style == 7:
                shotStyle = 'slc'
                newReturnDir = 'left'
            elif style == 8:
                shotStyle = 'slc'
                newReturnDir = 'right'
            
        else:
            #sample from fh CC, fh DTM, bh CC, bh DTM, fh IO, bh IO, sl CC, sl DTM, sl IO
            if self.handedness[player] == 'R':
                if style == 0:
                    shotStyle = 'fh'
                    newReturnDir = 'right'
                elif style == 1:
                    shotStyle = 'fh'
                    newReturnDir = 'mid'
                elif style == 2:
                    shotStyle = 'bh'
                    newReturnDir = 'left'
                elif style == 3:
                    shotStyle = 'bh'
                    newReturnDir = 'mid'
                elif style == 4:
                    shotStyle = 'fh'
                    newReturnDir = 'left'
                elif style == 5:
                    shotStyle = 'bh'
                    newReturnDir = 'right'
                elif style == 6:
                    shotStyle = 'slc'
                    newReturnDir = 'right'
                elif style == 7:
                    shotStyle = 'slc'
                    newReturnDir = 'mid'
                elif style == 8:
                    shotStyle = 'slc'
                    newReturnDir = 'left'

            else:
                if style == 0:
                    shotStyle = 'fh'
                    newReturnDir = 'left'
                elif style == 1:
                    shotStyle = 'fh'
                    newReturnDir = 'mid'
                elif style == 2:
                    shotStyle = 'bh'
                    newReturnDir = 'right'
                elif style == 3:
                    shotStyle = 'bh'
                    newReturnDir = 'mid'
                elif style == 4:
                    shotStyle = 'fh'
                    newReturnDir = 'right'
                elif style == 5:
                    shotStyle = 'bh'
                    newReturnDir = 'left'
                elif style == 6:
                    shotStyle = 'slc'
                    newReturnDir = 'left'
                elif style == 7:
                    shotStyle = 'slc'
                    newReturnDir = 'mid'
                elif style == 8:
                    shotStyle = 'slc'
                    newReturnDir = 'right'
        
        # newReturnDir = "left"
        # diceRoll = np.random.ranf()
        # if diceRoll < 0.5:
        #     shotStyle = 'fh'
        #     shot_type = 'F'
        # else:
        #     shotStyle = 'bh'
        #     shot_type = 'B'
        
        shot_type_procs = self.shot_type_proclivity[player][self.surface][shotStyle]
        
        diceRoll = np.random.ranf()
        
        summation = 0
        for entry in shot_type_procs.keys():
            summation += shot_type_procs[entry]
            
        for entry in shot_type_procs.keys():
            shot_type_procs[entry] /= summation
        
        cummulativeSum = 0
        for entry in shot_type_procs.keys():
            cummulativeSum += shot_type_procs[entry] 
            if diceRoll <= cummulativeSum:
                shot_type = entry
                break
            
        #proclivity, shotStyle
        newWinnerPercentage = self.shot_type_effectiveness[player][self.surface][shotStyle][shot_type]['w'] 
        newUnforcedError = self.shot_type_effectiveness[player][self.surface][shotStyle][shot_type]['ufe']
        newInducedError = self.shot_type_effectiveness[player][self.surface][shotStyle][shot_type]['ife']
            
        return self.Rally(otherPlayer, newReturnDir, newWinnerPercentage, newUnforcedError, newInducedError, player)
            

def matchSim(player1, player2, p):
    p1_sets = 0
    p2_sets = 0
    games_per_set = []
    
    while p1_sets != 2 and p2_sets != 2:
        if sum(games_per_set) % 2 == 0:
            res = setSim(player1, player2, p)
        elif sum(games_per_set) % 2 == 1:
            res = setSim(player2, player1, p)
        
        if res == player1:
            p1_sets += 1
        else:
            p2_sets += 1
    
    if p1_sets > p2_sets:
        return player1
    else:
        return player2
        
        
def setSim(player1, player2, p):
    
    p1_games = 0
    p2_games = 0
    server = None
    receiver = None
    
    while not (p1_games >= 6 and p2_games <= p1_games - 2) and not (p2_games >= 6 and p1_games <= p2_games - 2):
        if server != player1:
            server = player1
            receiver = player2
        else:
            server = player2
            receiver = player1
        
        res = gameSim(server, receiver, p)
        
        if res == player1:
            p1_games += 1
        else:
            p2_games += 1
    
    # print "Set Result:", player1, p1_games, player2, p2_games
    if p1_games > p2_games:
        return player1
    else:
        return player2
            
def gameSim(server, receiver, p):
    p.player1 = server
    p.player2 = receiver
    p.serveSide = None
    
    p1_pts = 0
    p2_pts = 0
    serveSide = None
    while not (p1_pts >= 4 and p2_pts <= p1_pts - 2) and not (p2_pts >= 4 and p1_pts <= p2_pts - 2):
        if p.serveSide in [None, 'adv']:
            p.serveSide = "deuce"
        else:
            p.serveSide = "adv"
            
        if p.serve() == server:
            p1_pts += 1
        else:
            p2_pts += 1
    
    # print "Game Result:", server, p1_pts, receiver, p2_pts
    if p1_pts > p2_pts:
        return server
    else:
        return receiver

def overallSim(player1, player2, point, no_of_times=100):
    p1_matches = 0
    p2_matches = 0
    for i in range(no_of_times):
        res = matchSim(player1, player2, point)
        if res == player1:
            p1_matches += 1
        else:
            p2_matches += 1
            
    # print "Sim Results:", player1, p1_matches, player2, p2_matches
    if p1_matches > p2_matches: return player1
    else: return player2
    
if __name__ == "__main__":
    player1 = "Nicolas Almagro"
    player2 = "Roger Federer"
    surface = "Clay"
    overallSim(player1, player2, surface)
            
        
        

    
            
        
    
'''
probability of body,wide,T serve given side given surface
Pick one serve style

probability of 1st in, 2nd in, DF
    If DF: give point to other player
        end
    if 1st in:
        pick Ace given 1st given global_surface
        pick FcedError given 1st given global_surface
    if 2nd in:
        pick Ace given 2nd
        pick FcedError given 2nd

finalVector = [serveStyle, aceProb, fcedErrorProb]
Call Return(oppositePlayer,side, otherPlayerHandedNess, finalVector)

Return(player, side, handedNess, serveStyle, aceProb, fcedErrorProb, returnableProb):
    from AceProb and fcedErrorProb determine if game has ended:
        Game ended end other player gets point
    
    #Stats next state needs to determine if game ended
    From side and serveStyle
        Pick winnerPercentage
        Pick unforcedError percentage
    
    inducedForced = 0 for returns
    
    Rally(oppositePlayer, winnerPercentage, unforcedError, induceForced, futureBallPosition, otherPlayerHandedNess)
        
Rally(player, winnerPercentage, unforcedError, induceForced, style, otherPlayerHandedNess)
        
        winner = 0.2, induceForced = 0.3, unforcedError = 0.1, normal = 0.4
        if winnerPercentage or induceForced:
            end game, other player gets a point

        if unforcedError:
            end game, current player gets a point
            
            Sample from shot direction:
                FH, BH, OR SLICE
                    Sample shot type:
                    ADD ALL FH. BH or SLICE shot types, pick one shot types
                    Extract the winnerPercentage, induceForced, unforcedError

        Rally(player, winnerPercentage, unforcedError, induceForced, style, otherPlayerHandedNess)
'''