import src.game as TheGame

# parallel list vs dict
hasHand = {
    "hasPair": False,       "hasTwoPair": False,
    "hasThreeOfAKind": False,   "hasFullHouse": False,
    "hasFourOfAKind": False,    "hasFiveOfAKind": False,
    "hasStraight": False,   "hasFlush": False
}


count = 0
# Test random hands until find a poker hand
if 0:
    while TheGame.evalHand(TheGame.generateHand(8)[0]) == False:
        count += 1
        print(count)

# Evaluate the following hand:
testHands = [["5D","6H","9S","7C","8C"], ["5D","6H","9S","8C","8C"], ['11D','7D','6D','10D','6H'], 
             ['2H','3D','5D','6D','7D'], ["8H","3H","9H","7H","11H"], ["5C","6C","9C","7C","8C"],
             ["1D", "11H", "12S", "13C", "10C"], ["1H", "1D", "1C", "1D", "1S"], ["1D", "1D", "1D", "1D", "1D"],
             ["5C", "6C", "9C", "7C", "8C"], ["10H", "10D", "10C", "1D", "10S"], ["1H", "1D", "1C", "1S"],
             ["10H", "1D", "11C", "10S", "10S"], ["10H", "11D", "1C", "7S", "10S"], ["10H", "11D", "11C", "7S", "10S"],
             ["2H", "1D", "2C", "10S", "1S"], ["1H", "2S", "2D", "1S", "2H"], ["1H", "2D", "3S", "10H"],
             ["2H", "10D", "2D", "2S"]]

testHandNames = ["ihStraight", "ihStraightFake", "ihStraightFake2",
                 "ihStraightFake3", "ihFlush", "ihStraightFlush",
                 "ihAceStraight", "ihFiveOfAKind", "ihFlushFive",
                 "ihStraightFlush", "ihFourOfAKind", "ihFourOfAKind2",
                 "ihThree", "ihPair", "ihTwoPair",
                 "ihTwoPair2", "ihFullHouse", "highCardAce",
                 "ThreeOfAKind"]


if 1:
    for i in range(len(testHandNames)):
        TheGame.hasHand = {
            "hasFlushFive": False, "hasFlushHouse": False,
            "hasFiveOfAKind": False, "hasStraightFlush": False,
            "hasFourOfAKind": False, "hasFullHouse": False, 
            "hasFlush": False, "hasStraight": False,
            "hasThreeOfAKind": False, "hasTwoPair": False, 
            "hasPair": False
        }
        print(i, "--------------------")
        print(testHandNames[i])
        notHighCard, scoredCards = TheGame.evalHand(testHands[i], 5)
        TheGame.scoreHand(testHands[i], scoredCards, notHighCard)

        print("")
