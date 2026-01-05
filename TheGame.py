import random
import copy
import random
import time
import os
import sys

from colorama import Fore, Back, Style

chipMultTable = [
  [160, 16, 50, 3, 1], # flush five
  [140, 14, 40, 4, 1], # flush house
  [120, 12, 35, 3, 1], # five of a kind
  [100,  8, 40, 4, 1], # Straight Flush
  [ 60,  7, 30, 3, 1], # four of a kind
  [ 40,  4, 25, 2, 1], # full house
  [ 35,  4, 15, 2, 1], # flush
  [ 30,  4, 30, 3, 1], # straight
  [ 30,  3, 20, 2, 1], # three of a kind
  [ 20,  2, 20, 1, 1], # two pair
  [ 10,  2, 15, 1, 1], # pair
  [  5,  1, 10, 1, 1]  # high card
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
    "Even Steven": ["Played cards with even rank give +4 Mult when scored (10, 8, 6, 4, 2)"],
    "Odd Todd": ["Played cards with odd rank give +31 Chips when scored (A, 9, 7, 5, 3)"],
    "Scholar": ["Played Aces give +20 Chips and +4 Mult when scored"]
}
# name, desc, + Chips, + Mult, X Mult, rarity, cost, sell_cost, counter (scaling)

# sell_cost = math.max(1, math.floor(cost/2))

uncommonJokers = {
    "Four Fingers": ["All Flushes and Straights can be made with 4 cards"],
    "Acrobat": ["X3 Mult on final hand of round"],
    "Bloodstone": ["1 in 2 chance for played cards with Heart suit to give X1.5 Mult when scored"],
    "Arrowhead": ["Played cards with Spade suit give +50 Chips when scored"],
    "Onyx Agate": ["Played cards with Club suit give +7 Mult when scored"],
    "Fibonacci": ["Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored"],
    "Space Joker": ["1 in 4 chance to upgrade level of played poker hand"]
}

rareJokers = {
    "Stuntman": ["+250 Chips, -2 hand size"],
    "The Trio": ["X3 Mult if played hand contains a Three of a Kind"],
    "The Family": ["X4 Mult if played hand contains a Four of a Kind"],
    "The Order": ["X3 Mult if played hand contains a Straight"],
    "The Tribe": ["X2 Mult if played hand contains a Flush"],
    "Brainstorm": ["Copies the ability of leftmost Joker"],
    "Burnt Joker": ["Upgrade the level of the first discarded poker hand each round"],
    "Triboulet": ["Played Kings and Queens each give X2 Mult when scored"]
}

allDecks = {
    "Red Deck": "+1 discard every round",
    "Blue Deck": "+1 hand every round",
    "Abandoned Deck": "No face cards in your deck",
    "Checkered Deck": "Only hearts and spades",
    "Picky Deck": "Start with the Trading Card joker",
    "Coal Deck": "Start with the Burnt Joker",
    "Green Deck": "Start with 3 random common jokers",
    "Gambler Deck": "Start with 2 random uncommon jokers",
    "High Roller Deck": "Start with a random rare joker"
}


debugMode = 0

fastMode = False
speed1 = 0.05
speed2 = 0.075
speed3 = 0.3

if fastMode:
    speed1, speed2, speed3 = 0, 0, 0



hasHand = {
    "hasFlushFive": False, "hasFlushHouse": False,
    "hasFiveOfAKind": False, "hasStraightFlush": False,
    "hasFourOfAKind": False, "hasFullHouse": False, 
    "hasFlush": False, "hasStraight": False,
    "hasThreeOfAKind": False, "hasTwoPair": False, 
    "hasPair": False
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

class Card:
    def __init__(self, rank, suit): 
        self.rank = rank
        self.suit = suit
        self.mult = 0

    def chips(self):
        if self.rank == 1:
            return 11
        elif self.rank in (11, 12, 13):
            return 10
        return self.rank
        #Enhancements: Bonus card, Mult Card, Wild Card, Glass Card, Steel Card, Stone Card, Gold Card, Lucky Card

        #Editions: Base, Foil (+50 chips), Holographic (+10 Mult), Polychrome (X1.5 Mult), Negative (+ 1 Joker Slot)

        #Seals: Gold Seal, Red Seal, Blue Seal, Purple Seal



def generateHand(handSize, baseCards) -> tuple:
    deck = copy.deepcopy(baseCards)
    random.shuffle(deck)
    return deck[0:handSize], deck[handSize:]

def drawCards(hand, deck, handSize) -> tuple:
    numNewCards = handSize - len(hand)
    return orderRank(hand + deck[0:numNewCards]), deck[numNewCards:]




def find_flush(hand: list, flushSize = 5) -> bool:
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0}

    for i in range(len(hand)):
        suitCount[hand[i][-1]] += 1

    if debugMode:
        print("\nfind_flush Check")
        print("hand", hand, "flush size:", flushSize)
        print(suitCount)
        
    return any(count >= flushSize for count in suitCount.values())

def find_straight(hand: list, straightSize = 5) -> bool:
    orderedHand = removeSuits(hand)

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
    orderedHand = removeSuits(hand)
    if debugMode:
        print("\nfind_five_of_a_kind Check")
        print("hand", orderedHand, len(orderedHand))
        print(all(orderedHand[0] == a for a in orderedHand))
    return all(orderedHand[0] == a for a in orderedHand) and len(orderedHand) == 5

def find_four_of_a_kind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)

    if debugMode:
        print("\nfind_four_of_a_kind Check")
        print("hand", orderedHand, len(orderedHand))

    if len(orderedHand) >= 4 and orderedHand[0] == orderedHand[3]:
            return True, [0, 1, 2, 3]
    if len(orderedHand) == 5 and orderedHand[1] == orderedHand[4]:
            return True, [1, 2, 3, 4]
    return False, None

# Returns FIRST 3oak found 
def find_three_of_a_kind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)
    lengthHand = len(orderedHand)

    if debugMode:
        print("\nfind_three_of_a_kind Check")
        print("hand", orderedHand, lengthHand)

    for i in range(len(orderedHand) - 2):
        if orderedHand[i] == orderedHand[i + 1] == orderedHand[i + 2]:
            return True, [i, i + 1, i + 2]
    return False, None

# Returns FIRST pair found 
def find_pair(hand: list) -> tuple:
    print(hand)
    orderedHand = removeSuits(hand)
    lengthHand = len(orderedHand)

    if debugMode:
        print("\nfind_pair Check")
        print("hand", orderedHand, lengthHand)
    
    for i in range(lengthHand - 1):
        if orderedHand[i] == orderedHand[i + 1]:
            return True, [i, i + 1]

    return False, None

def find_two_pair(hand: list) -> tuple:
    if len(hand) < 4:
        return False, None

    hasSecondPair, pairIndex2 = None, None

    hasFirstPair, pairIndex = find_pair(hand)

    if hasFirstPair:
        hand[pairIndex[0]] = "x"
        hand[pairIndex[1]] = "y"
        hasSecondPair, pairIndex2 = find_pair(hand)

    if debugMode:
        print("\nfind_two_pair Check")
        print("hand", hand, len(hand))
        print(hasFirstPair, pairIndex)
        print(hasSecondPair, pairIndex2)

    if hasFirstPair and hasSecondPair:
        return True, pairIndex + pairIndex2
    return False, None

def find_full_house(hand: list) -> tuple:
    if len(hand) < 5:
        return False, None

    hasPair, pairIndex = None, None

    hasThree, threeIndex = find_three_of_a_kind(hand)

    if hasThree:
        hand[threeIndex[0]] = "x"
        hand[threeIndex[1]] = "y"
        hand[threeIndex[2]] = "z"
        # Following works but removes them from the list permanently
        #del orderedHand[pairIndex[0]:pairIndex[1]+1]
        hasPair, pairIndex = find_pair(hand)

    if debugMode:
        print("\nfind_full_house Check")
        print("hand", hand, len(hand))
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

def removeSuits(hand):
    hand = [int(card[:-1]) for card in hand] # Removes the suit character at the end of each index
    return hand

# Orders the hand by rank, keeps the suits
def orderRank(hand: list) -> list:
    # It can be done in one line with the sorted() function and a lambda function / anonymous function
    return sorted(hand, key=lambda card: int(card[:-1]))


def aceCheck(hand: list) -> bool:
    return any(ace[:-1] == "1" for ace in hand)

# Finds the index of the input hand name from the hasHand dict
def findHighIndex(handName): 
    for i, j in enumerate(hasHand):
        if j == handName:
            return i
    return None



# Checks for multi-card hand types and stores the found hands in a dict, returns tuple (True/False if its highcard, list of lists with the indices of scored cards from partial hand types)
def evalHand(hand: list, fourFingers: int) -> tuple:
    # Resets all poker hand flags to false
    for key in hasHand:
        hasHand[key] = False

    # Stored hands types are low to high
    partiaHandIndices = [None] * 12
    # Whole Hands
    hasHand["hasFlush"] = find_flush(hand, fourFingers)
    hasHand["hasStraight"] = find_straight(hand, fourFingers)
    hasHand["hasFiveOfAKind"] = find_five_of_a_kind(hand)
    
    # Partial Hands
    hasHand["hasFourOfAKind"], partiaHandIndices[7] = find_four_of_a_kind(hand)
    hasHand["hasThreeOfAKind"], partiaHandIndices[3] = find_three_of_a_kind(hand)
    if hasHand["hasThreeOfAKind"]:
        hasHand["hasFullHouse"], partiaHandIndices[6] = find_full_house(hand)
    hasHand["hasPair"], partiaHandIndices[1] = find_pair(hand)
    if hasHand["hasPair"]:
        hasHand["hasTwoPair"], partiaHandIndices[2] = find_two_pair(hand)

    # Combo Whole Hands
    hasHand["hasFlushFive"] = hasHand["hasFlush"] and hasHand["hasFiveOfAKind"]
    hasHand["hasFlushHouse"] = hasHand["hasFlush"] and hasHand["hasFullHouse"]
    hasHand["hasStraightFlush"] = hasHand["hasFlush"] and hasHand["hasStraight"]

    if debugMode:
        print("evalHand Function")
        print(hasHand)

    foundMultiCardHand = any(hasHand.values())

    if not foundMultiCardHand: # High Card
        partiaHandIndices[0] = highCardFinder(hand, True)

    # Returns True if any Poker Hands are found, returns False for High Card
    return foundMultiCardHand, partiaHandIndices 

# 
def scoreHand(hand, partiaHandIndices, notHighCard) -> tuple:
    if debugMode: print("score HandFunction \n partiaHandIndices", partiaHandIndices)
    newPartialHand, highestHandName = None, None

    if notHighCard: 
        # Find first true value in the dict (highest scoring hand type present in hand)
        for key, value in hasHand.items():
            if value:
                highestHandName = key
                break
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + highestHandName[3:].upper() + Style.RESET_ALL, end=" ")
    else: # high card
        highestHandName = "hasHighHand"
        print(Fore.LIGHTMAGENTA_EX + Style.BRIGHT + "High Card" + Style.RESET_ALL, end=" ")

    # Check if the hand we're scoring is a partial hand or not
    partialHands = {"hasFourOfAKind":7, "hasThreeOfAKind":3,"hasTwoPair":2, "hasPair":1, "hasHighHand":0}
    if highestHandName in partialHands.keys():
        # Feed the correct partiaHandIndices index and score the respective hand indices 
        indices = partiaHandIndices[partialHands[highestHandName]]
        newPartialHand = [card for i, card in enumerate(hand) if i in indices]
        if debugMode:
            print(highestHandName)
            print(partiaHandIndices[partialHands[highestHandName]])
            print(newPartialHand)
    hand = hand if newPartialHand == None else newPartialHand

    # If highestHandName is None, set highestHandIndex to zero (high hand), else 
    highestHandIndex = 11 if highestHandName == "hasHighHand" else findHighIndex(highestHandName)
    tempChips = countChips(hand)
    chip, mult  = calculateChipMult(tempChips, highestHandIndex)
    return chip, mult, hand, highestHandName

# Counts chips given by cards from the played hand
def countChips(hand): 
    total = 0
    for card in hand:
        rank = int(card[:-1])
        if debugMode: print("rank", rank, end=" ")
        match rank:
            case 1:
                chips = 11
            case 11 | 12 | 13:
                chips = 10
            case 0: #to do todo stone cards. currently not in the game
                chips = 50
            case _:
                chips = rank
        total += chips
    if debugMode: print(", total", total)
    return total

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
    # Multiply by (chipMultTable[highestHandIndex][4] - 1) is for hand lvl scaling
    chip = cardChips + (chipMultTable[handIndex][0] + chipMultTable[handIndex][2] * (chipMultTable[handIndex][4] - 1))
    mult = chipMultTable[handIndex][1] + chipMultTable[handIndex][3] * (chipMultTable[handIndex][4] - 1)
    return chip, mult


def jokerSelection(playerJokers):
    start = len(playerJokers)
    currentJokerShop = jokerShop()
    print("Select a Joker by index")
    while len(playerJokers) < start + 3:
        printJokers(currentJokerShop, True)
        userSelection = int(input())
        if currentJokerShop[userSelection][0] not in playerJokers:
            playerJokers.append(currentJokerShop[userSelection][0])
        else:
            print("Select a DIFFERENT joker")
            time.sleep(speed1)
    printJokers(playerJokers)

def jokerShop() -> list:
    # Traverse and print joker dict with indices for input selection
    allJokers = commonJokers | uncommonJokers | rareJokers
    currentJokerShop = []

    rnglist = [0,0,0]
    for x in range(5):
        rng = random.randrange(0,100)
        if rng < 50:
            rnglist.append(0)
        elif rng > 85:
            rnglist.append(2)
        else:
            rnglist.append(1)
    for i in range(len(rnglist)):
        if rnglist[i] == 0: #common
            key, value = random.choice(list(commonJokers.items()))
            del commonJokers[key]
        elif rnglist[i] == 1: #uncommon
            key, value = random.choice(list(uncommonJokers.items()))
            del uncommonJokers[key]
        else: #rare
            key, value = random.choice(list(rareJokers.items()))
            del rareJokers[key]
        currentJokerShop.append((key,value))

    return currentJokerShop

def printJokers(jokers, shop = False):
    for j in range(len(jokers)):
        if shop: # Print Joker Shop items
            print(f'{j:<3}{jokers[j][0]:<25}{jokers[j][1][0]}')
        else: # Print the player's jokers
            print(jokers[j])
        time.sleep(speed1)

def deckSelection(selectedDeck) -> int:
    while selectedDeck == None:
        print("Select a deck by index")
        printDecks()
        selectedDeck = int(input())
    return selectedDeck

def printDecks():
    for index, (key, value) in enumerate(allDecks.items()):
        print(f'{index:<3}{key:<16}\t{value}')
        time.sleep(speed2)

def printHand(hand):
    for index, value in enumerate(hand):
        print(f"{index}.", end=" ")
        colorCard(value)
        print()
        time.sleep(speed2)

def colorCard(card):
    match card[-1]:
        case "H": 
            print(Style.BRIGHT + Fore.RED + card, end="")
        case "D":
            print(Style.BRIGHT + Fore.YELLOW + card, end="")
        case "S":
            print(Style.BRIGHT + Fore.BLUE + card, end="")
        case "C":
            print(Style.BRIGHT + Fore.GREEN + card, end="")
        case _: # wildcard modifier?
            print(Style.BRIGHT + Fore.MAGENTA + card, end="")
    print(Style.RESET_ALL, end="")

def mainLoopPrompt(goal, currentScore, currentHands, currentDiscards, printMode = 0):
    if printMode < 1:
        print("\nEnter " + Back.BLUE + Style.BRIGHT + "P" + Style.RESET_ALL + " followed by indices to play the hand. " + Back.RED 
            + Style.BRIGHT + "D" + Style.RESET_ALL + " for discard. E.g. p 023")
    if printMode < 2:
        print("Score to beat:", goal, "Current level score:", currentScore)
    if printMode < 3:
        print(f"{Fore.BLUE}Hands: {Back.BLUE}{currentHands}{Style.RESET_ALL}\t{Fore.RED}Discards: {Back.RED}{currentDiscards}{Style.RESET_ALL}")
    

def clear_console():
    # windows
    if os.name == 'nt':
        _ = os.system('cls')
    # mac linux
    else:
        _ = os.system('clear')

def slowWordPrint(word, type):
    for char in str(word):
        time.sleep(speed1)
        if type == "chip":
            print(Fore.BLUE + Style.BRIGHT + char + Style.RESET_ALL, end="", flush=True)
        elif type == "mult":
            print(Fore.RED + Style.BRIGHT + char + Style.RESET_ALL, end="", flush=True)
        else:
            print(Fore.RED + Back.WHITE + Style.BRIGHT + char + Style.RESET_ALL, end="", flush=True)
    print(end=" ")

def endJokerCalculation(chip, mult, XMult, playerJokers, currentDiscards, scoredCards):
    #to do todo: remove this testing block
    allJokers = commonJokers | uncommonJokers | rareJokers
    for i, v in enumerate(allJokers): # Gives player every joker
        playerJokers.append(v)
    
    playerJokers = ["Stuntman", "Cavendish"] #to do todo: remove

    noSuitHand = removeSuits(scoredCards)
    time.sleep(speed3)
    for jokers in playerJokers:
        match jokers:
            case "Classic Joker":
                mult += 4
                slowWordPrint("Joker: +4", "mult")
            case "Misprint":
                misprintMult = random.randint(0, 24)
                mult += misprintMult
                slowWordPrint("Misprint: +" + str(misprintMult), "mult")
            case "Cavendish":
                XMult += 3
                slowWordPrint("Cavendish: X3", "XMult")
                if random.randrange(0, 999) == 67:
                    print("Cavendish: 1 in 1000. You lose.")
                    sys.exit(0)
            case "Stuntman":
                chip += 250
                slowWordPrint("Stuntman: +250", "chip")
            case "Jolly Joker":
                if hasHand["hasPair"]:
                    slowWordPrint("Jolly Joker: +8", "mult")
                    mult += 8
            case "Zany Joker":
                if hasHand["hasThreeOfAKind"]:
                    slowWordPrint("Zany Joker: +12", "mult")
                    mult += 12
            case "Wily Joker":
                if hasHand["hasThreeOfAKind"]:
                    slowWordPrint("Wily Joker: +100", "chip")
                    chip += 100   
            case "Droll Joker":
                if hasHand["hasFlush"]:
                    slowWordPrint("Droll Joker: +10", "mult")
                    mult += 10
            case "Mystic Summit":
                if currentDiscards == 0:
                    slowWordPrint("Mystic Summit: +15", "mult")
                    mult += 15
            case "Half Joker":
                if len(scoredCards) <= 3:
                    slowWordPrint("Half Joker: +20", "mult")
                    mult += 20
            case "Gros Michel":
                mult += 15
                slowWordPrint("Gros Michel: +15", "mult")
                if random.randrange(0,10) == 5:
                    print("Gros Michel was destroyed.")
                    del playerJokers["Gros Michel"]
            case "Even Steven":
                evenCount = 0
                for i in range(len(noSuitHand)):
                    if noSuitHand[i] % 2 == 0 and noSuitHand[i] not in {11,12,13}:
                        evenCount += 1
                mult += evenCount * 4
                text = "Even Steven: +" + str(evenCount) + " * 4"
                slowWordPrint(text, "mult")
            case "Odd Todd":
                oddCount = 0
                for i in range(len(noSuitHand)):
                    if noSuitHand[i] % 2 == 1 and noSuitHand[i] not in {11,12,13}:
                        oddCount += 1
                chip += oddCount * 31
                text = "Odd Todd: +" + str(oddCount) + " * 31"
                slowWordPrint(text, "chip")
            case "Scholar":
                for i in range(len(noSuitHand)):
                    if noSuitHand[i] == 1:
                        pass
            case other:
                if debugMode: print(other)
    return chip, mult, XMult

def endOfCalcPrint(chip, mult, XMult):
    time.sleep(speed2)
    print(Fore.BLUE + "\nTotal Chips:" + Style.RESET_ALL)
    slowWordPrint(chip, "chip")

    time.sleep(speed2)
    print(Fore.RED + "\nTotal Mult:" + Style.RESET_ALL)
    slowWordPrint(mult, "mult")
    
    time.sleep(speed2)
    print(Fore.RED + Back.WHITE + "\nTotal XMult:" + Style.RESET_ALL)
    slowWordPrint(XMult, "XMult")

    time.sleep(speed1)
    print("\nHand score ",end="")
    printEquation(chip, mult, XMult)


def rainbow_text(text):
    colours = [
        Fore.RED, Fore.LIGHTRED_EX,
        Fore.YELLOW, Fore.GREEN,
        Fore.CYAN, Fore.BLUE,
        Fore.MAGENTA
    ]

    for i, char in enumerate(str(text)):
        colour = colours[i % len(colours)]
        print(colour + Style.BRIGHT + char, end='', flush=True)
        time.sleep(speed1)
    
    print(Style.RESET_ALL)  # Reset color at the end

def printEquation(chip, mult, XMult = None):
    if XMult == None:
        print(f"{Fore.BLUE+Style.BRIGHT}{chip}{Style.RESET_ALL} * {Fore.RED+Style.BRIGHT}{mult}{Style.RESET_ALL} = {Style.BRIGHT}{chip * mult}")
    else:
        print(f"{Fore.BLUE+Style.BRIGHT}{chip}{Style.RESET_ALL} * {Fore.RED+Style.BRIGHT}{mult}{Style.RESET_ALL} * {Fore.RED+Back.WHITE+Style.BRIGHT}{XMult}{Style.RESET_ALL} = {Style.BRIGHT}{chip * (mult * XMult)}")
    print(Style.RESET_ALL,end="")

def main():
    playerJokers = []
    selectedDeck = None

    dollars = 0
    totalHands, currentHands = 4, 4
    totalDiscards, currentDiscards = 3, 3
    handSize= 8

    currentLevel = 0
    requiredScores = [5000, 10000, 20000, 50000]
    score = 0

    chip, mult, XMult = 0, 0, 1

    partiaHandIndices = None
    playedHand = []
    discardPile = []
    fourFingers = 5

    baseCards = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C", # 0 - 13
		"1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "11D", "12D", "13D", # 14 - 26
		"1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
	    "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
    ]

    baseCards2 = [
        "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "11C", "12C", "13C" # 0 - 13
    ]

    # altered with a lot of 1s for testing
    baseCards1 = [
            "1C", "1C", "1C", "1C", "1C", "1C", "7C", "8C", "9C", "10C", "11C", "12C", "13C",
            "1C","1C","1C","1C","1C","1C","1C","1C","1C","1C"
        ]

    checkeredDeck = [
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 0 - 13
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S", # 14 - 26
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "11H", "12H", "13H", # 27 - 39
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "11S", "12S", "13S" # 40 - 52
        ];

    abandonedDeck = [
            "1C", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C",
            "1D", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D",
            "1H", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H",
            "1S", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S"
        ];



    clear_console()
    if not fastMode: print("""\
    ____                              _       _             
    |  _ \ ___   __ _ _   _  ___      | | ___ | | _____ _ __ 
    | |_) / _ \ / _` | | | |/ _ \  _  | |/ _ \| |/ / _ \ '__|
    |  _ < (_) | (_| | |_| |  __/ | |_| | (_) |   <  __/ |   
    |_| \_\___/ \__, |\__,_|\___|  \___/ \___/|_|\_\___|_|   
                |___/                                        
                    """)
    
    time.sleep(speed3)
    
    # deck selection 
    if not fastMode: selectedDeck = deckSelection(selectedDeck)
    else: selectedDeck = 0

    # apply new deck
    match selectedDeck:
        case 0: #red
            totalDiscards += 1
            currentDiscards = totalDiscards
        case 1: #blue
            totalHands += 1
            currentHands = totalHands
        case 2: #abandoned
            baseCards = abandonedDeck
        case 3: #checkered
            baseCards = checkeredDeck
        case 4: #picky
            playerJokers.append["Trading Card"]
            del commonJokers["Trading Card"]
        case 4: #coal
            playerJokers.append["Burnt Joker"]
            del commonJokers["Burnt Joker"]
        case 6: #green
            for i in range(3):
                key, _ = random.choice(list(commonJokers.items()))
                del commonJokers[key]
                playerJokers.append(key)
        case 7: #Gambler
            for i in range(2):
                key, _ = random.choice(list(uncommonJokers.items()))
                del uncommonJokers[key]
                playerJokers.append(key)
        case 8: #high roller
            key, _ = random.choice(list(rareJokers.items()))
            del rareJokers[key]
            playerJokers.append(key)
        case _:
            pass
    
    # Joker Selection from joker shop
    if not fastMode: jokerSelection(playerJokers)
    else: playerJokers = []

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

    time.sleep(speed3)
    # Per game Loop
    while currentLevel < len(requiredScores): 
        # Per level Loop
        while score < requiredScores[currentLevel]:
            chip, mult, XMult = 0, 0, 1

            # Check for lose condition
            if (currentHands <= 0 and score < requiredScores[currentLevel]):
                print(score, "is less than ", requiredScores[currentLevel], ".\nGame Over")
                sys.exit(0)
            
            mainLoopPrompt(requiredScores[currentLevel], score, currentHands, currentDiscards, 0)
            printHand(hand)
            print("Deck Length:", len(deck))
            userInput = input()
            userInputAction = userInput[0].lower()
            userInputCardIndex = userInput[1:].strip()
            selectedIndicesSet = {int(x) for x in userInputCardIndex}

            # Limit hand / discard size
            if len(selectedIndicesSet) > 5:
                print("Error: selected too many cards")
                mainLoopPrompt(requiredScores[currentLevel], score, currentHands, currentDiscards, 2)

            # DISCARD
            if (userInputAction == 'd' and currentDiscards > 0):
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
            elif (userInputAction == 'p'):
                currentHands -= 1
                for i in range(len(hand)):
                    if i in selectedIndicesSet:
                        playedHand.append(hand[i])
                # Sorts the inputted hand
                playedHand = orderRank(playedHand)
                print("You played:", playedHand)
                #notHighCard lets us know if it's a multi card hand thats being scored
                notHighCard, partiaHandIndices = evalHand(playedHand, fourFingers)

                scoredHandType = None # might not need this, jokers can check hasHand= {} to check if hand types are present
                chip, mult, scoredCards, scoredHandType = scoreHand(playedHand, partiaHandIndices, notHighCard)
                printEquation(chip, mult)

                chip, mult, XMult = endJokerCalculation(chip, mult, XMult, playerJokers, currentDiscards, scoredCards)
                XMult = XMult if XMult == 1 else XMult - 1

                endOfCalcPrint(chip, mult, XMult)
                score += chip * (mult * XMult)
                print("Total level Score", end=" ")
                if score > requiredScores[currentLevel]:
                    rainbow_text(score)
                else: 
                    print(score)

                #todo to do: next hand / round logic 

                keptCards = []
                for card in hand:
                    if card not in playedHand:
                        keptCards.append(card)

                hand, deck = drawCards(keptCards, deck, handSize)
                # Resets playedHand
                discardPile.append(playedHand) #todo to do discard pile
                playedHand = []
                

            elif (userInputAction == 'd' and currentDiscards == 0):
                print("Error: Out of Discards. Try Again")
            # help
            elif (userInputAction == '?'):
                print("\"q\" for quit\n\"c\" to clear text")

            # QUIT
            elif (userInputAction == 'q'):
                sys.exit(0)

            # CLEAR
            elif (userInputAction == 'c'):
                clear_console()

            else:
                clear_console()
                print("Error: Try Again")
                time.sleep(speed1)

        # Beat the current level
        if score > requiredScores[currentLevel]:
            print(score, "is greater than", requiredScores[currentLevel])
            # Reset variables for next level
            currentLevel += 1
            score = 0
            currentHands = totalHands
            currentDiscards = totalDiscards   
            #baseCards = discardPile + deck + remaining cards in hand #to do todo
            print("Press enter to continue")
            temp = input()
            print("--- LEVEL", currentLevel + 1, "---") # +1 for 0 index
            time.sleep(speed3)

    print("You win")
            

if __name__ == "__main__":
    main()