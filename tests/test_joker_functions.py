import os
import sys
from types import SimpleNamespace

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '../src'))
#pylint: disable=wrong-import-position
import data
from joker_functions import classicJoker, jokerCalculation
#pylint: enable=wrong-import-position

def testClassicJokerHelperIncreasesMult():
    state = {
        "chip": 10,
        "mult": 1,
        "XMult": 1,
        "playerJokers": [["Classic Joker"]],
        "scoredCards": ["1H"],
        "rs1": SimpleNamespace(hasHand={"hasPair": False}, currentDiscards=0, currentHands=1),
        "gs1": SimpleNamespace(chipMultTable=[]),
        "highestHand": "pair",
        "hasHand": {"hasPair": False},
        "noSuitHand": [1],
        "suitCount": {"H": 1, "D": 0, "S": 0, "C": 0, "X": 0},
        "brainstormRemove": False,
        "currentSpeed": 0,
    }

    updatedState = classicJoker(state)

    assert updatedState["mult"] == 5
    assert updatedState["chip"] == 10
    assert updatedState["XMult"] == 1


def testJokerCalculationDispatchesClassicJoker():
    rs1 = SimpleNamespace(currentDiscards=1, currentHands=1, hasHand=data.getHasHand())
    gs1 = SimpleNamespace(chipMultTable=[])
    rs1.highestHandIndex = 11  # Set a default value for highestHandIndex

    chip, mult, XMult = jokerCalculation([10,1,1], [["Classic Joker"]], ["1H"], rs1, gs1)

    assert chip == 10
    assert mult == 5
    assert XMult == 1
