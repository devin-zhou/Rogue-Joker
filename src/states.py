import data
import helper_functions as hp


class GameState:
    def __init__(self, baseCards):
        self.selectedDeck = None
        self.baseCards = baseCards
        self.currentLevel = 0
        self.requiredScores = [600, 1200, 5000, 12000, 25000, 75000, 200000]
        self.chipMultTable = None
        self.setDefaultTotals()

    def getChipMultTable(self):
        self.chipMultTable = data.chipMultTable

    def getCurrentScoreRequired(self):
        return self.requiredScores[self.currentLevel]

    def increaseHandLevel(self, handIndex):
        self.chipMultTable[handIndex][4] += 1
        return self.chipMultTable[handIndex][4]

    def setDefaultTotals(self, selectedDeck=None):
        # handSize, totalHands, totalDiscards
        if selectedDeck == "Red Deck":
            self.totalValues = [8, 4, 4]
        elif selectedDeck == "Blue Deck":
            self.totalValues = [8, 5, 3]
        else:
            self.totalValues = [8, 4, 3]


    def overflowTotals(self):
        if self.totalValues[0] >= 10:
            self.totalValues[2] += self.totalValues[0] - 9
            self.totalValues[0] = 9
            print("Hand size is greater than 9, discards increased by", self.totalValues[0] - 9)

        if self.totalValues[1] <= 0:
            self.totalValues[1] = 1
            self.totalValues[2] = 1
            print("Total hands is less than or equal to 0, setting to 1 and discards to 0")


class JokerState:
    def __init__(self, playerJokers):
        self.playerJokers = playerJokers
        self.fourFingers = 5
        self.commonJokers = None
        self.uncommonJokers = None
        self.rareJokers = None

    def initJokerPool(self):
        self.commonJokers = data.commonJokers.copy()
        self.uncommonJokers = data.uncommonJokers.copy()
        self.rareJokers = data.rareJokers.copy()

    def updateFourFingers(self):
        foundFourFingers = hp.findJoker("Four Fingers", self.playerJokers)
        if foundFourFingers:
            self.fourFingers = 4

class RoundState:
    def __init__(self, currentHands, currentDiscards, hasHand):
        self.currentHands = currentHands
        self.currentDiscards = currentDiscards
        self.hasHand = hasHand
        self.score = None
        self.resetScoringValues()

    def resetScoringValues(self, sameRound=False):
        self.chip = 0
        self.mult = 0
        self.XMult = 1
        if not sameRound:
            self.score = 0

    # next level
    def resetRound(self, hands, discards):
        self.resetScoringValues()
        self.currentHands = hands
        self.currentDiscards = discards
        self.hasHand = data.getHasHand()

    def getHighestHandIndex(self):
        index = hp.handNameToIndex(hp.findHighestHandName(self.hasHand), self.hasHand)
        if index is None:
            return 11
        return index



class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.mult = 0
        self.XMult = 1
        self.chip = self.chips()

    def chips(self):
        if self.rank == 1:
            return 11
        if self.rank in (11, 12, 13):
            return 10
        return self.rank

    def foil(self):
        self.chip += 50

    def holographic(self):
        self.mult += 10

    def polychrome(self):
        self.XMult += 0.5

    def __str__(self):
        return str(self.rank) + self.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    # Card Enhancements: Bonus, Mult, Wild, Glass, Steel, Stone, Gold, Lucky
    # Editions: Foil (+50 chips), Holographic (+10 Mult), Polychrome (X1.5 Mult), Negative
    # Seals: Gold Seal, Red Seal, Blue Seal, Purple Seal
