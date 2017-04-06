
'''
player[]grasstype[]serveside[]servetype[] - probability of servetype T,body,wide
- probability of 1st[]/2nd[]/df[] per 1st and 2nd, servequal[unfcd, w%]
'''

import csv
import numpy as np
from collections import defaultdict

# vector in the form wide,body,T probabilities
def getServeStyleProbabilities(validMatches):
    
    serveList = {}
    
    f = open('data/servedirection.csv')
    reader = csv.reader(f)
    
    idx = 0
    for row in reader:
        if idx != 0:
            if row[0] in validMatches:
                
                matchId = row[0].split('-')
                player1 = matchId[4].replace('_',' ').strip().lower()
                player2 = matchId[5].replace('_',' ').strip().lower()
                surface = validMatches[row[0]]
                if (not player1 in serveList):
                    serveList[str(player1)] = {}
                    
                if (not surface in serveList[str(player1)]):
                    serveList[str(player1)][surface] = {}
                    serveList[str(player1)][surface]['deuce'] = [0,0,0]
                    serveList[str(player1)][surface]['adv'] = [0,0,0]
                    
                if (not player2 in serveList):
                    serveList[player2] = {}
                
                if (not surface in serveList[str(player2)]):
                    serveList[str(player2)][surface] = {}
                    serveList[str(player2)][surface]['deuce'] = [0,0,0]
                    serveList[str(player2)][surface]['adv'] = [0,0,0]
                
                splitRow1 =  row[1].split(' ')
                if (splitRow1[1] == 'Total'):
                    if splitRow1[0] == '1':
                        deuceVector = serveList[str(player1)][surface]['deuce']
                        advVector = serveList[str(player1)][surface]['adv']
                        #wide
                        deuceVector[0] += int(row[2])
                        advVector[0] += int(row[5])
                        #body
                        deuceVector[1] += int(row[3])
                        advVector[1] += int(row[6])
                        #T
                        deuceVector[2] += int(row[4])
                        advVector[2] += int(row[7])
                    else:
                        deuceVector = serveList[str(player2)][surface]['deuce']
                        advVector = serveList[str(player2)][surface]['adv']
                        #wide
                        deuceVector[0] += int(row[2])
                        advVector[0] += int(row[5])
                        #body
                        deuceVector[1] += int(row[3])
                        advVector[1] += int(row[6])
                        #T
                        deuceVector[2] += int(row[4])
                        advVector[2] += int(row[7])
        idx = idx + 1
        
    for player in serveList:
        game = serveList[player]
        
        for surface in game:
            sides = game[surface]
            
            for side in sides:
                normalizedVector = sides[side]
                summation = np.sum(normalizedVector)
                for x in range(len(normalizedVector)):
                    normalizedVector[x] /= float(summation)
                
                serveList[player][surface][side] = normalizedVector
                
    return serveList
    
#vector is 1st in, 2nd in, double fault
def getServeInProbabilities(validMatches):
    
    serveList = {}
    
    f = open('data/svbreaktotal.csv')
    reader = csv.reader(f)
    
    idx = 0
    for row in reader:
        if idx != 0:
            if row[0] in validMatches:
                
                matchId = row[0].split('-')
                player1 = matchId[4].replace('_',' ').strip().lower()
                player2 = matchId[5].replace('_',' ').strip().lower()
                surface = validMatches[row[0]]
                if (not player1 in serveList):
                    serveList[str(player1)] = {}
                    
                if (not surface in serveList[str(player1)]):
                    serveList[str(player1)][surface] = {}
                    serveList[str(player1)][surface]['deuce'] = {}
                    serveList[str(player1)][surface]['deuce']['body'] = [0,0,0]
                    serveList[str(player1)][surface]['deuce']['wide'] = [0,0,0]
                    serveList[str(player1)][surface]['deuce']['t'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['adv'] = {}
                    serveList[str(player1)][surface]['adv']['body'] = [0,0,0]
                    serveList[str(player1)][surface]['adv']['wide'] = [0,0,0]
                    serveList[str(player1)][surface]['adv']['t'] = [0,0,0]
                    
                if (not player2 in serveList):
                    serveList[player2] = {}
                
                if (not surface in serveList[str(player2)]):
                    serveList[str(player2)][surface] = {}
                    serveList[str(player2)][surface]['deuce'] = {}
                    serveList[str(player2)][surface]['deuce']['body'] = [0,0,0]
                    serveList[str(player2)][surface]['deuce']['wide'] = [0,0,0]
                    serveList[str(player2)][surface]['deuce']['t'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['adv'] = {}
                    serveList[str(player2)][surface]['adv']['body'] = [0,0,0]
                    serveList[str(player2)][surface]['adv']['wide'] = [0,0,0]
                    serveList[str(player2)][surface]['adv']['t'] = [0,0,0]
                
                if row[1] == '1':
                    deuceVector = serveList[str(player1)][surface]['deuce']
                    dbVector = deuceVector['body']
                    dwVector = deuceVector['wide']
                    dtVector = deuceVector['t']
                    
                    advVector = serveList[str(player1)][surface]['adv']
                    abVector= advVector['body']
                    awVector = advVector['wide']
                    atVector = advVector['t']
                    
                    if row[2] == '5d':
                        dbVector[0] += int(row[9])
                        dbVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dbVector[2] += int(row[10])
                    
                    if row[2] == '4d':
                        dwVector[0] += int(row[9])
                        dwVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dwVector[2] += int(row[10])
                        
                    if row[2] == '6d':
                        dtVector[0] += int(row[9])
                        dtVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dtVector[2] += int(row[10])
                    
                    if row[2] == '5a':
                        abVector[0] += int(row[9])
                        abVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        abVector[2] += int(row[10])
                        
                    if row[2] == '4a':
                        awVector[0] += int(row[9])
                        awVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        awVector[2] += int(row[10])
                        
                    if row[2] == '6a':
                        atVector[0] += int(row[9])
                        atVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        atVector[2] += int(row[10])
                        
                else:
                    deuceVector = serveList[str(player2)][surface]['deuce']
                    dbVector = deuceVector['body']
                    dwVector = deuceVector['wide']
                    dtVector = deuceVector['t']
                    
                    advVector = serveList[str(player2)][surface]['adv']
                    abVector= advVector['body']
                    awVector = advVector['wide']
                    atVector = advVector['t']
                    
                    if row[2] == '5d':
                        dbVector[0] += int(row[9])
                        dbVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dbVector[2] += int(row[10])
                    
                    if row[2] == '4d':
                        dwVector[0] += int(row[9])
                        dwVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dwVector[2] += int(row[10])
                        
                    if row[2] == '6d':
                        dtVector[0] += int(row[9])
                        dtVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        dtVector[2] += int(row[10])
                    
                    if row[2] == '5a':
                        abVector[0] += int(row[9])
                        abVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        abVector[2] += int(row[10])
                        
                    if row[2] == '4a':
                        awVector[0] += int(row[9])
                        awVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        awVector[2] += int(row[10])
                        
                    if row[2] == '6a':
                        atVector[0] += int(row[9])
                        atVector[1] += int(row[3]) - int(row[9]) - int(row[10])
                        atVector[2] += int(row[10])
        idx = idx + 1
    
    
    for player in serveList:
        game = serveList[player]
        
        for surface in game:
            sides = game[surface]
            
            for side in sides:
                playStyles = sides[side]
                
                for style in playStyles:
                    
                    normalizedVector = playStyles[style]
                    summation = np.sum(normalizedVector)
                    for x in range(len(normalizedVector)):
                        if summation == 0:
                            normalizedVector[x] = 0
                        else:
                            normalizedVector[x] /= float(summation)
                
                    serveList[player][surface][side][style] = normalizedVector
    
                
    return serveList
        
#vector is aces, forcederror, totalpoints
def getServeQualityProbabilities(validMatches):
    
    serveList = {}
    
    f = open('data/svbreaksplit.csv')
    reader = csv.reader(f)
    
    idx = 0
    for row in reader:
        if idx != 0:
            if row[0] in validMatches:
                
                matchId = row[0].split('-')
                player1 = matchId[4].replace('_',' ').strip().lower()
                player2 = matchId[5].replace('_',' ').strip().lower()
                surface = validMatches[row[0]]
                if (not player1 in serveList):
                    serveList[str(player1)] = {}
                    
                if (not surface in serveList[str(player1)]):
                    serveList[str(player1)][surface] = {}
                    serveList[str(player1)][surface]['deuce'] = {}
                    serveList[str(player1)][surface]['deuce']['body'] = {}
                    serveList[str(player1)][surface]['deuce']['body']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['deuce']['body']['2nd'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['deuce']['wide'] = {}
                    serveList[str(player1)][surface]['deuce']['wide']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['deuce']['wide']['2nd'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['deuce']['t'] = {}
                    serveList[str(player1)][surface]['deuce']['t']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['deuce']['t']['2nd'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['adv'] = {}
                    serveList[str(player1)][surface]['adv']['body'] = {}
                    serveList[str(player1)][surface]['adv']['body']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['adv']['body']['2nd'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['adv']['wide'] = {}
                    serveList[str(player1)][surface]['adv']['wide']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['adv']['wide']['2nd'] = [0,0,0]
                    
                    serveList[str(player1)][surface]['adv']['t'] = {}
                    serveList[str(player1)][surface]['adv']['t']['1st'] = [0,0,0]
                    serveList[str(player1)][surface]['adv']['t']['2nd'] = [0,0,0]
                    
                if (not player2 in serveList):
                    serveList[player2] = {}
                
                if (not surface in serveList[str(player2)]):
                    serveList[str(player2)][surface] = {}
                    serveList[str(player2)][surface]['deuce'] = {}
                    serveList[str(player2)][surface]['deuce']['body'] = {}
                    serveList[str(player2)][surface]['deuce']['body']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['deuce']['body']['2nd'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['deuce']['wide'] = {}
                    serveList[str(player2)][surface]['deuce']['wide']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['deuce']['wide']['2nd'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['deuce']['t'] = {}
                    serveList[str(player2)][surface]['deuce']['t']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['deuce']['t']['2nd'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['adv'] = {}
                    serveList[str(player2)][surface]['adv']['body'] = {}
                    serveList[str(player2)][surface]['adv']['body']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['adv']['body']['2nd'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['adv']['wide'] = {}
                    serveList[str(player2)][surface]['adv']['wide']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['adv']['wide']['2nd'] = [0,0,0]
                    
                    serveList[str(player2)][surface]['adv']['t'] = {}
                    serveList[str(player2)][surface]['adv']['t']['1st'] = [0,0,0]
                    serveList[str(player2)][surface]['adv']['t']['2nd'] = [0,0,0]
                
                if row[1] == '1':
                    deuceVector = serveList[str(player1)][surface]['deuce']
                    db1Vector = deuceVector['body']['1st']
                    db2Vector = deuceVector['body']['2nd']
                    dw1Vector = deuceVector['wide']['1st']
                    dw2Vector = deuceVector['wide']['2nd']
                    dt1Vector = deuceVector['t']['1st']
                    dt2Vector = deuceVector['t']['1st']
                    
                    advVector = serveList[str(player1)][surface]['adv']
                    ab1Vector= advVector['body']['1st']
                    ab2Vector= advVector['body']['2nd']
                    aw1Vector = advVector['wide']['1st']
                    aw2Vector = advVector['wide']['2nd']
                    at1Vector = advVector['t']['1st']
                    at2Vector = advVector['t']['2nd']
                    
                    '''
                    1st
                    row[5] is aces
                    row[7] is fced
                    row[3] is total
                    
                    2nd
                    row[9] is total
                    row[11] is aces
                    row[13] is fced
                    '''
                    if row[2] == '5d':
                        db1Vector[0] += int(row[5])
                        db1Vector[1] += int(row[7])
                        db1Vector[2] += int(row[3])
                        
                        db2Vector[0] += int(row[11])
                        db2Vector[1] += int(row[13])
                        db2Vector[2] += int(row[9])
                    
                    if row[2] == '4d':
                        dw1Vector[0] += int(row[5])
                        dw1Vector[1] += int(row[7])
                        dw1Vector[2] += int(row[3])
                        
                        dw2Vector[0] += int(row[11])
                        dw2Vector[1] += int(row[13])
                        dw2Vector[2] += int(row[9])
                        
                    if row[2] == '6d':
                        dt1Vector[0] += int(row[5])
                        dt1Vector[1] += int(row[7])
                        dt1Vector[2] += int(row[3])
                        
                        dt2Vector[0] += int(row[11])
                        dt2Vector[1] += int(row[13])
                        dt2Vector[2] += int(row[9])
                    
                    if row[2] == '5a':
                        ab1Vector[0] += int(row[5])
                        ab1Vector[1] += int(row[7])
                        ab1Vector[2] += int(row[3])
                        
                        ab2Vector[0] += int(row[11])
                        ab2Vector[1] += int(row[13])
                        ab2Vector[2] += int(row[9])
                        
                    if row[2] == '4a':
                        aw1Vector[0] += int(row[5])
                        aw1Vector[1] += int(row[7])
                        aw1Vector[2] += int(row[3])
                        
                        aw2Vector[0] += int(row[11])
                        aw2Vector[1] += int(row[13])
                        aw2Vector[2] += int(row[9])
                        
                    if row[2] == '6a':
                        at1Vector[0] += int(row[5])
                        at1Vector[1] += int(row[7])
                        at1Vector[2] += int(row[3])
                        
                        at2Vector[0] += int(row[11])
                        at2Vector[1] += int(row[13])
                        at2Vector[2] += int(row[9])
                        
                else:
                    deuceVector = serveList[str(player2)][surface]['deuce']
                    db1Vector = deuceVector['body']['1st']
                    db2Vector = deuceVector['body']['2nd']
                    dw1Vector = deuceVector['wide']['1st']
                    dw2Vector = deuceVector['wide']['2nd']
                    dt1Vector = deuceVector['t']['1st']
                    dt2Vector = deuceVector['t']['1st']
                    
                    advVector = serveList[str(player2)][surface]['adv']
                    ab1Vector= advVector['body']['1st']
                    ab2Vector= advVector['body']['2nd']
                    aw1Vector = advVector['wide']['1st']
                    aw2Vector = advVector['wide']['2nd']
                    at1Vector = advVector['t']['1st']
                    at2Vector = advVector['t']['2nd']
                    
                    if row[2] == '5d':
                        db1Vector[0] += int(row[5])
                        db1Vector[1] += int(row[7])
                        db1Vector[2] += int(row[3])
                        
                        db2Vector[0] += int(row[11])
                        db2Vector[1] += int(row[13])
                        db2Vector[2] += int(row[9])
                    
                    if row[2] == '4d':
                        dw1Vector[0] += int(row[5])
                        dw1Vector[1] += int(row[7])
                        dw1Vector[2] += int(row[3])
                        
                        dw2Vector[0] += int(row[11])
                        dw2Vector[1] += int(row[13])
                        dw2Vector[2] += int(row[9])
                        
                    if row[2] == '6d':
                        dt1Vector[0] += int(row[5])
                        dt1Vector[1] += int(row[7])
                        dt1Vector[2] += int(row[3])
                        
                        dt2Vector[0] += int(row[11])
                        dt2Vector[1] += int(row[13])
                        dt2Vector[2] += int(row[9])
                    
                    if row[2] == '5a':
                        ab1Vector[0] += int(row[5])
                        ab1Vector[1] += int(row[7])
                        ab1Vector[2] += int(row[3])
                        
                        ab2Vector[0] += int(row[11])
                        ab2Vector[1] += int(row[13])
                        ab2Vector[2] += int(row[9])
                        
                    if row[2] == '4a':
                        aw1Vector[0] += int(row[5])
                        aw1Vector[1] += int(row[7])
                        aw1Vector[2] += int(row[3])
                        
                        aw2Vector[0] += int(row[11])
                        aw2Vector[1] += int(row[13])
                        aw2Vector[2] += int(row[9])
                        
                    if row[2] == '6a':
                        at1Vector[0] += int(row[5])
                        at1Vector[1] += int(row[7])
                        at1Vector[2] += int(row[3])
                        
                        at2Vector[0] += int(row[11])
                        at2Vector[1] += int(row[13])
                        at2Vector[2] += int(row[9])
                        
        idx = idx + 1
    
    
    for player in serveList:
        game = serveList[player]
        
        for surface in game:
            sides = game[surface]
            
            for side in sides:
                playStyles = sides[side]
                
                for style in playStyles:
                    ins = playStyles[style]
                    
                    for quality in ins:
                        
                        normalizedVector = ins[quality]
                        summation = float(normalizedVector[2])
                        
                        if summation == 0:
                            normalizedVector[0] = 0
                            normalizedVector[1] = 0
                            
                        else:
                            normalizedVector[0] = normalizedVector[0]/summation
                            normalizedVector[1] = normalizedVector[1]/summation
                        
                        serveList[player][surface][side][style][quality] = normalizedVector
    
    
    return serveList
    
def getSurfaces(valid_matches):
    surfaces = {}
    f = open('data/allmatches.csv')
    reader = csv.reader(f)
    
    idx = 0
    for row in reader:
        
        if idx != 0:
            matchId = row[0]
            surface = row[11]
            
            surfaces[matchId] = surface
        idx += 1
    
    for key in surfaces.keys():
        if key not in valid_matches:
            surfaces.pop(key)
    
    return surfaces
    
def getBaselineFeatures(serveStyleProbs, serveInProb, serveQuality):
    f = open('data/allmatches.csv')
    reader = csv.reader(f)
    
    playerVectors = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    
    for player in serveStyleProbs:
        for surface in serveStyleProbs[player]:
            w = 0
            for hand in serveStyleProbs[player][surface]:
                playerVectors[player][surface]['wide'] += serveStyleProbs[player][surface][hand][0]
                playerVectors[player][surface]['body'] += serveStyleProbs[player][surface][hand][1]
                playerVectors[player][surface]['t'] += serveStyleProbs[player][surface][hand][2]
                w += 1
            for att in playerVectors[player][surface]:
                if att == 'wide' or att == 'body' or att == 't':
                    playerVectors[player][surface][att] /= float(w)
    
    for player in serveInProb:
        for surface in serveInProb[player]:
            w = 0
            for hand in serveInProb[player][surface]:
                for style in serveInProb[player][surface][hand]:
                    playerVectors[player][surface]['1st'] += serveInProb[player][surface][hand][style][0]
                    playerVectors[player][surface]['2nd'] += serveInProb[player][surface][hand][style][1]
                    playerVectors[player][surface]['df'] += serveInProb[player][surface][hand][style][2]
                    w += 1
            for att in playerVectors[player][surface]:
                if att == '1st' or att == '2nd' or att == 'df':
                    playerVectors[player][surface][att] /= float(w)
                
    for player in serveQuality:
        for surface in serveQuality[player]:
            w = 0
            for hand in serveQuality[player][surface]:
                for style in serveQuality[player][surface][hand]:
                    for quality in serveQuality[player][surface][hand][style]:
                        playerVectors[player][surface]['ace'] += serveQuality[player][surface][hand][style][quality][0]
                        playerVectors[player][surface]['forcedError'] += serveQuality[player][surface][hand][style][quality][1]
                        w += 1
            for att in playerVectors[player][surface]:
                if att == 'ace' or att == 'forcedError':
                    playerVectors[player][surface][att] /= float(w)

    matchVectors = defaultdict(list)    
        
    idx = 0
    for row in reader:
        
        if idx != 0:
            
            matchId = row[0].split('-')
            player1 = matchId[4]
            player2 = matchId[5]
            
            surface = row[11]
            surfaceEncoding = -1
            
            if surface == 'Hard':
                surfaceEncoding = 0
            elif surface == 'Clay':
                surfaceEncoding = 1
            elif surface == 'Grass':
                surfaceEncoding = 2
            elif surface == 'Indoor Hard':
                surfaceEncoding = 3
                
            if surfaceEncoding != -1:
                p1 = playerVectors[player1][surface]
                p2 = playerVectors[player2][surface]
                
                #wide, body, t, 1stin, 2ndin, DF, ace, forcedError
                wide = p1['wide'] - p2['wide']
                body = p1['body'] - p2['body']
                t = p1['t'] - p2['t']
                first = p1['1st'] - p2['1st']
                sec = p1['2nd'] - p2['2nd']
                df = p1['df'] - p2['df']
                ace = p1['ace'] - p1['ace']
                fced = p1['forcedError'] - p1['forcedError']
                
                matchVectors[row[0]].extend((surfaceEncoding, wide, body, t, first, sec, df, ace, fced))
                
        idx += 1
    matchVectors['20151030-M-Valencia-QF-Joao_Sousa-Pablo_Cuevas'] = matchVectors['20151030-M-Valencia-QF-Joao_Sousa-Pablo_Cuevas'][0:9]
    return matchVectors
    
def getStats(valid_matches):
    surfaces = getSurfaces(valid_matches)
    
    #wide,body,T
    serveStyleProbs = getServeStyleProbabilities(surfaces)
    #print serveStyleProbs['Bjorn_Borg']['Hard']['deuce']
    
    #1stin,2ndin,DF
    serveInProb = getServeInProbabilities(surfaces)
    #print serveInProb['Bjorn_Borg']['Hard']['deuce']['wide']
    
    #ace, forcedError, acestotal, forcederrortotals
    serveQuality = getServeQualityProbabilities(surfaces)
    #print serveQuality['Bjorn_Borg']['Hard']['deuce']['wide']['1st']
    
    return serveStyleProbs, serveInProb, serveQuality

def getBaseline():
    serveStyleProbs, serveInProb, serveQuality = getStats()
    return getBaselineFeatures(serveStyleProbs, serveInProb, serveQuality)
    
if __name__ == "__main__":
    surfaces = getSurfaces()
    
    #wide,body,T
    serveStyleProbs = getServeStyleProbabilities(surfaces)
    #print serveStyleProbs['Bjorn_Borg']['Hard']['deuce']
    print serveStyleProbs['juan martin del potro']
    
    #1stin,2ndin,DF
    serveInProb = getServeInProbabilities(surfaces)
    #print serveInProb['Bjorn_Borg']['Hard']['deuce']['wide']
    
    #ace, forcedError, acestotal, forcederrortotals
    serveQuality = getServeQualityProbabilities(surfaces)
    #print serveQuality['Bjorn_Borg']['Hard']['deuce']['wide']['1st']
    
    #matchId: [surfaceEncoding, wide, body, t, 1stin, 2ndin, DF, ace, forcedError]
    baselines = getBaselineFeatures(serveStyleProbs, serveInProb, serveQuality)
    #print baselines['19751219-M-Davis_Cup_World_Group_F-RR-Bjorn_Borg-Jiri_Hrebec']
    
    b = getBaseline()
    #print b['20100126-M-Australian_Open-QF-Novak_Djokovic-Jo_Wilfried_Tsonga']
    ctr = 0
    for matchid in b:
        ctr += 1
    print ctr
