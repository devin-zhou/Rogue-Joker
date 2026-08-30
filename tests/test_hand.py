# pylint: skip-file

import os
import sys
#import pytest

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '../src'))
import data
from game import main, scoreHand
from hand_functions import evalHand
import states


# todo to do joker eval tests


#test_seeded_mode
def seeded_mode():
    # Run the game with a forced seed
    main(forcePlayerJokers = None, forcedSeed=1)

def test_evalHand_straight():
    # Returns True if any Poker Hands are found, returns False for High Card,
    # a DICT with all the found hand types as keys with True/False as values
    # and a LIST containing the indices of the SCORED cards for partial hand types (high card, pair, etc)
    hand = ["10H", "11D", "12S", "13C", "1H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] is True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_straight_fourFingers():
    hand = ["3H", "10H", "11D", "12S", "13C"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [1, 2, 3, 4], f"Expected [1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] is True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_straight_fourFingers():
    hand = ["3H", "10H", "11D", "12S", "13C"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [1, 2, 3, 4], f"Expected [1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] is True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_flush():
    hand = ["1H", "9H", "11H", "5H", "7H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[5] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[5]}"
    assert foundHands["hasFlush"] is True, f"Expected True for Flush, got {foundHands['hasFlush']}"

def test_evalHand_flush_fourFingers():
    hand = ["1H", "9H", "11H", "5H", "1D"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[5] == [0, 1, 2, 3], f"Expected [0, 1, 2, 3] for partialHandIndices, got {partialHandIndices[5]}"
    assert foundHands["hasFlush"] is True, f"Expected True for Flush, got {foundHands['hasFlush']}"

def test_evalHand_twoPair():
    hand = ["1H", "1D", "9H", "9D", "7H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[2] == [0, 1, 2, 3], f"Expected [0, 1, 2, 3] for partialHandIndices, got {partialHandIndices[2]}"
    assert foundHands["hasTwoPair"] is True, f"Expected True for Two Pair, got {foundHands['hasTwoPair']}"
    
def test_evalHand_fullHouse():
    hand = ["1H", "1D", "1C", "9H", "9D"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[6] == [3, 4, 0, 1, 2], f"Expected [3, 4, 0, 1, 2] for partialHandIndices, got {partialHandIndices[6]}"
    assert foundHands["hasFullHouse"] is True, f"Expected True for Full House, got {foundHands['hasFullHouse']}"
    
def test_evalHand_fullHouse2():
    hand = [ "2D", "2D", "10C", "10D", "10C",]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[6] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[6]}"
    assert foundHands["hasFullHouse"] is True, f"Expected True for Full House, got {foundHands['hasFullHouse']}"

# Negative Tests
def test_evalHand_highCard():
    hand = ["2H", "9D", "11S", "5C", "7H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is False, f"Expected False for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[0] == [4], f"Expected [4] for partialHandIndices, got {partialHandIndices[0]}"
    assert all(foundHands.values()) is False, f"Expected False for High Card, got {all(foundHands.values())}"

# Secret Hands
# 0 5OAK
def test_evalHand_fiveOfAKind(secretPokerHands):
    hand = secretPokerHands[0]
    assert hand == ['1S', '1H', '1H', '1C', '1D']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[9] == None, f"Expected None for partialHandIndices, got {partialHandIndices[9]}"
    assert foundHands["hasFiveOfAKind"] is True, f"Expected True for Five of a Kind, got {foundHands['hasFiveOfAKind']}"
# 1 Flush House
def test_evalHand_flushHouse(secretPokerHands):
    hand = secretPokerHands[1]
    assert hand == ['7D', '7D', '7D', '4D', '4D']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[10] == None, f"Expected None for partialHandIndices, got {partialHandIndices[10]}"
    assert foundHands["hasFlushHouse"] is True, f"Expected True for Flush House, got {foundHands['hasFlushHouse']}"
# 2 Flush Five
def test_evalhand_flushFive(secretPokerHands):
    hand = secretPokerHands[2]
    assert hand == ['1S', '1S', '1S', '1S', '1S']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 5)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[11] == None, f"Expected None for partialHandIndices, got {partialHandIndices[11]}"
    assert foundHands["hasFlushFive"] is True, f"Expected True for Flush Five, got {foundHands['hasFlushFive']}"
# 3 Flush House Four Fingers
def test_evalHand_flushHouse_fourFingers(secretPokerHands):
    hand = secretPokerHands[3]
    assert hand == ['1D', '1D', '1D', '2D', '2H']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[10] == None, f"Expected None for partialHandIndices, got {partialHandIndices[10]}"
    assert foundHands["hasFlushHouse"] is True, f"Expected True for Flush House, got {foundHands['hasFlushHouse']}"
# 4 Flush Five Four Fingers
def test_evalhand_flushFive_fourFingers(secretPokerHands):
    hand = secretPokerHands[4]
    assert hand == ['10C', '10S', '10S', '10S', '10S']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[11] == None, f"Expected None for partialHandIndices, got {partialHandIndices[11]}"
    assert foundHands["hasFlushFive"] is True, f"Expected True for Flush Five, got {foundHands['hasFlushFive']}"
# 5 Flush House Four Fingers Wild Card
def test_evalhand_flushFive_fourFingers_wildCard(secretPokerHands):
    hand = secretPokerHands[5]
    assert hand == ['1D', '1D', '1D', '2X', '2H']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[10] == None, f"Expected None for partialHandIndices, got {partialHandIndices[10]}"
    assert foundHands["hasFlushHouse"] is True, f"Expected True for Flush House, got {foundHands['hasFlushHouse']}"
# 6 Flush Five Four Fingers Wild Card
def test_evalhand_flushFive_fourFingers_wildCard(secretPokerHands):
    hand = secretPokerHands[6]
    assert hand == ['10C', '10S', '10X', '10S', '10S']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[11] == None, f"Expected None for partialHandIndices, got {partialHandIndices[11]}"
    assert foundHands["hasFlushFive"] is True, f"Expected True for Flush Five, got {foundHands['hasFlushFive']}"
# 7 Flush Five Four Fingers ALL Wild Card
def test_evalhand_flushFive_fourFingers_allWildCard(secretPokerHands):
    hand = secretPokerHands[7]
    assert hand == ['12X', '12X', '12X', '12X', '12X']
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, data.getHasHand(), 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[11] == None, f"Expected None for partialHandIndices, got {partialHandIndices[11]}"
    assert foundHands["hasFlushFive"] is True, f"Expected True for Flush Five, got {foundHands['hasFlushFive']}"


# straightFlush_fourFingers all cards scored
def test_evalHand_scoreHand_straightFlush_fourFingers(straightFlush_fourFingers):
    hand, playerJokers = straightFlush_fourFingers
    rs1 = states.RoundState(currentHands = 1, currentDiscards = 1, hasHand = data.getHasHand())
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, rs1.hasHand, 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    #[None, None, None, None, [0, 1, 2, 3], [0, 1, 2, 3], None, None, NONE, None, None, None]
    #[None, None, None, None, [0, 1, 2, 3], [0, 1, 2, 3], None, None, {0, 1, 2, 3, 4}, None, None, None]
    assert partialHandIndices[8] == {0, 1, 2, 3, 4}, f"Expected {{0, 1, 2, 3, 4}} for partialHandIndices, got {partialHandIndices[8]}"
    assert foundHands["hasStraightFlush"] is True, f"Expected True for Straight Flush, got {foundHands['hasStraightFlush']}"
        # this hand scores 127 * 8 = 1016
    chip, mult, XMult, hand = scoreHand(hand, partialHandIndices, foundMultiCardHand, 4, data.chipMultTable, rs1)
    assert chip == 127, f"Expected 127 for chip, got {chip}"
    assert mult == 8, f"Expected 8 for mult, got {mult}"
    assert XMult == 1, f"Expected 1 for XMult, got {XMult}"
    assert hand == ["1H", "2H", "3H", "4D", "7H"], f"Expected ['1H', '2H', '3H', '4D', '7H'] for hand, got {hand}"
    # to do todo: addd joker calc

    

# straightFlush_fourFingers only 4 cards scored
def test_evalHand_straightFlush_fourFingers_2():
    hand = ["4H", "5H", "6H", "7H", "1C"]
    hasHand = data.getHasHand()
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, hasHand, 4)
    assert foundMultiCardHand is True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[8] == {0, 1, 2, 3}, f"Expected {{0, 1, 2, 3}} for partialHandIndices, got {partialHandIndices[8]}"
    assert foundHands["hasStraightFlush"] is True, f"Expected True for Straight Flush, got {foundHands['hasStraightFlush']}"
