import random
import copy
import random

from colorama import Fore, Back, Style
import rich


baseCards1 = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ];

# altered with a lot of 1s for testing
baseCards = [
        "1C", "1C", "1C", "1C", "1C", "1C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "1D", "1D", "1D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "1H", "1H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ];


chipMultTable = [
  [160, 16, 50, 3, 1],
  [140, 14, 40, 4, 1],
  [120, 12, 35, 3, 1],
  [100,  8, 40, 4, 1],
  [ 60,  7, 30, 3, 1],
  [ 40,  4, 25, 2, 1],
  [ 35,  4, 15, 2, 1],
  [ 30,  4, 30, 3, 1],
  [ 30,  3, 20, 2, 1],
  [ 20,  2, 20, 1, 1],
  [ 10,  2, 15, 1, 1],
  [  5,  1, 10, 1, 1] # high card
]
# blue chip, red mult, this * handLVL for chip scale, this * hand level for mult scale, handLVL


allJokers = {
    "Joker": ["+4 Mult", 0, 4, 1, "common", 2, 1, 0],
    "Misprint": ["+0-23 Mult", 0, random.randrange(0, 24), 1, "common", 4, 2, 0] # misprint randomizes only radomizes once
}
# name, desc, + Chips, + Mult, X Mult, rarity, cost, sell_cost, counter (scaling)

# sell_cost = math.max(1, math.floor(cost/2))

debugMode = 0

DEFAULT_HAND_SIZE = 8
DEFAULT_JOKER_SLOTS = 5
DEFAULT_DECK_SIZE = 52

currentJokers = []

# parallel list vs dict
hasPokerHand = [False,False,False,
                False,False,False,
                False]
thePokerHand = ["hasPair", "hasTwoPair", "hasThreeOfAKind", "hasFullHouse"
                "hasFourOfAKind", "hasFiveOfAKind", "hasStraight", 
                "hasFlush"]

# parallel list vs dict
hasHand = {
    "hasFlushFive": False, "hasFlushHouse": False,
    "hasFiveOfAKind": False, "hasStraightFlush": False,
    "hasFlush": False, "hasStraight": False,
    "hasFiveOfAKind": False, "hasFourOfAKind": False,
    "hasFullHouse": False, "hasThreeOfAKind": False,
    "hasTwoPair": False, "hasPair": False
}

handRankings = {
    "highCard": 0,
    "pair": 1,
    "twoPair": 2,
    "threeOfAKind": 3,
    "straight": 4,
    "flush": 5,
    "fullHouse": 6,
    "fourOfAKind": 7,
    "straightFlush": 8,
    "fiveOfAKind": 9,
    "flushHouse": 10,
    "flushFive": 11
}

class card:
    def __init__(self): 
        self.rank = 1
        self.suit = "C"
        self.mult = 0
        self.chips = self.rank # idk if need this declaration, same thing is in the Else of the Pattern Matching
        match self.rank:
            case 1:
                self.chips = 11
            case 11, 12, 13:
                self.chips = 10
            case _:
                self.chips = self.rank
        #Enhancements: Bonus card, Mult Card, Wild Card, Glass Card, Steel Card, Stone Card, Gold Card, Lucky Card

        #Editions: Base, Foil (+50 chips), Holographic (+10 Mult), Polychrome (X1.5 Mult), Negative (+ 1 Joker Slot)

        #Seals: Gold Seal, Red Seal, Blue Seal, Purple Seal



def generateHand(handSize) -> tuple:
    deck = copy.deepcopy(baseCards)
    random.shuffle(deck)
    return deck[0:handSize], deck[handSize:]

def discardDraw(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]




def find_flush(hand: list, flushSize = 5) -> bool:
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0}
    # Joker: Four Fingers
    # if global var has the joker? or make a parameter for it in this func?
    #flushSize = 4

    for i in range(len(hand)):
        suitCount[hand[i][-1]] += 1

    if debugMode:
        print("\nfind_flush Check")
        print("hand", hand, "flush size:", flushSize)
        print(suitCount)
        
    return any(count >= flushSize for count in suitCount.values())

def find_straight(hand: list, straightSize = 5) -> bool:
    orderedHand = orderRankNumbers(hand)
    # Joker: Four Fingers
    # if global var has the joker? or make a parameter for it in this func?
    #straightSize = 4

    # Ace Case
    # Might not work with Four Fingers
    if aceCheck(hand) and 13 in orderedHand:
        orderedHand.remove(1)
        orderedHand.append(14)

    if debugMode:
        print("\nfind_straight Check")
        print("sorted hand", orderedHand)
        print("sums", sum(orderedHand), orderedHand[0] * 5 + 10)
        print("first card == last card minus 4:", orderedHand[0], orderedHand[-1] - 4)

    return len(orderedHand) == straightSize and sum(orderedHand) == orderedHand[0] * 5 + 10 and orderedHand[0] == orderedHand[-1] - 4

def find_five_of_a_kind(hand: list) -> bool:
    orderedHand = orderRankNumbers(hand)
    if debugMode:
        print("\nfind_five_of_a_kind Check")
        print("hand", orderedHand, len(orderedHand))
        print(all(orderedHand[0] == a for a in orderedHand))
    return all(orderedHand[0] == a for a in orderedHand) and len(orderedHand) == 5

def find_four_of_a_kind(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)

    if debugMode:
        print("\nfind_four_of_a_kind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 4 and orderedHand[0] == orderedHand[3]:
            return True, [0, 1, 2, 3]
    if len(orderedHand) == 5 and orderedHand[1] == orderedHand[4]:
            return True, [1, 2, 3, 4]
    return False, None

def find_three_of_a_kind(hand: list, sorted = False) -> tuple:
    orderedHand = orderRankNumbers(hand) if not sorted else hand

    if debugMode:
        print("\nfind_three_of_a_kind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 3 and orderedHand[0] == orderedHand[2]:
            return True, [0, 1, 2]
    if len(orderedHand) >= 4 and orderedHand[1] == orderedHand[3]:
            return True, [1, 2, 3]
    if len(orderedHand) >= 5 and orderedHand[2] == orderedHand[4]:
        return True, [2, 3, 4]
    return False, None

def find_pair(hand: list, sorted = False) -> tuple:
    orderedHand = orderRankNumbers(hand) if not sorted else hand

    if debugMode:
        print("\nfind_pair Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 2 and orderedHand[0] == orderedHand[1]:
            return True, [0, 1]
    if len(orderedHand) >= 3 and orderedHand[1] == orderedHand[2]:
            return True, [1, 2]
    if len(orderedHand) >= 4 and orderedHand[2] == orderedHand[3]:
            return True, [2, 3]
    if len(orderedHand) >= 5 and orderedHand[3] == orderedHand[4]:
        return True, [3, 4]
    return False, None

def find_two_pair(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)
    hasSecondPair, pairIndex2 = None, None

    hasFirstPair, pairIndex = find_pair(orderedHand, True)

    if hasFirstPair:
        orderedHand[pairIndex[0]] = "x"
        orderedHand[pairIndex[1]] = "y"
        # Following works but removes them from the list permanently
        #del orderedHand[pairIndex[0]:pairIndex[1]+1]
        hasSecondPair, pairIndex2 = find_pair(orderedHand, True)

    if debugMode:
        print("\nfind_two_pair Check")
        print("hand", orderedHand, len(orderedHand))
        print(hasFirstPair, pairIndex)
        print(hasSecondPair, pairIndex2)

    if hasFirstPair and hasSecondPair:
        return True, pairIndex + pairIndex2
    return False, None

def find_full_house(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)
    hasPair, pairIndex = None, None

    hasThree, threeIndex = find_three_of_a_kind(orderedHand, True)

    if hasThree:
        orderedHand[threeIndex[0]] = "x"
        orderedHand[threeIndex[1]] = "y"
        orderedHand[threeIndex[2]] = "z"
        # Following works but removes them from the list permanently
        #del orderedHand[pairIndex[0]:pairIndex[1]+1]
        hasPair, pairIndex = find_pair(orderedHand, True)

    if debugMode:
        print("\nfind_full_house Check")
        print("hand", orderedHand, len(orderedHand))
        print(hasPair, pairIndex)

    if hasThree and hasPair:
        return True, pairIndex + threeIndex
    return False, None




# Orders the hand suit. Ordered by rank within each respective suit.
def orderSuit(hand: list) -> list:
    spades, hearts, diamonds, clubs  = [], [], [], []
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
                print("Error")
    return orderRank(spades) + orderRank(hearts) + orderRank(diamonds) + orderRank(clubs)

# Orders the hand by rank, removes the suits, making them int
def orderRankNumbers(hand: list) -> list:
    orderedHand = [int(card[:-1]) for card in hand] # Removes the suit character at the end of each index
    orderedHand.sort(key = int) # List of numbers in quotations, key allows us to sort them as ints without disturbing the list
    return orderedHand

# Orders the hand by rank, keeps the suits
def orderRank(hand: list) -> list:
    # Way to do it without touching the suits:
    #hand.sort(key=lambda card: int(card[:-1]))

    # It can be done in one line with the sorted() function and a lambda function / anonymous function
    return sorted(hand, key=lambda card: int(card[:-1]))



# UNUSED
# List of strings to list of tuples (Rank, "Suit")
def stringToTuple(hand: list) -> list: # UNUSED
    ranks = []; suits = []
    for card in hand:
        ranks.append(int(card[:-1]))
        suits.append(card[-1])
    return list(map(lambda rank, suit : (rank, suit), ranks, suits))
# UNUSED
def stringToTuple2(hand: list) -> list: # UNUSED
    return [(int(card[:-1]), card[-1]) for card in hand]


def aceCheck(hand: list) -> bool:
    return any(ace[:-1] == "1" for ace in hand)

def findHIndex(handName): # Finds the index of the input hand name
    for i, j in enumerate(hasHand):
        if j == handName:
            return i
    return None




def evalHand(hand: list) -> tuple:
    scoredCards = [None] * 12
    print()
    print(hand)

# Whole Hands
    hasHand["hasFlush"] = find_flush(hand)
    hasHand["hasStraight"] = find_straight(hand)
    hasHand["hasFiveOfAKind"] = find_five_of_a_kind(hand)
    
# Partial Hands
    hasHand["hasFourOfAKind"], scoredCards[7] = find_four_of_a_kind(hand)
    
    hasHand["hasThreeOfAKind"], scoredCards[3] = find_three_of_a_kind(hand)
    if hasHand["hasThreeOfAKind"]:
        hasHand["hasFullHouse"], scoredCards[6] = find_full_house(hand)
            
    hasHand["hasPair"], scoredCards[1] = find_pair(hand)
    if hasHand["hasPair"]:
        hasHand["hasTwoPair"], scoredCards[2] = find_two_pair(hand)

# Combo Whole Hands
    hasHand["hasFlushFive"] = hasHand["hasFlush"] and hasHand["hasFiveOfAKind"]
    hasHand["hasFlushHouse"] = hasHand["hasFlush"] and hasHand["hasFullHouse"]
    hasHand["hasStraightFlush"] = hasHand["hasFlush"] and hasHand["hasStraight"]

    if debugMode:
        print("evalHand Function")
        print(hasHand)

    print()
    # Returns True if any Poker Hands are found, returns False for High Card
    return any(handType == True for handType in hasHand.values()), scoredCards 


def scoreHand(hand, scoredCards = None) -> int:
    if debugMode: print("scoredCards", scoredCards)
    cardChips = 0
    newHand = None
    highestHandType = None
# Find first true value in the dict
    for k, v in hasHand.items():
        if v == True: 
            highestHandType = k
            break
    print("Score the following:", highestHandType)

    partialHands = {"hasFourOfAKind":7, "hasThreeOfAKind":3, "hasPair":1, "hasTwoPair":2}

# Check if the hand we're scoring is a partial hand or not
    if highestHandType in partialHands.keys():
    # Feed the correct scoredCards index here and score the respective hand indices 
        indices = scoredCards[partialHands[highestHandType]]
        newHand = [card for i, card in enumerate(hand) if i in indices]
        if debugMode:
            print("scoreHand: Function", highestHandType)
            print(scoredCards[partialHands[highestHandType]])
            print(indices)
            print(newHand)

    hand = hand if newHand == None else newHand

    for card in hand:
        rank = int(card[:-1])
        print("rank", rank, end=" ")
        match rank: #to do functionize this for high card?
            case 1:
                chips = 11
            case 11 | 12 | 13:
                chips = 10
            case _:
                chips = rank
        cardChips += chips
    print(", total", cardChips)

    if highestHandType == None:
        highHandInd = 0
    else:
        highHandInd = findHIndex(highestHandType)
    
    # to do functionize the calcs
    # Multiply by (chipMultTable[highHandInd][4] - 1) is for hand lvl scaling
    totalChip = cardChips + (chipMultTable[highHandInd][0] + chipMultTable[highHandInd][2] * (chipMultTable[highHandInd][4] - 1))
    totalMult = chipMultTable[highHandInd][1] + chipMultTable[highHandInd][3] * (chipMultTable[highHandInd][4] - 1)
    calculateScore = totalChip * totalMult
    print("Total Chips:", totalChip, "Total Mult:", totalMult) #to do color, blue and red
    print("You scored:", calculateScore)
    return calculateScore

def jokerSelection():
    while not currentJokers:
        print("Select a Joker by index")
        # Traverse and print joker dict with indices for input selection
        [print(f'{index}. {key}:\t{value[0]}') for index, (key, value) in enumerate(allJokers.items())]
        currentJokers.append(int(input()))
    print("jokers:", currentJokers)

def printHand(hand):
    #[print(f"{i}. {colorCard(v)}") for i, v in enumerate(hand)]
    for i, v in enumerate(hand):
        print(f"{i}.", end="")
        colorCard(v)
        print()

def colorCard(card):
    match card[-1]:
        case "H":
            print(Fore.RED + card, end=" ")
        case "D":
            print(Fore.YELLOW + card, end=" ")
        case "S":
            print(Fore.BLUE + card, end=" ")
        case "C":
            print(Fore.GREEN + card, end=" ")
        case _: # wildcard modfier?
            print(card)
    print(Style.RESET_ALL, end="")
    


def main():
    score = 0
    handAndDeck = generateHand(DEFAULT_HAND_SIZE)
    hand, deck = orderRank(handAndDeck[0]), handAndDeck[1]
    scoredCards = None

    jokerSelection()
        
    playedHand = []
    #print("In the crib playing balala")
    print("Enter P followed by indices to play the hand. D for discard. E.g. p 023")
    while not playedHand:
        print("Rank Order:")
        printHand(hand)
        #[print(f"{i}. {v}") for i, v in enumerate(hand)]
        print()
        print("Suit Order:", orderSuit(hand), len(deck))
        userInput = input()
        userInputAction = userInput[0].lower()
        userInputCardIndex = userInput[1:].strip()

    # Discard
        if (userInputAction == 'd'):
            discards = {int(x) for x in userInputCardIndex}
            # to do unlimited discards atm
            hand = [j for i, j in enumerate(hand) if i not in discards] # Removes cards from the hand based on indices
            hand, deck = discardDraw(hand, deck, DEFAULT_HAND_SIZE)
            print(deck) # TEMP todo: make into debug line
    # Play
        elif (userInputAction == 'p'):
            indices = {int(x) for x in userInputCardIndex}
            # to do unlimited played cards atm
            for i in range(len(hand)):
                if i in indices:
                    playedHand.append(hand[i])
            print("You played:", playedHand)
            notHighCard, scoredCards = evalHand(playedHand) #notHighCard lets us know if it's a multi card hand thats being scored

            if notHighCard: # multi card poker hand
                score += scoreHand(playedHand, scoredCards)
            else: # to do: high card
                pass
            # evaluate jokers here
            print("Subtotal score", score)

            #to do: check if the blind is defeated
            #to do: next hand / round logic 
                # or end game if hands are out (hands are inf rn)
            
        else:
            print("Game Over---------------------")
            break

if __name__ == "__main__":
    main()