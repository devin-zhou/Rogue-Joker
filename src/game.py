import os
import random
import sys
import time
import copy

from pick import pick

import text_ui

chipMultTable = [
    [160, 16, 50, 3, 1],  # flush five
    [140, 14, 40, 4, 1],  # flush house
    [120, 12, 35, 3, 1],  # five of a kind
    [100, 8, 40, 4, 1],  # Straight Flush
    [60, 7, 30, 3, 1],  # four of a kind
    [40, 4, 25, 2, 1],  # full house
    [35, 4, 15, 2, 1],  # flush
    [30, 4, 30, 3, 1],  # straight
    [30, 3, 20, 2, 1],  # three of a kind
    [20, 2, 20, 1, 1],  # two pair
    [10, 2, 15, 1, 1],  # pair
    [5, 1, 10, 1, 1],  # high card
]
# chip, mult, x * lvl (chip scale), x * lvl (mult scale), lvl


commonJokers = {
    "Classic Joker": ["+4 Mult", 0, 4, 1, "common", 2, 1, 0],
    "Misprint": ["+0-23 Mult", 0, 0, 1, "common", 4, 2, 0],
    "Cavendish": ["Cavendish: X3 Mult 1 in 1000 chance you instantly lose"],
    "Lusty Joker": ["Played cards with Heart suit give +3 Mult when scored"],
    "Greedy Joker": ["Played cards with Diamond suit give +3 Mult when scored"],
    "Wrathful Joker": ["Played cards with Spade suit give +3 Mult when scored"],
    "Gluttonous Joker": ["Played cards with Club suit give +3 Mult when scored"],
    "Jolly Joker": ["+8 Mult if played hand contains a Pair"],
    "Zany Joker": ["+12 Mult if played hand contains a Three of a Kind"],
    "Wily Joker": ["+100 Chips if played hand contains a Three of a Kind"],
    "Droll Joker": ["+10 Mult if played hand contains a Flush"],
    "Mystic Summit": ["+15 Mult when 0 discards remaining"],
    "Trading Card": ["If first discard of round has only 1 card, destroy it"],
    "Smiley Face": ["Played face cards give +5 Mult when scored"],
    "Half Joker": ["+20 Mult if scored hand contains 3 or fewer cards"],
    "Gros Michel": ["+15 Mult, 1 in 10 chance this is destroyed each use"],
    "Even Steven": [
        "Played cards with even rank give +4 Mult when scored (10, 8, 6, 4, 2)"
    ],
    "Odd Todd": [
        "Played cards with odd rank give +31 Chips when scored (A, 9, 7, 5, 3)"
    ],
    "Scholar": ["Played Aces give +20 Chips and +4 Mult when scored"],
}
# name, desc, + Chips, + Mult, X Mult, rarity, cost, sell_cost, counter (scaling)

# sell_cost = math.max(1, math.floor(cost/2))

uncommonJokers = {
    "Four Fingers": ["All Flushes and Straights can be made with 4 cards"],
    "Acrobat": ["X3 Mult on final hand of round"],
    "Bloodstone": [
        "1 in 2 chance for played cards with Heart suit to give X1.5 Mult when scored"
    ],
    "Arrowhead": ["Played cards with Spade suit give +50 Chips when scored"],
    "Onyx Agate": ["Played cards with Club suit give +7 Mult when scored"],
    "Fibonacci": ["Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored"],
    "Space Joker": ["1 in 4 chance to upgrade level of played poker hand"],
}

rareJokers = {
    "Stuntman": ["+250 Chips, -2 hand size"],
    "The Trio": ["X3 Mult if played hand contains a Three of a Kind"],
    "The Family": ["X4 Mult if played hand contains a Four of a Kind"],
    "The Order": ["X3 Mult if played hand contains a Straight"],
    "The Tribe": ["X2 Mult if played hand contains a Flush"],
    "Brainstorm": ["Copies the ability of leftmost Joker"],
    "Burnt Joker": ["Upgrade the level of the first discarded poker hand each round"],
    "Triboulet": ["Played Kings and Queens each give X2 Mult when scored"],
}

DEBUG_MODE = 0

FAST_MODE = True
speeds = [0.01, 0.05, 0.075, 0.3]

if FAST_MODE:
    speeds = [0, 0, 0, 0]


hasHand = {
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
    "hasPair": False,
}


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.mult = 0

    def chips(self):
        if self.rank == 1:
            return 11
        if self.rank in (11, 12, 13):
            return 10
        return self.rank

    # Card Enhancements: Bonus, Mult, Wild, Glass, Steel, Stone, Gold, Lucky

    # Editions: Foil (+50 chips), Holographic (+10 Mult), Polychrome (X1.5 Mult), Negative

    # Seals: Gold Seal, Red Seal, Blue Seal, Purple Seal


def generateHand(handSize, baseCards) -> tuple:
    deck = copy.deepcopy(baseCards)
    random.shuffle(deck)
    return deck[0:handSize], deck[handSize:]


def drawCards(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]


def findFlush(hand: list, flushSize=5) -> bool:
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0}

    for card in hand:
        suitCount[card[-1]] += 1
        if card[-1] == "X": # wildcard
            suitCount["S"] += 1
            suitCount["H"] += 1
            suitCount["D"] += 1
            suitCount["C"] += 1

    if DEBUG_MODE:
        print("\nfindFlush Check")
        print("hand", hand, "flush size:", flushSize)
        print(suitCount)

    return any(count >= flushSize for count in suitCount.values())


def findStraight(hand: list, straightSize=5) -> bool:
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
            return True
    return False


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


# Orders the hand by rank, keeps the suits
def orderRank(hand: list) -> list:
    # It can be done in one line with the sorted() function and a lambda function / anonymous function
    return sorted(hand, key=lambda card: int(card[:-1]))

# Orders the hand suit. Ordered by rank within each respective suit.
def orderSuit(hand: list) -> list:
    spades, hearts, diamonds, clubs, wildcards  = [], [], [], [], []
    for cardSuit in hand:
        match cardSuit[-1]:
            case "S":
                spades.append(cardSuit)
            case "H":
                hearts.append(cardSuit)
            case "D":
                diamonds.append(cardSuit)
            case "C":
                clubs.append(cardSuit)
            case _:
                wildcards.append(cardSuit)
    return orderRank(spades) + orderRank(hearts) + orderRank(diamonds) + orderRank(clubs) + orderRank(wildcards)


# Finds the index of the input hand name from the hasHand dict
def findHighIndex(handName):
    return next((i for i, key in enumerate(hasHand) if key == handName), None)


# Checks for multi-card hand types and stores the found hands in a dict
# Returns tuple (True/False if its highcard, list of lists with the indices of scored cards from partial hand types)
def evalHand(hand: list, fourFingers: int) -> tuple:
    # Resets all poker hand flags to false
    for key in hasHand:
        hasHand[key] = False

    # Stored hands types are low to high
    partiaHandIndices = [None] * 12
    # Whole Hands
    hasHand["hasFlush"] = findFlush(hand, fourFingers)
    hasHand["hasStraight"] = findStraight(hand, fourFingers)
    hasHand["hasFiveOfAKind"] = findFiveOfAKind(hand)

    # Partial Hands
    hasHand["hasFourOfAKind"], partiaHandIndices[7] = findFourOfAKind(hand)
    hasHand["hasThreeOfAKind"], partiaHandIndices[3] = findThreeOfAKind(hand)
    if hasHand["hasThreeOfAKind"]:
        hasHand["hasFullHouse"], partiaHandIndices[6] = findFullHouse(hand)
    hasHand["hasPair"], partiaHandIndices[1] = findPair(hand)
    if hasHand["hasPair"]:
        hasHand["hasTwoPair"], partiaHandIndices[2] = findTwoPair(hand)

    # Combo Whole Hands
    hasHand["hasFlushFive"] = hasHand["hasFlush"] and hasHand["hasFiveOfAKind"]
    hasHand["hasFlushHouse"] = hasHand["hasFlush"] and hasHand["hasFullHouse"]
    hasHand["hasStraightFlush"] = hasHand["hasFlush"] and hasHand["hasStraight"]

    if DEBUG_MODE:
        print("evalHand Function")
        print(hasHand)

    foundMultiCardHand = any(hasHand.values())

    if not foundMultiCardHand:  # High Card
        partiaHandIndices[0] = highCardFinder(hand, True)

    # Returns True if any Poker Hands are found, returns False for High Card
    # and a LIST containting the indices of the SCORED cards for partial hand types (high card, pair, 3oak, 4oak, two pair)
    return foundMultiCardHand, partiaHandIndices


def scoreHand(hand, partiaHandIndices, notHighCard) -> tuple:
    if DEBUG_MODE:
        print("score HandFunction \n partiaHandIndices", partiaHandIndices)
    newPartialHand, highestHandName = None, None

    if notHighCard:
        # Find first true value in the dict (highest scoring hand type present in hand)
        for key, value in hasHand.items():
            if value:
                highestHandName = key
                break
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
    if highestHandName in partialHands.keys():
        # Feed the correct partiaHandIndices index and score the respective hand indices
        indices = partiaHandIndices[partialHands[highestHandName]]
        newPartialHand = [card for i, card in enumerate(hand) if i in indices]

        if DEBUG_MODE:
            print(highestHandName)
            print(partiaHandIndices[partialHands[highestHandName]])
            print(newPartialHand)

    hand = hand if newPartialHand is None else newPartialHand

    # If highestHandName is None, set highestHandIndex to zero (high hand), else
    highestHandIndex = (
        11 if highestHandName == "hasHighHand" else findHighIndex(highestHandName)
    )
    tempChips = countChips(hand)
    chip, mult = calculateChipMult(tempChips, highestHandIndex)
    return chip, mult, hand


# Counts chips given by cards from the played hand
def countChips(hand):
    total = 0
    for card in hand:
        rank = int(card[:-1])
        if DEBUG_MODE:
            print("rank", rank, end=" ")
        match rank:
            case 1:
                chips = 11
            case 11 | 12 | 13:
                chips = 10
            case _:
                chips = rank
        total += chips
    if DEBUG_MODE:
        print(", total", total)
    return total

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


def calculateChipMult(cardChips, handIndex):
    # The last multiply by (chipMultTable[handIndex][4] - 1) is for hand lvl scaling
    chip = cardChips + (
        chipMultTable[handIndex][0]
        + chipMultTable[handIndex][2] * (chipMultTable[handIndex][4] - 1)
    )
    mult = chipMultTable[handIndex][1] + chipMultTable[handIndex][3] * (
        chipMultTable[handIndex][4] - 1
    )
    return chip, mult



def jokerSelection(playerJokers):
    currentJokerShop = jokerShop()
    selected = []
    # tuple of strings with the joker name and description for the current joker shop
    options = tuple(map(lambda item: item[0] + " - " + item[1][0], currentJokerShop))

    while len(selected) != 3:
        title = "Select 3 jokers (press SPACE to mark, ENTER to continue): "
        selected = pick(options, title, multiselect=True, min_selection_count=3)

    for i in selected:
        playerJokers.append(currentJokerShop[i[1]])

    text_ui.printJokers(playerJokers)


def jokerShop() -> list:
    #allJokers = commonJokers | uncommonJokers | rareJokers
    currentJokerShop = []

    for i in range(8):
        rng = random.randrange(0, 100)
        if i < 3 or rng < 50:
            key, value = random.choice(list(commonJokers.items()))
            del commonJokers[key]
        elif rng > 85:
            key, value = random.choice(list(rareJokers.items()))
            del rareJokers[key]
        else:
            key, value = random.choice(list(uncommonJokers.items()))
            del uncommonJokers[key]
        currentJokerShop.append((key, value))

    return currentJokerShop


def deckSelection(allDecks) -> int:
    # Returns a tuple of strings with the deck name and description
    options = tuple(map(lambda item: item[0] + " - " + item[1], allDecks.items()))
    title = "Select a deck (ENTER to continue): "
    selected = pick(options, title)
    print("Selected Deck:", selected[0])
    return selected[1]



def endJokerCalculation(chip, mult, XMult, playerJokers, currentDiscards, scoredCards):
    # to do todo: remove this testing block
    #allJokers = commonJokers | uncommonJokers | rareJokers
    #for i, v in enumerate(allJokers):  # Gives player every joker
        #playerJokers.append(v)

    #playerJokers = ["Stuntman", "Cavendish"]  # to do todo: remove

    noSuitHand = removeSuits(scoredCards)
    time.sleep(speeds[3])
    time.sleep(speeds[3])
    for jokers in playerJokers:
        match jokers[0]:
            case "Classic Joker":
                mult += 4
                text_ui.slowWordPrint("Joker: +4", "mult")
            case "Misprint":
                misprintMult = random.randint(0, 24)
                mult += misprintMult
                text_ui.slowWordPrint("Misprint: +" + str(misprintMult), "mult")
            case "Cavendish":
                XMult += 3
                text_ui.slowWordPrint("Cavendish: X3", "XMult")
                if random.randrange(0, 999) == 67:
                    print("Cavendish: 1 in 1000. You lose.")
                    sys.exit(0)
            case "Stuntman":
                chip += 250
                text_ui.slowWordPrint("Stuntman: +250", "chip")
            case "Jolly Joker":
                if hasHand["hasPair"]:
                    text_ui.slowWordPrint("Jolly Joker: +8", "mult")
                    mult += 8
            case "Zany Joker":
                if hasHand["hasThreeOfAKind"]:
                    text_ui.slowWordPrint("Zany Joker: +12", "mult")
                    mult += 12
            case "Wily Joker":
                if hasHand["hasThreeOfAKind"]:
                    text_ui.slowWordPrint("Wily Joker: +100", "chip")
                    chip += 100
            case "Droll Joker":
                if hasHand["hasFlush"]:
                    text_ui.slowWordPrint("Droll Joker: +10", "mult")
                    mult += 10
            case "Mystic Summit":
                if currentDiscards == 0:
                    text_ui.slowWordPrint("Mystic Summit: +15", "mult")
                    mult += 15
            case "Half Joker":
                if len(scoredCards) <= 3:
                    text_ui.slowWordPrint("Half Joker: +20", "mult")
                    mult += 20
            case "Gros Michel":
                mult += 15
                text_ui.slowWordPrint("Gros Michel: +15", "mult")
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
                text_ui.slowWordPrint(text, "mult")
            case "Odd Todd":
                oddCount = 0
                for rank in noSuitHand:
                    if rank % 2 == 1 and rank not in {11, 12, 13}:
                        oddCount += 1

                chip += oddCount * 31
                text = "Odd Todd: +" + str(oddCount) + " * 31"
                text_ui.slowWordPrint(text, "chip")
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



def main():
    playerJokers = []
    selectedDeck = None

    #dollars = 0
    totalHands, currentHands = 4, 4
    totalDiscards, currentDiscards = 3, 3
    handSize = 8

    currentLevel = 0
    requiredScores = [5000, 10000, 20000, 50000]
    score = 0

    chip, mult, XMult = 0, 0, 1

    partiaHandIndices = None
    playedHand = []
    discardPile = []
    fourFingers = 5

    allDecks = {
        "Red Deck": "+1 discard every round",
        "Blue Deck": "+1 hand every round",
        "Abandoned Deck": "No Face Cards in your deck",
        "Checkered Deck": "Only Hearts and Spades",
        "Picky Deck": "Start with the Trading Card Joker",
        "Coal Deck": "Start with the Burnt Joker",
        "Green Deck": "Start with 3 random Common Jokers",
        "Gambler Deck": "Start with 2 random Uncommon Jokers",
        "High Roller Deck": "Start with a random Rare Joker",
        "Cobble Deck": "All Face Cards are replaced with Stone Cards (50 chips each)",
        "Erratic Deck": "All Ranks and Suits in deck are randomized",
    }

    baseCards = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ]


    '''
    # altered with a lot of 1s for testing
    baseCards1 = [
            "1C", "1C", "1C", "1C", "1C", "1C", "7C", "8C", "9C", "10C", "11C", "12C", "13C",
            "1C","1C","1C","1C","1C","1C","1C","1C","1C","1C"
        ]

    baseCards2 = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C" # 0 - 13
    ]
    '''
    checkeredDeck = [
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 0 - 13
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S", # 14 - 26
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
        ]

    abandonedDeck = [
            "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C",
            "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D",
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H",
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S"
        ]

    clearConsole()
    if not FAST_MODE:
        text_ui.printInstructions()
        time.sleep(speeds[3])

    # deck selection
    # if not FAST_MODE: selectedDeck = deckSelection(selectedDeck)
    # else: selectedDeck = 0
    selectedDeck = deckSelection(allDecks)

    # apply new deck
    match selectedDeck:
        case 0:  # red
            totalDiscards += 1
            currentDiscards = totalDiscards
        case 1:  # blue
            totalHands += 1
            currentHands = totalHands
        case 2:  # abandoned
            baseCards = abandonedDeck
        case 3:  # checkered
            baseCards = checkeredDeck
        case 4:  # picky
            playerJokers.append("Trading Card")
            del commonJokers["Trading Card"]
        case 5:  # coal
            playerJokers.append("Burnt Joker")
            del commonJokers["Burnt Joker"]
        case 6:  # green
            for i in range(3):
                key, item = random.choice(list(commonJokers.items()))
                del commonJokers[key]
                playerJokers.append([key, item])
        case 7:  # Gambler
            for i in range(2):
                key, item = random.choice(list(uncommonJokers.items()))
                del uncommonJokers[key]
                playerJokers.append([key, item])
        case 8:  # high roller
            key, item = random.choice(list(rareJokers.items()))
            del rareJokers[key]
            playerJokers.append([key, item])
        case 9:  # cobble
            for i in range(len(baseCards)):
                if baseCards[i][:-1] in {"11", "12", "13"}:
                    baseCards[i] = "50" + baseCards[i][-1]
        case 10:  # erratic
            for i in range(len(baseCards)):
                rank = random.randint(1, 13)
                suit = random.choice(["S", "H", "D", "C"])
                baseCards[i] = str(rank) + suit
            baseCards = orderSuit(baseCards)
        case _:
            pass

    # Joker Selection from joker shop
    # if not FAST_MODE: jokerSelection(playerJokers)
    # else: playerJokers = []
    jokerSelection(playerJokers)
    # apply jokers that affect deck, hand
    for jokers in playerJokers:
        match jokers:
            case "Stuntman":
                handSize -= 2
            case "Four Fingers":
                fourFingers = 4
            case _:
                pass

    # todo to do adjust and move to account for multiple levels
    handWithDeck = generateHand(handSize, baseCards)
    hand, deck = orderRank(handWithDeck[0]), handWithDeck[1]

    time.sleep(speeds[3])
    # Per game Loop
    while currentLevel < len(requiredScores):
        # Per level Loop
        while score < requiredScores[currentLevel]:
            chip, mult, XMult = 0, 0, 1

            # Check for lose condition
            if currentHands <= 0 and score < requiredScores[currentLevel]:
                print(score, "is less than ", requiredScores[currentLevel], ".\nGame Over")
                sys.exit(0)

            text_ui.mainLoopPrompt(requiredScores[currentLevel], score, currentHands, currentDiscards, score)
            text_ui.printHand(hand)
            print("Deck Length:", len(deck))
            userInput = input()
            userInputAction = userInput[0].lower()
            userInputCardIndex = userInput[1:].strip()
            selectedIndicesSet = {int(x) for x in userInputCardIndex}

            # Limit hand / discard size
            if len(selectedIndicesSet) > 5:
                print("Error: selected too many cards")
                text_ui.mainLoopPrompt(requiredScores[currentLevel], score, currentHands, currentDiscards, 2)
                continue

            # DISCARD
            if userInputAction == "d" and currentDiscards > 0:
                currentDiscards -= 1
                # Removes cards from the hand based on indices
                keptCards = []
                for i, j in enumerate(hand):
                    if i not in selectedIndicesSet:
                        keptCards.append(j)
                    else:
                        discardPile.append(j)
                        # todo to do Handle Burnt Joker here
                        # todo to do Handle Trading Card
                        # todo to do Handle new jokers that delete certain ranks
                hand = keptCards
                hand, deck = drawCards(hand, deck, handSize)

            # PLAY
            elif userInputAction == "p":
                currentHands -= 1
                for i, card in enumerate(hand):
                    if i in selectedIndicesSet:
                        playedHand.append(card)
                # Sorts the inputted hand
                playedHand = orderRank(playedHand)
                print("You played:", playedHand)
                # notHighCard lets us know if it's a multi card hand thats being scored
                notHighCard, partiaHandIndices = evalHand(playedHand, fourFingers)

                #scoredHandType = None  # might not need this, jokers can check hasHand= {} to check if hand types are present
                chip, mult, scoredCards = scoreHand(playedHand, partiaHandIndices, notHighCard)
                text_ui.printEquation(chip, mult)

                chip, mult, XMult = endJokerCalculation(
                    chip, mult, XMult, playerJokers, currentDiscards, scoredCards
                )
                XMult = XMult if XMult == 1 else XMult - 1

                text_ui.endOfCalcPrint(chip, mult, XMult)
                score += chip * (mult * XMult)
                text_ui.slowWordPrint("Total level Score", None, speeds[2])
                time.sleep(speeds[3])
                if score > requiredScores[currentLevel]:
                    text_ui.rainbowText(score)
                else:
                    text_ui.slowWordPrint(score, None, speeds[2])
                print()
                print()
                # todo to do: next hand / round logic

                keptCards = []
                for card in hand:
                    if card not in playedHand:
                        keptCards.append(card)

                hand, deck = drawCards(keptCards, deck, handSize)
                # Resets playedHand
                discardPile.append(playedHand)  # todo to do discard pile
                playedHand = []

            elif userInputAction == "d" and currentDiscards == 0:
                print("Error: Out of Discards. Try Again")
                text_ui.mainLoopPrompt(requiredScores[currentLevel], score, currentHands, currentDiscards, 2)
                continue

            # help
            elif userInputAction == "?":
                print('"q" to quit\n"c" to clear text\n"j" to view jokers\n"v" to view deck')

            # QUIT
            elif userInputAction == "q":
                sys.exit(0)

            # CLEAR
            elif userInputAction == "c":
                clearConsole()

            # JOKERS
            elif userInputAction == "j":
                text_ui.printJokers(playerJokers)

            # VIEW DECK
            elif userInputAction == "v":
                # Temp variable to prevent changing deck order
                remainingDeckTemp = orderSuit(deck)
                text_ui.printDeck(baseCards, remainingDeckTemp)

            else:
                clearConsole()
                print("Error: Try Again")
                time.sleep(speeds[1])

        # Beat the current level
        if score > requiredScores[currentLevel]:
            print(score, "is greater than", requiredScores[currentLevel])
            # Reset variables for next level
            currentLevel += 1
            score = 0
            currentHands = totalHands
            currentDiscards = totalDiscards
            # baseCards = discardPile + deck + remaining cards in hand #to do todo
            print("Press enter to continue")
            input()
            print("--- LEVEL", currentLevel + 1, "---")  # +1 for 0 index
            time.sleep(speeds[3])

    print("--- You win ---")


if __name__ == "__main__":
    main()
