import random
import Game

# randomly return 'h' or 's' regardless of the info given
class RandomAgent:
    def getAction(self, hand, dealerCard):
        rand = random.random()
        if rand < 0.5:
            return 'h'
        else:
            return 's'

# a simple reflec agent that returns action based on the configured heuristic
class HeuristicBasedAgent:
    def totalAceAs11(self, hand):
        total = 0
        sortedHand = hand
        sortedHand.sort()
        for card in sortedHand:
            if card == 11 or card == 12 or card == 13:
                card = 10
            if card == 14:
                card = 11
            total += card
        return total
    def getTotal(self, hand):
        total = 0
        sortedHand = hand
        sortedHand.sort()
        for card in sortedHand:
            if card == 11 or card == 12 or card == 13:
                card = 10
            if card == 14 and total >= 11:
                card = 1
            if card == 14 and total < 11:
                card = 11
            total += card
        return total

    def isSoftHand(self, hand):
        return 14 in hand and self.totalAceAs11(hand) <= 21

    def getAction(self, hand, dealerCard):
        #hard:
        sum = self.getTotal(hand)
        print('sum is ', sum)
        if not self.isSoftHand(hand):
            if sum <= 11:
                return 'h'
            elif sum == 12:
                if dealerCard == 4 or dealerCard == 5 or dealerCard == 6:
                    return 's'
                else:
                    return 'h'
            elif 13 <= sum and sum <= 16:
                if dealerCard >= 7:
                    return 'h'
                else:
                    return 's'
            else:
                return 's'
        else:
            if sum <= 17:
                return 'h'
            elif sum == 18:
                if dealerCard == 9 or dealerCard == 10:
                    return 'h'
                else:
                    return 's'
            else:
                return 's'
        #if hand <= 11 return h
        #if hand 12
        #if hand 13-16
        #if hand >= 17 return s
        #soft:
        #if hand <= 17 return h
        #if hand = 18
        #if hand >=19 return s 

# a Monte Carlo Tree Search agent that simulates from the given game state to 
# return the action with the highest win rate among the simulations
class MCTSAgent:
    # policy is either h for heuristic based simulation or r for random simulation
    def __init__(self, policy):
        self.winLossCount = {}
        self.policy = policy
        self.winLossCount[(1, 's')] = 0  # the cases that we stop and win
        self.winLossCount[(-1, 's')] = 0  # the cases that we stop and lose
        self.winLossCount[(0, 's')] = 0  # the cases that we stop and draw
        self.winLossCount[(1, 'h')] = 0  # the cases that we hit and win
        self.winLossCount[(-1, 'h')] = 0  # the cases that we hit and lose
        self.winLossCount[(0, 'h')] = 0  # the cases that we hit and draw

    # simulate blackjack games for a given number of iterations, starting from the game state with the 
    # given hand and the showing dealer card
    def simPlayBlackjack(self, numOfGames, hand, dealerCard):
        for i in range(numOfGames):
            game = Game.BlackJackGame()
            gameResult = game.simulateGame(hand, dealerCard, self.policy)
            if not gameResult in self.winLossCount.keys():
                self.winLossCount[gameResult] = 0
            self.winLossCount[gameResult] += 1

    # compare the win rate between the two actions among the simulations
    def getAction(self, hand, dealerCard):
        self.simPlayBlackjack(15000, hand, dealerCard)
        if (self.winLossCount[(1, 's')] + self.winLossCount[(-1, 's')]) == 0:
            chooseStopWinRate = 0
        else:
            chooseStopWinRate = self.winLossCount[(1, 's')] / (self.winLossCount[(1, 's')] + self.winLossCount[(-1, 's')])
        
        if (self.winLossCount[(1, 'h')] + self.winLossCount[(-1, 'h')]) == 0:
            chooseHitWinRate = 0
        else:
            chooseHitWinRate = self.winLossCount[(1, 'h')] / (self.winLossCount[(1, 'h')] + self.winLossCount[(-1, 'h')])
        if chooseStopWinRate > chooseHitWinRate:
            return 's'
        else:
            return 'h'
