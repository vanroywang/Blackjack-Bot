# this is a game of blackjack

from os import error
import random
import Agent 

class BlackJackGame: #the game state of the blackjack game
    #initialize the game with a full deck and empty hands
    def __init__(self):
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]*4
        self.playerHand = []#hands are list of numbers where 11 is equivalent to J, and so on. 14 is equivalent to A
        self.dealerHand = []

    # Randomly deal a card to the player's hand
    def hitPlayerHand(self):
        random.shuffle(self.deck)
        card = self.deck.pop()
        self.playerHand.append(card)

    # Randomly deal a card to the deaker's hand
    def hitDealerHand(self):
        random.shuffle(self.deck)
        card = self.deck.pop()
        self.dealerHand.append(card)
    
    # reset the game
    def resetGame(self):
        self.__init__()

    # move a specific card from deck to the player's hand
    def moveCardToPlayerHand(self, card):
        self.deck.remove(card)
        self.playerHand.append(card)

    # move a specific card from deck to the dealer's hand
    def moveCardToDealerHand(self, card):
        self.deck.remove(card)
        self.dealerHand.append(card)

    # return the total of player hand
    def getPlayerTotal(self):
        total = 0
        self.playerHand.sort()
        for card in self.playerHand:
            if card == 11 or card == 12 or card == 13:
                card = 10
            if card == 14 and total >= 11:
                card = 1
            if card == 14 and total < 11:
                card = 11
            total += card
        return total

    # return the total of dealer hand
    def getDealerTotal(self):
        total = 0
        self.dealerHand.sort()
        for card in self.dealerHand:
            if card == 11 or card == 12 or card == 13:
                card = 10
            if card == 14 and total >= 11:
                card = 1
            if card == 14 and total < 11:
                card = 11
            total += card
        return total

    # checks if player has 21 point
    def playerTwentyOne(self):
        return self.getPlayerTotal() == 21

    # checks if dealer has 21 point
    def dealerTwentyOne(self):
        return self.getDealerTotal() == 21
    
    # checks if the player is busted
    def playerBust(self):
        return self.getPlayerTotal() > 21

    # checks if the dealer is busted
    def dealerBust(self):
        return self.getDealerTotal() > 21

    # checks if the dealer is showing an Ace(dealer has a good hand)
    def dealerShowingAce(self):
        return self.dealerHand[0] == 14

    # calculates the sum of the player hand while counting all aces as 11
    # this method is used to determine whether the player hand is soft or hard
    def playerTotalAceAs11(self):
        total = 0
        self.playerHand.sort()
        for card in self.playerHand:
            if card == 11 or card == 12 or card == 13:
                card = 10
            if card == 14:
                card = 11
            total += card
        return total

    # checks if the player has a soft hand
    def playerSoftHand(self):#returns if the player has ace and using it as 14 now
        return 14 in self.playerHand and self.playerTotalAceAs11() <= 21

    # a script to simulate game play using the general heuristic
    def getHeuristicAction(self):
        sum = self.getPlayerTotal()
        dealerCard = self.dealerHand[0]
        if not self.playerSoftHand():
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

    # a script to simulate gameplay using randomness
    # chances are adjusted based on general heuristics
    def getRandomAction(self):
        #the chance of hitting should be lower when the player total is high
        rand = random.random()
        chanceToStop = 0
        dealerCard = self.dealerHand[0]
        if self.playerSoftHand():
            if self.getPlayerTotal() <= 15:
                chanceToStop = 0
            elif self.getPlayerTotal() == 16:
                chanceToStop = 0.05
            elif self.getPlayerTotal() == 17:
                chanceToStop = 0.1
            elif self.getPlayerTotal() == 18:
                chanceToStop = 0.80
            else:
                chanceToStop = 1
        else: #hard hand
            if self.getPlayerTotal() <= 11:
                chanceToStop = 0
            elif self.getPlayerTotal() == 12:
                if dealerCard == 4 or dealerCard == 5 or dealerCard == 6:
                    chanceToStop = 0.4
                else:
                    chanceToStop = 0
            elif self.getPlayerTotal() == 13:
                if dealerCard >= 7:
                    chanceToStop = 0.5
                else:
                    chanceToStop = 0

            elif self.getPlayerTotal() == 14:
                if dealerCard >= 7:
                    chanceToStop = 0.6
                else:
                    chanceToStop = 0.05
            
            elif self.getPlayerTotal() == 15:
                if dealerCard >= 7:
                    chanceToStop = 0.7
                else:
                    chanceToStop = 0.1
                if self.dealerShowingAce():
                    chanceToStop -= 0.1

            elif self.getPlayerTotal() == 16:
                if dealerCard >= 7:
                    chanceToStop = 0.85
                else:
                    chanceToStop = 0.2
                if self.dealerShowingAce():
                    chanceToStop -= 0.2

            elif self.getPlayerTotal() == 17:
                chanceToStop = 0.9
                if self.dealerShowingAce():
                    chanceToStop -= 0.4

            elif self.getPlayerTotal() == 18:
                chanceToStop = 0.95
                if self.dealerShowingAce():
                    chanceToStop -= 0.1

            else:
                chanceToStop = 1
        if rand < chanceToStop:
            return 's'
        else:
            return 'h'

    # compare the hands of the player and the dealer
    # return 0 if it is a draw, 1 if player win, -1 if player lose
    def compareHand(self):
        if self.getDealerTotal() == self.getPlayerTotal() :
            return 0
        elif self.getDealerTotal() < self.getPlayerTotal() :
            return 1
        elif self.getDealerTotal() > self.getPlayerTotal() :
            return -1

    # play a random game, and return (isWon, firstChoice),
    # isWon is 1 if win, -1 if lost, 0 if drawn; 
    def simulateGame(self, hand, dealerCard, policy):# we use this to gather information
        self.resetGame()
        for card in hand:
            self.moveCardToPlayerHand(card)
        self.moveCardToDealerHand(dealerCard)
        self.hitDealerHand()
        firstChoice = None
        ongoing = True
        while ongoing:
            if policy == 'h':
                choice = self.getHeuristicAction()
            elif policy == 'r':
                choice = self.getRandomAction()
            else:
                raise Exception("invalid simulation policy")
            if firstChoice == None:
                firstChoice = choice
            if choice == 'h':
                self.hitPlayerHand()
                if self.playerBust():
                    isWon = -1
                    ongoing = False
                    return (isWon, firstChoice)
            elif choice == 's':
                #need to add that dealer stops hitting when he has more than player
                while self.getDealerTotal() < 17: # the dealer is a simple reflex agent
                    self.hitDealerHand()
                    if self.getDealerTotal() > 21:
                        isWon = 1
                        ongoing = False
                        return (isWon, firstChoice)
                isWon = self.compareHand()
                ongoing = False
                return (isWon, firstChoice)

    # takes an agent and play a game. Whenever a decision needs to be made,
    # agent.getAction takes in the player hand and the showing dealer card,
    # and then return an action: 'h' for hit or 's' for stay
    def playGame(self, agent):
        self.resetGame()
        self.hitDealerHand()
        self.hitDealerHand()
        self.hitPlayerHand()
        self.hitPlayerHand()
        #print("player hand: ", self.playerHand)
        #print("dealer hand: ", self.dealerHand)
        while True:
            choice = agent.getAction(self.playerHand, self.dealerHand[0])
            if choice == 'h':
                self.hitPlayerHand()
                if self.playerBust():
                    #print("bust player hand: ", self.playerHand)
                    return -1
                #else:
                    #print("player drew a card")
                    #print("player hand: ", self.playerHand)
            elif choice == 's':
                #print("Player Stopped with total of ", self.getPlayerTotal())
                while self.getDealerTotal() < 17: # the dealer is a simple reflex agent
                    self.hitDealerHand()
                    if self.getDealerTotal() > 21:
                        #print("bust dealer hand: ", self.dealerHand)
                        return 1
                    #else:
                        #print("dealer drew a card")
                        #print("dealer hand: ", self.dealerHand)
                #print("Dealer Stopped with total of ", self.getDealerTotal())
                return self.compareHand()