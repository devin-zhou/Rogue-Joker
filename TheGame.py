import random
import copy

baseCards1 = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ];

# altered with a lot of 1s
baseCards = [
        "1C", "1C", "1C", "1C", "1C", "1C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "1D", "1D", "1D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "1H", "1H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ];

deck = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ];

#what are these values
handChips = [
  [160, 16, 50, 3],
  [140, 14, 40, 4],
  [120, 12, 35, 3],
  [100,  8, 40, 4],
  [ 60,  7, 30, 3],
  [ 40,  4, 25, 2],
  [ 35,  4, 15, 2],
  [ 30,  4, 30, 3],
  [ 30,  3, 20, 2],
  [ 20,  2, 20, 1],
  [ 10,  2, 15, 1],
  [  5,  1, 10, 1]
]

debugMode = 0

DEFAULT_HAND_SIZE = 8
DEFAULT_JOKER_SLOTS = 5
DEFAULT_DECK_SIZE = 52


# parallel list vs dict
hasPokerHand = [False,False,False,
                False,False,False,
                False]
thePokerHand = ["hasPair", "hasTwoPair", "hasThreeOfAKind", "hasFullHouse"
                "hasFourOfAKind", "hasFiveOfAKind", "hasStraight", 
                "hasFlush"]

# parallel list vs dict
hasHand = {
    "hasPair": False,       "hasTwoPair": False,
    "hasThreeOfAKind": False,   "hasFullHouse": False,
    "hasFourOfAKind": False,    "hasFiveOfAKind": False,
    "hasStraight": False,   "hasFlush": False
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

# Notes
'''
Flow
    Hand type, resolve jokers that require knowledge of hand, knowledge of joker order, , knowledge of jokers, 
    score cards, score cards-in-hand (steel), score jokers, 

PAIRS / THREE OF A KIND / FOUR OF A KIND
    Reference checks for x of a kind by checking for 4 of a Kind -> found pair, 3, and 4 of a kind then going down until pair
    4OAK: if hand size == 4, then checks if list[0] == list[3]
        then if hand size == 5, check (if list[0] == list[3]) or (if list[1] == list[4])

    5 of a kind, flush five, flush house, straight flush are checked on their own

order: flush 5, flush house, 5 of a kind, straight flush, 4 of a kind, full house, flush, straight, 3 of a kind, 2 pair, pair, high card


Flush: Flushes are stored in an array of arrays [[], [], [], []]. Each suit corresponds to an index and is pushed into the corresponding array.
    Index and suit are setup so that Smeared Joker can be found using modulus:
    Eg: (this.SmearedJoker ? card[SUIT] % 2 == i : card[SUIT] === i)

'''



class card:
    def __init__(self): 
        self.rank = 1
        self.suit = "C"
        self.mult = 0
        self.chips = self.rank # idk if i need this declaration? same thing is in the Else of the Pattern Matching
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
    randomHand = copy.deepcopy(baseCards)
    random.shuffle(randomHand)
    return randomHand[0:handSize], randomHand[handSize:]

def discardDraw(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]


def flush(hand: list, flushSize = 5) -> bool:
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0}
    # Joker: Four Fingers
    # if global var has the joker? or make a parameter for it in this func?
    #flushSize = 4

    for i in range(len(hand)):
        suitCount[hand[i][-1]] += 1

    if debugMode:
        print("\nFlush Check")
        print("hand", hand, "flush size:", flushSize)
        print(suitCount)
        
    return any(count >= flushSize for count in suitCount.values())

def straight(hand: list, straightSize = 5) -> bool:
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
        print("\nStraight Check")
        print("sorted hand", orderedHand)
        print("sums", sum(orderedHand), orderedHand[0] * 5 + 10)
        print("first card == last card minus 4:", orderedHand[0], orderedHand[4] - 4)

    return len(orderedHand) == straightSize and sum(orderedHand) == orderedHand[0] * 5 + 10 and orderedHand[0] == orderedHand[4] - 4

def fiveOfAKind(hand: list) -> bool:
    orderedHand = orderRankNumbers(hand)
    if debugMode:
        print("\nfiveOfAKind Check")
        print("hand", orderedHand, len(orderedHand))
        print(all(orderedHand[0] == a for a in orderedHand))
    return all(orderedHand[0] == a for a in orderedHand) and len(orderedHand) == 5

def fourOfAKind(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)

    if debugMode:
        print("\nfourOfAKind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 4 and orderedHand[0] == orderedHand[3]:
            return True, [0, 1, 2, 3]
    if len(orderedHand) == 5 and orderedHand[1] == orderedHand[4]:
            return True, [1, 2, 3, 4]
    return False, None

def threeOfAKind(hand: list, sorted = False) -> tuple:
    orderedHand = orderRankNumbers(hand) if not sorted else hand

    if debugMode:
        print("\nthreeOfAKind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 3 and orderedHand[0] == orderedHand[2]:
            return True, [0, 1, 2]
    if len(orderedHand) >= 4 and orderedHand[1] == orderedHand[3]:
            return True, [1, 2, 3]
    if len(orderedHand) >= 5 and orderedHand[2] == orderedHand[4]:
        return True, [2, 3, 4]
    return False, None

def pair(hand: list, sorted = False) -> tuple:
    orderedHand = orderRankNumbers(hand) if not sorted else hand

    if debugMode:
        print("\npair Check")
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

def twoPair(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)
    hasSecondPair, pairIndex2 = None, None

    hasFirstPair, pairIndex = pair(orderedHand, True)

    if hasFirstPair:
        orderedHand[pairIndex[0]] = "x"
        orderedHand[pairIndex[1]] = "y"
        # Following works but removes them from the list permanently
        #del orderedHand[pairIndex[0]:pairIndex[1]+1]
        hasSecondPair, pairIndex2 = pair(orderedHand, True)

    if debugMode:
        print("\ntwoPair Check")
        print("hand", orderedHand, len(orderedHand))
        print(hasFirstPair, pairIndex)
        print(hasSecondPair, pairIndex2)

    if hasFirstPair and hasSecondPair:
        return True, pairIndex + pairIndex2
    return False, None

def fullHouse(hand: list) -> tuple:
    orderedHand = orderRankNumbers(hand)
    hasPair, pairIndex = None, None

    hasThree, threeIndex = threeOfAKind(orderedHand, True)

    if hasThree:
        orderedHand[threeIndex[0]] = "x"
        orderedHand[threeIndex[1]] = "y"
        orderedHand[threeIndex[2]] = "z"
        # Following works but removes them from the list permanently
        #del orderedHand[pairIndex[0]:pairIndex[1]+1]
        hasPair, pairIndex = pair(orderedHand, True)

    if debugMode:
        print("\nfullHouse Check")
        print("hand", orderedHand, len(orderedHand))
        print(hasPair, pairIndex)

    if hasThree and hasPair:
        return pairIndex + threeIndex
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
    # HERE: the 1 liner keeps the suit, the original strips the suit and returns just the numbers

# Orders the hand by rank, keeps the suits
def orderRank(hand: list) -> list:
    # The following line is a way to do it without touching the suits
    #hand.sort(key=lambda card: int(card[:-1]))

    # It can be done in one line with the sorted() function and a lambda function / anonymous function
    return sorted(hand, key=lambda card: int(card[:-1]))

# List of strings to list of tuples (Rank, "Suit")
def stringToTuple(hand: list) -> list:
    ranks = []; suits = []
    for card in hand:
        ranks.append(int(card[:-1]))
        suits.append(card[-1])
    return list(map(lambda rank, suit : (rank, suit), ranks, suits))
def stringToTuple2(hand: list) -> list:
    return [(int(card[:-1]), card[-1]) for card in hand]

def aceCheck(hand: list) -> bool:
    return any(ace[:-1] == "1" for ace in hand)

def evalHand(hand: list):
    scoredCards = [None] * 12
    print()
    print(hand)
    if(flush(hand)):
        print("found flush")
        hasHand["hasFlush"] = True
    if(straight(hand)):
        print("found straight")
        hasHand["hasStraight"] = True
    if(fiveOfAKind(hand)):
        print("found 5 of a kind")
        hasHand["hasFiveOfAKind"] = True
        hasHand["hasFourOfAKind"] = True
        hasHand["hasThreeOfAKind"] = True
        hasHand["hasPair"] = True
    if(fourOfAKind(hand)[0]):
        scoredCards[7] = fourOfAKind(hand)[1]
        print("found 4 of a kind")
        hasHand["hasFourOfAKind"] = True
        hasHand["hasThreeOfAKind"] = True
        hasHand["hasPair"] = True
    if(threeOfAKind(hand)[0]):
        scoredCards[3] = threeOfAKind(hand)[1]
        print("found 3 of a kind")
        hasHand["hasThreeOfAKind"] = True
        hasHand["hasPair"] = True
        if(fullHouse(hand)[0]):
            scoredCards[6] = fullHouse(hand)[1]
            print("found FullHouse")
            hasHand["hasFullHouse"] = True

    if(pair(hand)[0]):
        scoredCards[1] = pair(hand)[1]
        print("found pair")
        hasHand["hasPair"] = True
        if(twoPair(hand)[0]):
            scoredCards[2] = twoPair(hand)[1]
            print("found two pair")
            hasHand["hasTwoPair"] = True

# combo hands

    if(hasHand["hasFlush"] and hasHand["hasFiveOfAKind"]):
        print("found flush five")
        return True, scoredCards
    
    if(hasHand["hasFlush"] and hasHand["hasFullHouse"]):
        print("found flush house")
        return True, scoredCards
    
    if(hasHand["hasFiveOfAKind"]):
        print("found FiveOfAKind")
        return True, scoredCards
    
    if(hasHand["hasFlush"] and hasHand["hasStraight"]):
        print("found straight flush")
        return True, scoredCards
    
    if(hasHand["hasFlush"] or hasHand["hasStraight"] or hasHand["hasFullHouse"] or hasHand["hasTwoPair"] or
        hasHand["hasFourOfAKind"] or hasHand["hasThreeOfAKind"] or hasHand["hasPair"]):
        return True, scoredCards
    
    return False, scoredCards

def scoreHand(hand, scoredCards = None):
    # to do
    if not scoredCards: # Score all indices
        print("score all")
    else: # Only score certain indices
        print("score some")

# Evaluate the following hand:
testHands = [["5D", "6H", "9S", "7C", "8C"], ["5D", "6H", "9S", "8C", "8C"], ['11D', '7D', '6D', '10D', '6H'], ['2H', '3D', '5D', '6D', '7D'], ["8H", "3H", "9H", "7H", "11H"], ["5C", "6C", "9C", "7C", "8C"], ["13D", "6H", "9S", "7C", "8C", "11H", "5D", "6H", "1S", "7C", "12C", "11C"], ["1D", "11H", "12S", "13C", "10C"], ["1H", "1D", "1C", "1D", "1S"], ["1D", "1D", "1D", "1D", "1D"], ["5C", "6C", "9C", "7C", "8C"], ["10H", "10D", "10C", "1D", "10S"], ["1H", "1D", "1C", "1S"], ["10H", "1D", "1C", "10S", "10S"], ["10H", "11D", "1C", "7S", "10S"], ["10H", "11D", "11C", "7S", "10S"], ["2H", "1D", "2C", "10S", "1S"], ["1H", "2S", "2D", "1S", "2H"]]
testHandNames = ["ihStraight", "ihStraightFake", "ihStraight3", "ihStraight4", "ihFlush", "ihStraightFlush", "ihSuitRanking", "ihAceStraight", "ihFiveOfAKind", "ihFlushFive", "ihStraightFlush", "ihFourOfAKind", "ihFourOfAKind2", "ihThree", "ihPair", "ihTwoPair", "ihTwoPair2", "ihFullHouse"]

if 0:
    for i in range(len(testHandNames)):
        hasHand = {
            "hasPair": False,
            "hasTwoPair": False,
            "hasThreeOfAKind": False,
            "hasFullHouse": False,
            "hasFourOfAKind": False,
            "hasFiveOfAKind": False,
            "hasStraight": False,
            "hasFlush": False
            }
        print(testHandNames[i], i)
        evalHand(testHands[i])
        print("--------------------", i)

count = 0
# Test random hands until find a poker hand
if 0:
    while evalHand(generateHand()[0]) == False:
        count += 1;
        print(count)
        pass

score = 0
handAndDeck = generateHand(DEFAULT_HAND_SIZE)
hand, deck = orderRank(handAndDeck[0]), handAndDeck[1]
scoredCards = None

playedHand = []
print("In the crib playing balala")
print("Enter P followed by indices to play the hand. D for discard. E.g. p 023")
while not playedHand:
    print("Rank Order:")
    [print(f"{i}. {v}") for i, v in enumerate(hand)]
    print()
    print("Suit Order:", orderSuit(hand), len(deck))
    userInput = input().split()
    
    if (userInput[0].lower() == 'd'):
        # to do
        # unlimited discards atm to do
        discards = {int(x) for x in userInput[1]}
        hand = [j for i, j in enumerate(hand) if i not in discards]
        hand, deck = discardDraw(hand, deck, DEFAULT_HAND_SIZE)

    elif (userInput[0].lower() == 'p'):
        # to do
        # unlimited played cards atm to do
        indices = [int(x) for x in userInput[1]]
        for i in range(len(hand)):
            if i in indices:
                playedHand.append(hand[i])
        print("You played:", playedHand)
        temp, scoredCards = evalHand(playedHand)
        scoreHand(playedHand, scoredCards)
        
    else:
        print("Game Over---------------------")
        break