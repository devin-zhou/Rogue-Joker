import os
import random
import sys
import time
import copy

from pick import pick

import data
import deck_functions
import text_ui


DEBUG_MODE = 0

FAST_MODE = True
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
        self.handSize = 8
        self.totalHands = 4
        self.totalDiscards = 3
        self.currentLevel = 0
        self.requiredScores = [5000, 10000, 20000, 50000]

    def getChipMultTable(self):
        self.chipMultTable = data.chipMultTable

    def chooseDeck(self, allDecks):
        self.selectedDeck = deckSelection(allDecks)

    def getCurrentScoreRequired(self):
        return self.requiredScores[self.currentLevel]

class JokerState:
    def __init__(self, playerJokers):
        self.playerJokers = playerJokers
        self.fourFingers = 5

    def initJokerPool(self):
        self.commonJokers = data.commonJokers
        self.uncommonJokers = data.uncommonJokers
        self.rareJokers = data.rareJokers

    def updateFourFingers(self):
        if "Four Fingers" in self.playerJokers:
            self.fourFingers = 4

class RoundState:
    def __init__(self, currentHands, currentDiscards, hasHand):
        self.currentHands = currentHands
        self.currentDiscards = currentDiscards
        self.hasHand = hasHand
        self.resetValues()
    
    def resetValues(self):
        self.chip = 0
        self.mult = 0
        self.XMult = 1
        self.score = 0

def generateHand(handSize, baseCards) -> tuple:
    deck = copy.deepcopy(baseCards)
    random.shuffle(deck)
    return deck[0:handSize], deck[handSize:]


def drawCards(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return deck_functions.orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]


def findFlush(hand: list, flushSize=5) -> tuple:
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0, "X": 0}

    for card in hand:
        suitCount[card[-1]] += 1

    numWildCards = suitCount["X"]
    flushFlag = False
    indicesMax = []
    indices = []

    for suit, count in suitCount.items():
        if count + numWildCards >= flushSize and suit != "X":
            flushFlag = True
            indices = [i for i, card in enumerate(hand) if card[-1] == suit or card[-1] == "X"]

            indicesMax = indices if not indicesMax else indicesMax

            if 4 in indices:
                indicesMax = indices

    if DEBUG_MODE:
        print("\nfindFlush Check")
        print("hand", hand, "flush size:", flushSize)
        print(suitCount)

    return flushFlag, indices


def findStraight(hand: list, straightSize=5) -> tuple:
    orderedHand = removeSuits(hand)  # Already sorted by rank

    # Ace Case
    # Might not work with Four Fingers
    if 1 in orderedHand and 13 in orderedHand:
        orderedHand.remove(1)
        orderedHand.append(14)

    if DEBUG_MODE:
        print("\nfindStraight Check")
        print("sorted hand", orderedHand)
        print("sums", sum(orderedHand), orderedHand[0] * 5 + 10)
        print("first card == last card minus 4:", orderedHand[0], orderedHand[-1] - 4)

    # Sliding window check
    for i in range(len(orderedHand) - straightSize + 1):
        window = orderedHand[i : i + straightSize]

        if all(window[j] + 1 == window[j + 1] for j in range(straightSize - 1)):
            return True, list(range(i, i + straightSize))
    return False, None


def findFiveOfAKind(hand: list) -> bool:
    orderedHand = removeSuits(hand)
    if DEBUG_MODE:
        print("\nfindFiveOfAKind Check")
        print("hand", orderedHand, len(orderedHand))
        print(all(orderedHand[0] == a for a in orderedHand))
    return all(orderedHand[0] == a for a in orderedHand) and len(orderedHand) == 5


def findFourOfAKind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)

    if DEBUG_MODE:
        print("\nfindFourOfAKind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 4 and orderedHand[0] == orderedHand[3]:
        return True, [0, 1, 2, 3]
    if len(orderedHand) == 5 and orderedHand[1] == orderedHand[4]:
        return True, [1, 2, 3, 4]
    return False, None


# Returns FIRST 3oak found
def findThreeOfAKind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)
    lengthHand = len(orderedHand)

    if DEBUG_MODE:
        print("\nfindThreeOfAKind Check")
        print("hand", orderedHand, lengthHand)

    for i in range(len(orderedHand) - 2):
        if orderedHand[i] == orderedHand[i + 1] == orderedHand[i + 2]:
            return True, [i, i + 1, i + 2]
    return False, None


# Returns FIRST pair found
def findPair(hand: list) -> tuple:
    orderedHand = removeSuits(hand)
    lengthHand = len(orderedHand)

    if DEBUG_MODE:
        print("\nfindPair Check")
        print("hand", orderedHand, lengthHand)

    for i in range(lengthHand - 1):
        if orderedHand[i] == orderedHand[i + 1]:
            return True, [i, i + 1]

    return False, None


def findTwoPair(hand: list) -> tuple:
    if len(hand) < 4:
        return False, None

    hasSecondPair, pairIndex2 = None, None

    hasFirstPair, pairIndex = findPair(hand)

    if hasFirstPair:
        hand[pairIndex[0]] = "100"
        hand[pairIndex[1]] = "200"
        hasSecondPair, pairIndex2 = findPair(hand)

    if DEBUG_MODE:
        print("\nfindTwoPair Check")
        print("hand", hand, len(hand))
        print(hasFirstPair, pairIndex)
        print(hasSecondPair, pairIndex2)

    if hasFirstPair and hasSecondPair:
        return True, pairIndex + pairIndex2
    return False, None


def findFullHouse(hand: list) -> tuple:
    if len(hand) < 5:
        return False, None

    hasPair, pairIndex = None, None

    hasThree, threeIndex = findThreeOfAKind(hand)

    if hasThree:
        hand[threeIndex[0]] = "100"
        hand[threeIndex[1]] = "200"
        hand[threeIndex[2]] = "300"
        hasPair, pairIndex = findPair(hand)

    if DEBUG_MODE:
        print("\nfindFullHouse Check")
        print("hand", hand, len(hand))
        print(hasPair, pairIndex)

    if hasThree and hasPair:
        return True, pairIndex + threeIndex
    return False, None


def removeSuits(hand):
    hand = [
        int(card[:-1]) for card in hand
    ]  # Removes the suit character at the end of each index
    return hand


# Finds the index of the input hand name from the hasHand dict
def handNameToIndex(handName, hasHand) -> int:
    return next((i for i, key in enumerate(hasHand) if key == handName), None)

# Find first true value in the dict (highest scoring hand type present in hand)
def findHighestHandName(foundHands):
    for key, value in foundHands.items():
        if value:
            return key
    return "hasHighHand"

def getRandomIndices(deck, k) -> list:
    return random.sample(range(len(deck)), k)

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


def mainLoopPlay(roundState1, jokerState1, gameState1, selectedIndicesSet, hand, discardPile):
    roundState1.currentHands -= 1
    playedHand = [card for i, card in enumerate(hand) if i in selectedIndicesSet]
    # SORTS the inputted hand before evaluating
    playedHand = deck_functions.orderRank(playedHand)
    print("You played:", playedHand)
    # notHighCard lets us know if it's a multi card hand thats being scored
    notHighCard, partialHandIndices, roundState1.hasHand = evalHand(playedHand, roundState1.hasHand, jokerState1.fourFingers)

    chip, mult, XMult, scoredCards = scoreHand(playedHand, partialHandIndices, notHighCard, jokerState1.fourFingers, gameState1.chipMultTable, roundState1.hasHand)
    text_ui.printEquation(chip, mult)

    chip, mult, XMult = endJokerCalculation(
        chip, mult, XMult, jokerState1.playerJokers, scoredCards, roundState1
    )
    XMult = XMult if XMult == 1 else XMult - 1

    text_ui.endOfCalcPrint(chip, mult, XMult)
    score += chip * (mult * XMult)
    text_ui.slowPrint("Total level Score", None, speeds[2])
    time.sleep(speeds[3])
    
    if score > gameState1.getcurrentScoreRequired():
        text_ui.rainbowText(score)
    else:
        text_ui.slowPrint(score, None, speeds[2])
    print()
    print()

    # Resets playedHand
    keptCards = [card for card in hand if card not in playedHand]
    hand, deck = drawCards(keptCards, deck, gameState1.handSize)
    discardPile.append(playedHand)
    
    return hand, deck, score, discardPile


# Checks for multi-card hand types and stores the found hands in a dict
# Returns tuple (True/False if its highcard, list of lists with the indices of scored cards from partial hand types)
def evalHand(hand: list, foundHands, fourFingers) -> tuple:
    # Stored hands types are low to high
    partialHandIndices = [None] * 12

    # Whole Hands
    foundHands["hasFlush"], partialHandIndices[5] = findFlush(hand, fourFingers)
    foundHands["hasStraight"], partialHandIndices[4] = findStraight(hand, fourFingers)
    foundHands["hasFiveOfAKind"] = findFiveOfAKind(hand)

    # Partial Hands
    foundHands["hasFourOfAKind"], partialHandIndices[7] = findFourOfAKind(hand)
    foundHands["hasThreeOfAKind"], partialHandIndices[3] = findThreeOfAKind(hand)
    if foundHands["hasThreeOfAKind"]:
        foundHands["hasFullHouse"], partialHandIndices[6] = findFullHouse(hand)
    foundHands["hasPair"], partialHandIndices[1] = findPair(hand)
    if foundHands["hasPair"]:
        foundHands["hasTwoPair"], partialHandIndices[2] = findTwoPair(hand)

    # Combo Whole Hands
    foundHands["hasFlushFive"] = foundHands["hasFlush"] and foundHands["hasFiveOfAKind"]
    foundHands["hasFlushHouse"] = foundHands["hasFlush"] and foundHands["hasFullHouse"]
    foundHands["hasStraightFlush"] = foundHands["hasFlush"] and foundHands["hasStraight"]


    foundMultiCardHand = any(foundHands.values())

    if not foundMultiCardHand:  # High Card
        partialHandIndices[0] = highCardFinder(hand, True)

    # Returns True if any Poker Hands are found, returns False for High Card,
    # a DICT with all the found hand types as keys with True/False as values
    # and a LIST containting the indices of the SCORED cards for partial hand types (high card, pair, etc)
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


def scoreHand(hand, partialHandIndices, notHighCard, fourFingers: int, chipMultTable, hasHand) -> tuple:
    newPartialHand, highestHandName = None, None

    if notHighCard:
        highestHandName = findHighestHandName(hasHand)
        text_ui.magPrint(highestHandName[3:].upper())
    else:  # high card
        highestHandName = "hasHighHand"
        text_ui.magPrint("High Card")

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

    hand = hand if newPartialHand is None else newPartialHand

    # If highestHandName is None, set highestHandIndex to zero (high hand), else
    highestHandIndex = (
        11 if highestHandName == "hasHighHand" else handNameToIndex(highestHandName, hasHand)
    )
    tempChips = countChips(hand)
    chip, mult = calculateChipMult(tempChips, highestHandIndex, chipMultTable)
    XMult = 1
    return chip, mult, XMult, hand


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

    text_ui.printJokers(jokerState.playerJokers)


def jokerShop(jokerState) -> list:
    #allJokers = commonJokers | uncommonJokers | rareJokers
    currentJokerShop = []

    for i in range(8):
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



def endJokerCalculation(chip, mult, XMult, playerJokers, scoredCards, roundState1) -> tuple:
    # to do todo: remove this testing block
    #allJokers = commonJokers | uncommonJokers | rareJokers
    #for i, v in enumerate(allJokers):  # Gives player every joker
        #playerJokers.append(v)

    #playerJokers = ["Stuntman", "Cavendish"]  # to do todo: remove
    
    hasHand = roundState1.hasHand

    noSuitHand = removeSuits(scoredCards)
    time.sleep(speeds[3])
    time.sleep(speeds[3])
    for jokers in playerJokers:
        match jokers[0]:
            case "Classic Joker":
                mult += 4
                text_ui.slowPrint("Joker: +4", "mult")
            case "Misprint":
                misprintMult = random.randint(0, 24)
                mult += misprintMult
                text_ui.slowPrint("Misprint: +" + str(misprintMult), "mult")
            case "Cavendish":
                XMult += 3
                text_ui.slowPrint("Cavendish: X3", "XMult")
                if random.randrange(0, 999) == 67:
                    print("Cavendish: 1 in 1000. You lose.")
                    sys.exit(0)
            case "Stuntman":
                chip += 250
                text_ui.slowPrint("Stuntman: +250", "chip")
            case "Jolly Joker":
                if hasHand["hasPair"]:
                    text_ui.slowPrint("Jolly Joker: +8", "mult")
                    mult += 8
            case "Zany Joker":
                if hasHand["hasThreeOfAKind"]:
                    text_ui.slowPrint("Zany Joker: +12", "mult")
                    mult += 12
            case "Wily Joker":
                if hasHand["hasThreeOfAKind"]:
                    text_ui.slowPrint("Wily Joker: +100", "chip")
                    chip += 100
            case "Droll Joker":
                if hasHand["hasFlush"]:
                    text_ui.slowPrint("Droll Joker: +10", "mult")
                    mult += 10
            case "Mystic Summit":
                if roundState1.currentDiscards == 0:
                    text_ui.slowPrint("Mystic Summit: +15", "mult")
                    mult += 15
            case "Half Joker":
                if len(scoredCards) <= 3:
                    text_ui.slowPrint("Half Joker: +20", "mult")
                    mult += 20
            case "Gros Michel":
                mult += 15
                text_ui.slowPrint("Gros Michel: +15", "mult")
                if random.randrange(0, 10) == 5:
                    print("Gros Michel was destroyed.")
                    playerJokers.remove("Gros Michel")
            case "Even Steven":
                evenCount = 0
                for rank in noSuitHand:
                    if rank % 2 == 0 and rank not in {11, 12, 13}:
                        evenCount += 1

                mult += evenCount * 4
                text = "Even Steven: +" + str(evenCount) + " * 4"
                text_ui.slowPrint(text, "mult")
            case "Odd Todd":
                oddCount = 0
                for rank in noSuitHand:
                    if rank % 2 == 1 and rank not in {11, 12, 13}:
                        oddCount += 1

                chip += oddCount * 31
                text = "Odd Todd: +" + str(oddCount) + " * 31"
                text_ui.slowPrint(text, "chip")
            case "Scholar":
                for rank in noSuitHand:
                    if rank == 1:
                        mult += 4
                        chip += 20
            case other:
                if DEBUG_MODE:
                    print(other)

    return chip, mult, XMult


def clearConsole():
    # windows
    if os.name == "nt":
        _ = os.system("cls")
    # mac linux
    else:
        _ = os.system("clear")



def main(forcePlayerJokers = None):
    playerJokers = [] if forcePlayerJokers is None else forcePlayerJokers
    discardPile = []
    printMode = (0, 1, 2)

    gameState1 = GameState(baseCards = deck_functions.getBaseCards())
    gameState1.getChipMultTable()
    roundState1 = RoundState(currentHands = 4, currentDiscards = 3, hasHand = getHasHand())
    jokerState1 = JokerState(playerJokers)

    clearConsole()

    if not FAST_MODE:
        text_ui.printInstructions()

    # deck selection
    if not FAST_MODE:
        gameState1.chooseDeck(data.allDecks)
    else:
        gameState1.selectedDeck = "Red Deck"


    # apply new deck
    deck_functions.applyDeck(gameState1.selectedDeck, roundState1, jokerState1, gameState1)

    # Joker Selection from joker shop
    if not FAST_MODE:
        # insert deck dependency here
        #
        jokerState1.initJokerPool()
        jokerSelection(jokerState1)
    else:
        jokerState1.playerJokers = ["Four Fingers", "Burnt Joker"]

    # apply jokers that affect deck, hand
    for jokers in jokerState1.playerJokers:
        match jokers:
            case "Stuntman":
                gameState1.handSize -= 2
            case "Four Fingers":
                jokerState1.updateFourFingers()
            case _:
                pass

    # todo to do adjust and move to account for multiple levels
    handWithDeck = generateHand(gameState1.handSize, gameState1.baseCards)
    hand, deck = deck_functions.orderRank(handWithDeck[0]), handWithDeck[1]

    time.sleep(speeds[3])
    # Per game Loop
    while gameState1.currentLevel < len(gameState1.requiredScores):
        # Per level Loop
        currentRequiredScore = gameState1.getCurrentScoreRequired()
        while roundState1.score < currentRequiredScore:
            roundState1.resetValues()

            # Reset hasHand
            roundState1.hasHand = getHasHand()

            # Check for lose condition
            if roundState1.currentHands <= 0 and roundState1.score < currentRequiredScore:
                print(roundState1.score, "is less than ", currentRequiredScore, ".\nGame Over")
                sys.exit(0)

            text_ui.mainLoopPrompt(currentRequiredScore, roundState1.score, roundState1.currentHands, roundState1.currentDiscards, printMode)
            printMode = (2,) # The comma is needed to make it a tuple with one element, which is what mainLoopPrompt expects
            text_ui.printHand(hand)
            print("Deck Length:", len(deck))

            userInput = input()
            userInputAction = userInput[0].lower()
            userInputCardIndex = userInput[1:].strip()
            selectedIndicesSet = {int(x) for x in userInputCardIndex}

            # Limit hand / discard size
            if len(selectedIndicesSet) > 5:
                print("Error: selected too many cards")
                text_ui.mainLoopPrompt(currentRequiredScore, roundState1.score, roundState1.currentHands, roundState1.currentDiscards, (0,))
                continue

            # DISCARD
            if userInputAction == "d" and roundState1.currentDiscards > 0:
                roundState1.currentDiscards -= 1
                firstDiscard = gameState1.totalDiscards == roundState1.currentDiscards + 1
                # Removes cards from the hand based on indices
                keptCards, discarded = [], []
                for index, card in enumerate(hand):
                    if index not in selectedIndicesSet:
                        keptCards.append(card)
                    else:
                        discarded.append(card)

                if firstDiscard and "Trading Card" in jokerState1.playerJokers and len(discarded) == 1:
                    # Trading Card prevents the discarded card from entering the discardPile, thus removing it from the deck
                    pass
                else:
                    discardPile.append(discarded)

                if "Burnt Joker" in jokerState1.playerJokers and firstDiscard:
                    tempHasHand = getHasHand()
                    foundMultiCardHand, _, foundHands = evalHand(discarded, tempHasHand, jokerState1.fourFingers)

                    if foundMultiCardHand:
                        upgradeName = findHighestHandName(foundHands)
                        upgradeIndex = handNameToIndex(upgradeName, tempHasHand)
                    else:
                        upgradeName = "hasHighHand"
                        upgradeIndex = 11

                    for i, handType in enumerate(gameState1.chipMultTable):
                        if i == upgradeIndex:
                            handType[4] += 1
                            text_ui.slowPrint("Burnt Joker: " + upgradeName[3::] + " Level: "
                                              + str(handType[4] - 1) + " -> " + str(handType[4]))
                    print()

                # todo to do Handle new jokers that delete certain ranks

                hand = keptCards
                hand, deck = drawCards(hand, deck, gameState1.handSize)

            # PLAY
            elif userInputAction == "p":
                hand, deck, score, discardPile = mainLoopPlay(roundState1, jokerState1, gameState1, selectedIndicesSet, hand, discardPile)

            # Out of Discards
            elif userInputAction == "d" and roundState1.currentDiscards == 0:
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
                text_ui.printJokers(jokerState1.playerJokers)
                time.sleep(speeds[3])

            # VIEW DECK
            elif userInputAction == "v":
                # Temp variable to prevent changing deck order
                remainingDeckTemp = deck_functions.orderSuit(deck)
                text_ui.printDeck(gameState1.baseCards, remainingDeckTemp)
                time.sleep(speeds[3])

            else:
                clearConsole()
                print("Error: Try Again")
                time.sleep(speeds[1])

        # Beat the current level
        if roundState1.score > currentRequiredScore:
            print(roundState1.score, "is greater than", currentRequiredScore)
            # Reset variables for next level
            # todo to do: make function in gameState1 to increment and reset for next level
            gameState1.currentLevel += 1
            roundState1.score = 0
            roundState1.currentHands = gameState1.totalHands
            roundState1.currentDiscards = gameState1.totalDiscards
            # baseCards = discardPile + deck + remaining cards in hand #to do todo
            print("Press enter to continue")
            input()
            print("--- LEVEL", gameState1.currentLevel + 1, "---")  # +1 for 0 index
            time.sleep(speeds[3])

    print("--- You win ---")


if __name__ == "__main__":
    # Can force jokers from command line argument for testing, format should be a list of joker names (e.g. ["Stuntman", "Cavendish"])
    forcedJoker = sys.argv[1] if len(sys.argv) > 1 else None
    main(forcedJoker)
