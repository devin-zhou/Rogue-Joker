import os
import sys
import pytest

here = os.path.dirname(__file__)

sys.path.append(os.path.join(here, '../src'))

from game import evalHand, getHasHand, main


@pytest.fixture
def straightFlush_fourFingers():
    hand = ["1H", "2H", "3H", "4D", "7H"]
    playerJokers = ["Four Fingers"]
    return hand, playerJokers

#test_seeded_mode
def seeded_mode():
    # Run the game with a forced seed
    main(forcePlayerJokers = None, forcedSeed=1)

    # Check that the expected output is produced (this will depend on the specific behavior of the game with the given seed)
    # For example, you might check that certain jokers are drawn or that the discard pile has a specific state after running the game.

def test_evalHand_straight():
    # Returns True if any Poker Hands are found, returns False for High Card,
    # a DICT with all the found hand types as keys with True/False as values
    # and a LIST containing the indices of the SCORED cards for partial hand types (high card, pair, etc)
    hand = ["10H", "11D", "12S", "13C", "1H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 5)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] == True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_straight_fourFingers():
    hand = ["3H", "10H", "11D", "12S", "13C"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 4)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [1, 2, 3, 4], f"Expected [1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] == True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_straight_fourFingers():
    hand = ["3H", "10H", "11D", "12S", "13C"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 4)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[4] == [1, 2, 3, 4], f"Expected [1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[4]}"
    assert foundHands["hasStraight"] == True, f"Expected True for Straight, got {foundHands['hasStraight']}"

def test_evalHand_flush():
    hand = ["1H", "9H", "11H", "5H", "7H"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 5)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[5] == [0, 1, 2, 3, 4], f"Expected [0, 1, 2, 3, 4] for partialHandIndices, got {partialHandIndices[5]}"
    assert foundHands["hasFlush"] == True, f"Expected True for Flush, got {foundHands['hasFlush']}"

def test_evalHand_flush_fourFingers():
    hand = ["1H", "9H", "11H", "5H", "1D"]
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 4)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    assert partialHandIndices[5] == [0, 1, 2, 3], f"Expected [0, 1, 2, 3] for partialHandIndices, got {partialHandIndices[5]}"
    assert foundHands["hasFlush"] == True, f"Expected True for Flush, got {foundHands['hasFlush']}"

def test_evalHand_straightFlush_fourFingers(straightFlush_fourFingers):
    hand, playerJokers = straightFlush_fourFingers
    foundMultiCardHand, partialHandIndices, foundHands = evalHand(hand, getHasHand(), 4)
    assert foundMultiCardHand == True, f"Expected True for foundMultiCardHand, got {foundMultiCardHand}"
    #[None, None, None, None, [0, 1, 2, 3], [0, 1, 2, 3], None, None, NONE, None, None, None]
    #[None, None, None, None, [0, 1, 2, 3], [0, 1, 2, 3], None, None, {0, 1, 2, 3, 4}, None, None, None]
    assert partialHandIndices[8] == {0, 1, 2, 3, 4}, f"Expected {{0, 1, 2, 3, 4}} for partialHandIndices, got {partialHandIndices[8]}"
    assert foundHands["hasStraightFlush"] == True, f"Expected True for Straight Flush, got {foundHands['hasStraightFlush']}"

def test_scoreHand_straightFlush_fourFingers(straightFlush_fourFingers):
    hand, playerJokers = straightFlush_fourFingers
    # this hand scores 127 * 8 = 1016
    pass
