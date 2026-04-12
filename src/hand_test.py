import game

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

TEST_RANDOM = False

# Test random hands until find a poker hand
if TEST_RANDOM:
    print(list(hasHand.keys())[::-1]) # Reverse the list of keys
    count = 0
    found = False
    baseCards = game.getBaseCards()
    while found is False:
        handGen, deckGen = game.generateHand(8, baseCards)
        handGen = game.orderRank(handGen)
        print(handGen)
        x = game.evalHand(handGen, 5)
        print(x)
        if x[0] is True:
            found = True
        count += 1
        print(count)

# Evaluate the following hand:
testHands = [["5D","6H","9S","7C","8C"],    ["5D","6H","9S","8C","8C"], ['11D','7D','6D','10D','6H'], # 0-2
             ['2H','3D','5D','6D','7D'],    ["8H","3H","9H","7H","11H"], ["5C","6C","9C","7C","8C"], # 3-5
             ["1D", "11H", "12S", "13C", "10C"], ["1H", "1D", "1C", "1D", "1S"], ["1D", "1D", "1D", "1D", "1D"], # 6-8
             ["5C", "6C", "9C", "7C", "8C"], ["10H", "10D", "10C", "1D", "10S"], ["1H", "1D", "1C", "1S"], # 9-11
             ["10H", "1D", "11C", "10S", "10S"], ["10H", "11D", "1C", "7S", "10S"], ["10H", "11D", "11C", "7S", "10S"], # 12-14
             ["2H", "1D", "2C", "10S", "1S"], ["1H", "2S", "2D", "1S", "2H"], ["1H", "2D", "3S", "10H"], # 15-17
             ["2H", "10D", "2D", "2S"], ["10D", "2D", "2S"], ['1D', '2D', '1X', '10D', '5D'], # 18-20
             ['2D', '4X', '1X', '12X', '3D'], ['1X', '1X', '1X', '12X', '7X'], ['5D', '7H', '8H', '11H', '12H'], #21-23
             ['1X', '1X', '1D', '12H', '7X'], ['1D', '1X', '1D', '12D'], ['10X', '11X', '1X', '12X']] # 24-26

testHandNames = ["ihStraight", "ihStraightFake", "ihStraightFake2",
                 "ihStraightFake3", "ihFlush", "ihStraightFlush",
                 "ihAceStraight", "ihFiveOfAKind", "ihFlushFive",
                 "ihStraightFlush", "ihFourOfAKind", "ihFourOfAKind2",
                 "ihThree", "ihPair", "ihTwoPair",
                 "ihTwoPair2", "ihFullHouse", "highCardAce",
                 "ThreeOfAKind", "ihPair", "Wild Card Flush",
                 "Wild Card Flush 2", "Wild Card Flush 3", "Four Fingers Flush",
                 "Four Fingers Flush Wild Card", "Four Fingers Flush Wild Card 2", "Four Fingers Flush Wild Card 3"]


if not TEST_RANDOM:
    fourFingers = 5 # off
    for i in range(len(testHandNames)):
        # Reset hasHand for each test case
        hasHand = game.getHasHand()
        chipMultTable = game.getChipMultTable()

        if testHandNames[i] == "Four Fingers Flush":
            fourFingers = 4 # on

        hand = game.orderRank(testHands[i])
        print(i, "-", hand)
        print("Test Case:", testHandNames[i])
        notHighCard, partiaHandIndices, _ = game.evalHand(hand, fourFingers)

        print("Result:")
        game.scoreHand(hand, partiaHandIndices, notHighCard, fourFingers, chipMultTable, hasHand)

        print("\n")
