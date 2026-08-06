
def removeSuits(hand):
    hand = [int(card[:-1]) for card in hand]  # Removes the suit character at the end of each index
    return hand

def countSuits(hand):
    suitCount = {"S": 0, "H": 0, "D": 0, "C": 0, "X": 0}

    for card in hand:
        suitCount[card[-1]] += 1

    return suitCount

def findFlush(hand: list, flushSize=5) -> tuple:
    suitCount = countSuits(hand)

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

    return flushFlag, indices


def findStraight(hand: list, straightSize=5) -> tuple:
    orderedHand = removeSuits(hand)  # Already sorted by rank

    # Ace Case
    # Might not work with Four Fingers
    if 1 in orderedHand and 13 in orderedHand:
        orderedHand.remove(1)
        orderedHand.append(14)

    # Sliding window check
    for i in range(len(orderedHand) - straightSize + 1):
        window = orderedHand[i : i + straightSize]

        if all(window[j] + 1 == window[j + 1] for j in range(straightSize - 1)):
            return True, list(range(i, i + straightSize))

    return False, None


def findFiveOfAKind(hand: list) -> bool:
    orderedHand = removeSuits(hand)
    return all(orderedHand[0] == a for a in orderedHand) and len(orderedHand) == 5


def findFourOfAKind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)

    if len(orderedHand) >= 4 and orderedHand[0] == orderedHand[3]:
        return True, [0, 1, 2, 3]
    if len(orderedHand) == 5 and orderedHand[1] == orderedHand[4]:
        return True, [1, 2, 3, 4]
    return False, None


# Returns FIRST 3oak found
def findThreeOfAKind(hand: list) -> tuple:
    orderedHand = removeSuits(hand)

    for i in range(len(orderedHand) - 2):
        if orderedHand[i] == orderedHand[i + 1] == orderedHand[i + 2]:
            return True, [i, i + 1, i + 2]
    return False, None


# Returns FIRST pair found
def findPair(hand: list) -> tuple:
    orderedHand = removeSuits(hand)

    for i in range(len(orderedHand) - 1):
        if orderedHand[i] == orderedHand[i + 1]:
            return True, [i, i + 1]

    return False, None


def findTwoPair(hand: list) -> tuple:
    if len(hand) < 4:
        return False, None

    hasSecondPair, pairIndex2 = None, None
    hasFirstPair, pairIndex = findPair(hand)
    tempHand = hand.copy()
    if hasFirstPair:
        tempHand[pairIndex[0]] = "100"
        tempHand[pairIndex[1]] = "200"
        hasSecondPair, pairIndex2 = findPair(tempHand)

    if hasFirstPair and hasSecondPair:
        return True, pairIndex + pairIndex2
    return False, None


def findFullHouse(hand: list) -> tuple:
    if len(hand) < 5:
        return False, None

    hasPair, pairIndex = None, None
    hasThree, threeIndex = findThreeOfAKind(hand)
    tempHand = hand.copy()
    if hasThree:
        tempHand[threeIndex[0]] = "100"
        tempHand[threeIndex[1]] = "200"
        tempHand[threeIndex[2]] = "300"
        hasPair, pairIndex = findPair(tempHand)

    if hasThree and hasPair:
        return True, pairIndex + threeIndex
    return False, None
