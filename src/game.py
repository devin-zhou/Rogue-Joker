import os
import random
import sys
import time
import copy

from pick import pick

import data
import deck_functions as df
import hand_functions as hf
import helper_functions as helper
import joker_functions as jf
import text_ui as ui

DEBUG_MODE = 0

FAST_MODE = False
speeds = [0.01, 0.05, 0.075, 0.3]

if FAST_MODE:
    speeds = [0, 0, 0, 0]


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

    def chooseDeck(self, allDecks):
        self.selectedDeck = deckSelection(allDecks)

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
        foundFourFingers = helper.findJoker("Four Fingers", self.playerJokers)
        if foundFourFingers:
            self.fourFingers = 4

class RoundState:
    def __init__(self, currentHands, currentDiscards, hasHand):
        self.currentHands = currentHands
        self.currentDiscards = currentDiscards
        self.hasHand = hasHand
        self.score = None
        self.resetScoringValues()
        self.highestHandIndex = None

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
        self.hasHand = getHasHand()


def generateHand(handSize, baseCards) -> tuple:
    deck = copy.deepcopy(baseCards)
    random.shuffle(deck)
    return deck[0:handSize], deck[handSize:]


def drawCards(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return df.orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]

# Finds the index of the input hand name from the hasHand dict
def handNameToIndex(handName, hasHand) -> int:
    return next((i for i, key in enumerate(hasHand) if key == handName), None)

# Find first true value in the dict (highest scoring hand type present in hand)
def findHighestHandName(foundHands):
    for key, value in foundHands.items():
        if value:
            return key
    return "hasHighHand"

def getHasHand():
    return {
        "hasFlushFive": False,
        "hasFlushHouse": False,
        "hasFiveOfAKind": False,
        "hasStraightFlush": False,
        "hasFourOfAKind": False,
        "hasFullHouse": False,
        "hasFlush": False,
        "hasStraight": False,
        "hasThreeOfAKind": False,
        "hasTwoPair": False,
        "hasPair": False
    }


def mainLoopPlay(rs1, js1, gs1, selectedIndicesSet, hand, deck, discardPile):
    rs1.currentHands -= 1
    playedHand = [card for i, card in enumerate(hand) if i in selectedIndicesSet]
    # SORTS the inputted hand before evaluating
    playedHand = df.orderRank(playedHand)
    print("You played:", playedHand)
    # notHighCard lets us know if it's a multi card hand thats being scored
    notHighCard, partialHandIndices, rs1.hasHand = evalHand(playedHand, rs1.hasHand, js1.fourFingers)

    chip, mult, XMult, scoredCards = scoreHand(playedHand,partialHandIndices,notHighCard,js1.fourFingers,gs1.chipMultTable,rs1)
    time.sleep(speeds[3])
    ui.printEquation(chip, mult)
    time.sleep(speeds[3])
    print("Scored cards:", scoredCards)

    chip, mult, XMult = jf.jokerCalculation(chip, mult, XMult, js1.playerJokers, scoredCards, rs1, gs1)
    XMult = XMult if XMult == 1 else XMult - 1

    ui.endOfCalcPrint(chip, mult, XMult)

    rs1.score += chip * (mult * XMult)
    ui.slowPrint("Total level Score", None, speeds[2])
    time.sleep(speeds[3])

    if rs1.score > gs1.getCurrentScoreRequired():
        ui.rainbowText(rs1.score)
    else:
        ui.slowPrint(rs1.score, None, speeds[2])
    print()
    print()

    # Resets playedHand
    keptCards = [card for card in hand if card not in playedHand]
    hand, deck = drawCards(keptCards, deck, gs1.totalValues[0])
    discardPile = discardPile + playedHand

    return hand, deck, discardPile


# Checks for multi-card hand types and stores the found hands in a dict
# Returns tuple (True/False if its highcard, list of lists with the indices of scored cards from partial hand types)
def evalHand(hand: list, foundHands: dict, fourFingers: int) -> tuple:
    # Stored hands types are low to high
    partialHandIndices = [None] * 12

    # Whole Hands
    foundHands["hasFlush"], partialHandIndices[5] = hf.findFlush(hand, fourFingers)
    foundHands["hasStraight"], partialHandIndices[4] = hf.findStraight(hand, fourFingers)
    foundHands["hasFiveOfAKind"] = hf.findFiveOfAKind(hand)

    # Partial Hands
    foundHands["hasFourOfAKind"], partialHandIndices[7] = hf.findFourOfAKind(hand)
    foundHands["hasThreeOfAKind"], partialHandIndices[3] = hf.findThreeOfAKind(hand)
    if foundHands["hasThreeOfAKind"]:
        foundHands["hasFullHouse"], partialHandIndices[6] = hf.findFullHouse(hand)
    foundHands["hasPair"], partialHandIndices[1] = hf.findPair(hand)
    if foundHands["hasPair"]:
        foundHands["hasTwoPair"], partialHandIndices[2] = hf.findTwoPair(hand)

    # Combo Whole Hands
    foundHands["hasFlushFive"] = foundHands["hasFlush"] and foundHands["hasFiveOfAKind"]
    foundHands["hasFlushHouse"] = foundHands["hasFlush"] and foundHands["hasFullHouse"]

    if foundHands["hasFlush"] and foundHands["hasStraight"]:
        foundHands["hasStraightFlush"] = True
        partialHandIndices[8] = set(partialHandIndices[5]) | set(partialHandIndices[4])

    foundMultiCardHand = any(foundHands.values())

    if not foundMultiCardHand:  # High Card
        partialHandIndices[0] = highCardFinder(hand, True)

    # Returns True if any Poker Hands are found, returns False for High Card,
    # a DICT with all the found hand types as keys with True/False as values
    # and a LIST containing the indices of the SCORED cards for partial hand types (high card, pair, etc)
    return foundMultiCardHand, partialHandIndices, foundHands

# Returns the index of the high card in the hand
def highCardFinder(hand: list, findIndex: bool):
    if findIndex:
        if hand[0][0] == "1":
            hand = [0]
        else:
            hand = [len(hand) - 1]
    else:
        if hand[0][0] == "1":
            hand = [hand[0]]
        else:
            hand = [hand[-1]]
    return hand


def scoreHand(hand, partialHandIndices, notHighCard, fourFingers, chipMultTable, rs1) -> tuple:
    newPartialHand, highestHandName = None, None
    hasHand = rs1.hasHand
    if notHighCard:
        highestHandName = findHighestHandName(hasHand)
        ui.magPrint(highestHandName[3:].upper())
    else:  # high card
        highestHandName = "hasHighHand"
        ui.magPrint("High Card")

    # Check if the hand we're scoring is a partial hand or not
    partialHands = {
        "hasFourOfAKind": 7,
        "hasThreeOfAKind": 3,
        "hasTwoPair": 2,
        "hasPair": 1,
        "hasHighHand": 0,
    }
    if fourFingers == 4:
        partialHands["hasFlush"] = 5
        partialHands["hasStraight"] = 4

    if highestHandName in partialHands:
        # Feed the correct partialHandIndices index and score the respective hand indices
        indices = partialHandIndices[partialHands[highestHandName]]
        newPartialHand = [card for i, card in enumerate(hand) if i in indices]

    filteredHand = hand if newPartialHand is None else newPartialHand

    # If highestHandName is None, set highestHandIndex to zero (high hand), else
    highestHandIndex = (
        11 if highestHandName == "hasHighHand" else handNameToIndex(highestHandName, hasHand)
    )
    tempChips = countChips(filteredHand)
    chip, mult = calculateChipMult(tempChips, highestHandIndex, chipMultTable)
    XMult = 1
    rs1.highestHandIndex = highestHandIndex
    return chip, mult, XMult, filteredHand


# Counts chips given by cards from the played hand
def countChips(hand):
    total = 0
    for card in hand:
        rank = int(card[:-1])
        match rank:
            case 1:
                chips = 11
            case 11 | 12 | 13:
                chips = 10
            case _:
                chips = rank
        total += chips
    return total



def calculateChipMult(cardChips, handIndex, chipMultTable) -> tuple:
    baseChip, chipScaling = chipMultTable[handIndex][0], chipMultTable[handIndex][2]
    baseMult, multScaling = chipMultTable[handIndex][1], chipMultTable[handIndex][3]
    handLvl = chipMultTable[handIndex][4] - 1

    calculatedChip = cardChips + baseChip + (chipScaling * handLvl)
    calculatedMult = baseMult + (multScaling * handLvl)
    return calculatedChip, calculatedMult



def jokerSelection(jokerState):
    currentJokerShop = jokerShop(jokerState)
    selected = []
    # tuple of strings with the joker name and description for the current joker shop
    options = tuple(map(lambda item: item[0] + " - " + item[1][0], currentJokerShop))

    while len(selected) != 3:
        title = "Select 3 jokers (press SPACE to select, ENTER to continue): "
        selected = pick(options, title, multiselect=True, min_selection_count=3)

    for i in selected:
        jokerState.playerJokers.append(currentJokerShop[i[1]])

    ui.printJokers(jokerState.playerJokers)


def jokerShop(jokerState) -> list:
    #allJokers = commonJokers | uncommonJokers | rareJokers
    currentJokerShop = []

    for i in range(8):
        #check for running out of jokers.
        if not (jokerState.commonJokers and jokerState.uncommonJokers and jokerState.rareJokers):
            jokerState.initJokerPool()
        rng = random.randrange(0, 100)
        if i < 3 or rng < 50:
            key, value = random.choice(list(jokerState.commonJokers.items()))
            del jokerState.commonJokers[key]
        elif rng > 85:
            key, value = random.choice(list(jokerState.rareJokers.items()))
            del jokerState.rareJokers[key]
        else:
            key, value = random.choice(list(jokerState.uncommonJokers.items()))
            del jokerState.uncommonJokers[key]
        currentJokerShop.append((key, value))

    return currentJokerShop


def deckSelection(allDecks) -> int:
    # Returns a tuple of strings with the deck name and description
    options = tuple(map(lambda item: item[0] + " - " + item[1], allDecks.items()))
    title = "Select a deck (ENTER to continue): "
    selected = pick(options, title)
    print("Selected Deck:", selected[0])
    return options[selected[1]].split(" - ")[0] # Returns the name of the deck without the description


def clearConsole():
    # windows
    if os.name == "nt":
        _ = os.system("cls")
    # mac linux
    else:
        _ = os.system("clear")



def main(playerJokers = None, setSeed = None):
    random.seed(setSeed)

    # prevent dangerous-default-value
    if playerJokers is None:
        playerJokers = []

    discardPile = []
    printMode = (0, 1, 2)
    hand, deck = None, None

    gs1 = GameState(baseCards = df.getBaseCards())
    gs1.getChipMultTable()
    rs1 = RoundState(currentHands = gs1.totalValues[1], currentDiscards = gs1.totalValues[2], hasHand = getHasHand())
    js1 = JokerState(playerJokers)

    clearConsole()

    # deck selection
    if not FAST_MODE:
        ui.printInstructions()
        gs1.chooseDeck(data.allDecks)
    else:
        gs1.selectedDeck = "Checkered Deck"

    # apply new deck
    df.applyDeck(gs1.selectedDeck, js1, gs1)

    # Joker Selection from joker shop
    js1.initJokerPool()
    if not FAST_MODE:
        # insert deck dependency here
        #
        jokerSelection(js1)
    else:
        js1.playerJokers = [["Classic Joker","a"], ["Four Fingers","a"], ["Burnt Joker","a"],
                            ["Lusty Joker","a"],["Bloodstone","a"], ["Trading Card","a"],
                            ["Brainstorm","a"], ["Space Joker","a"]]

    time.sleep(speeds[3])

    # Per game Loop
    while gs1.currentLevel < len(gs1.requiredScores):
        gs1.setDefaultTotals(gs1.selectedDeck)  # Set the default totals based on the selected deck
        # apply jokers that affect deck, hand
        for jokers in js1.playerJokers:
            match jokers[0]:
                case "Stuntman":
                    gs1.totalValues[0] -= 2
                case "Four Fingers":
                    js1.updateFourFingers()
                case "Troubadour":
                    gs1.totalValues[0] += 2
                    gs1.totalValues[1] -= 1
                case "Merry Andy":
                    gs1.totalValues[2] += 3
                    gs1.totalValues[0] -= 1
                case _:
                    pass
        gs1.overflowTotals()
        # Assigns currentHands and currentDiscards to the game state's total hands, total discards
        rs1.resetRound(gs1.totalValues[1], gs1.totalValues[2])

        # to do todo put deck and hand into a state object

        if discardPile : # Check if not first loop of game, mix discard pile with remaining deck and hand
            gs1.baseCards = deck + discardPile + hand
        handWithDeck = generateHand(gs1.totalValues[0], gs1.baseCards)
        hand, deck = df.orderRank(handWithDeck[0]), handWithDeck[1]

        # Per level Loop
        currentRequiredScore = gs1.getCurrentScoreRequired()
        print("--- LEVEL", gs1.currentLevel + 1, "---")  # +1 for 0 index
        print("Score Required:", currentRequiredScore)
        while rs1.score < currentRequiredScore:
            # Check for lose condition (out of hands)
            if rs1.currentHands <= 0 and rs1.score < currentRequiredScore:
                print(rs1.score, "is less than", currentRequiredScore, "\nGame Over")
                sys.exit(0)

            # Reset round values
            rs1.resetScoringValues(True)
            # Reset hasHand
            rs1.hasHand = getHasHand()


            ui.mainLoopPrompt(currentRequiredScore, rs1, printMode)
            printMode = (2,) # The comma is needed to make it a tuple with one element, which is what mainLoopPrompt expects
            ui.printHand(hand)
            print("Deck Length:", len(deck))

            userInput = input()
            userInputAction = userInput[0].lower()
            userInputCardIndex = userInput[1:].strip()
            selectedIndicesSet = {int(x) for x in userInputCardIndex}

            # Limit hand / discard size
            if len(selectedIndicesSet) > 5:
                print("Error: selected too many cards")
                ui.mainLoopPrompt(currentRequiredScore, rs1, (0,))
                continue

            # DISCARD
            if userInputAction == "d" and rs1.currentDiscards > 0:
                rs1.currentDiscards -= 1 # Used up a discard

                # Removes cards from the hand based on indices
                keptCards, discarded = [], []
                for index, card in enumerate(hand):
                    if index not in selectedIndicesSet:
                        keptCards.append(card)
                    else:
                        discarded.append(card)

                # Trading Card
                firstDiscard = gs1.totalValues[2] == rs1.currentDiscards + 1
                foundTradingCard = helper.findJoker("Trading Card", js1.playerJokers)
                if firstDiscard and foundTradingCard and len(discarded) == 1:
                    # Trading Card prevents the discarded card from entering the discardPile, thus removing it from the deck
                    ui.slowPrint("Trading Card: " + str(discarded[0]) + " removed from deck")
                    print()
                else:
                    discardPile = discardPile + discarded

                # Burnt Joker
                foundBurntJoker = helper.findJoker("Burnt Joker", js1.playerJokers)
                if foundBurntJoker and firstDiscard:
                    tempHasHand = getHasHand()
                    foundMultiCardHand, _, foundHands = evalHand(discarded, tempHasHand, js1.fourFingers)

                    if foundMultiCardHand:
                        upgradeName = findHighestHandName(foundHands)
                        upgradeIndex = handNameToIndex(upgradeName, tempHasHand)
                    else:
                        upgradeName = "hasHighHand"
                        upgradeIndex = 11

                    newLvl = gs1.increaseHandLevel(upgradeIndex)
                    ui.slowPrint("Burnt Joker: " + upgradeName[3::] + " level increased from "
                                 + str(newLvl - 1) + " -> " + str(newLvl))
                    print()

                hand = keptCards
                hand, deck = drawCards(hand, deck, gs1.totalValues[0])

            # PLAY
            elif userInputAction == "p":
                hand, deck, discardPile = mainLoopPlay(rs1, js1, gs1, selectedIndicesSet, hand, deck, discardPile)

            # Out of Discards
            elif userInputAction == "d" and rs1.currentDiscards == 0:
                print("Error: Out of Discards. Try Again")
                time.sleep(speeds[3])
                continue

            # HELP
            elif userInputAction == "?":
                print('"q" to quit\n"c" to clear text\n"j" to view jokers\n"v" to view deck')
                time.sleep(speeds[3])

            # QUIT
            elif userInputAction == "q":
                sys.exit(0)

            # CLEAR
            elif userInputAction == "c":
                clearConsole()

            # SHOW JOKERS
            elif userInputAction == "j":
                ui.printJokers(js1.playerJokers)
                time.sleep(speeds[3])
                
            # SHOW chip mult table
            elif userInputAction == "t":
                print(gs1.chipMultTable)
                time.sleep(speeds[3])

            # VIEW DECK
            elif userInputAction == "v":
                # Temp variable to prevent changing deck order
                remainingDeckTemp = df.orderSuit(deck)
                ui.printDeck(gs1.baseCards, remainingDeckTemp)
                time.sleep(speeds[3])

            else:
                clearConsole()
                print("Error: Try Again")
                time.sleep(speeds[1])

        # Beat the current level
        if rs1.score > currentRequiredScore:
            print(rs1.score, "is greater than", currentRequiredScore)
            # Reset variables for next level
            gs1.currentLevel += 1
            rs1.resetRound(gs1.totalValues[1], gs1.totalValues[2]) #todo to do might not need this
            print("Press enter to continue")
            input()
            time.sleep(speeds[3])
            if gs1.currentLevel != len(gs1.requiredScores):
                jokerSelection(js1)
                foundFourFingers = helper.findJoker("Four Fingers", js1.playerJokers)
                if foundFourFingers:
                    js1.updateFourFingers()

    print("--- You win ---")


if __name__ == "__main__":
    # Can force jokers from command line argument for testing, format should be a list of joker names (e.g. ["Stuntman", "Cavendish"])
    forcedJoker = sys.argv[1] if len(sys.argv) > 1 else None
    forcedSeed = sys.argv[2] if len(sys.argv) > 2 else None
    main(forcedJoker, forcedSeed)
