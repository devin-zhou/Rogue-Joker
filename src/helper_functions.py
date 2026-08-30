import os
import random

#from games
#removeSuits()

def getRandomIndices(deck, k) -> list:
    return random.sample(range(len(deck)), k)

def findJoker(jokerName, jokerList) -> bool:
    for joker in jokerList:
        if joker[0] == jokerName:
            return True
    return False

#from deck_functions
#orderSuit
#orderRank

def calculateChipMult(cardChips, handIndex, chipMultTable) -> tuple:
    baseChip, chipScaling = chipMultTable[handIndex][0], chipMultTable[handIndex][2]
    baseMult, multScaling = chipMultTable[handIndex][1], chipMultTable[handIndex][3]
    handLvl = chipMultTable[handIndex][4] - 1

    calculatedChip = cardChips + baseChip + (chipScaling * handLvl)
    calculatedMult = baseMult + (multScaling * handLvl)
    return calculatedChip, calculatedMult


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

# Find first true value in the dict (highest scoring hand type present in hand)
def findHighestHandName(foundHands):
    for key, value in foundHands.items():
        if value:
            return key
    return "hasHighHand"

# Finds the index of the input hand name from the hasHand dict
def handNameToIndex(handName, hasHand) -> int:
    return next((i for i, key in enumerate(hasHand) if key == handName), None)

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

def clearConsole():
    # windows
    if os.name == "nt":
        _ = os.system("cls")
    # mac linux
    else:
        _ = os.system("clear")
