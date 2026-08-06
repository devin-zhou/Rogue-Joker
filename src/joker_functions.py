import random
import time
import sys

import hand_functions as hf
import text_ui as ui


speeds = [0.01, 0.05, 0.075, 0.3]
DEBUG_MODE = False

def classicJoker(state):
    state["mult"] += 4
    ui.slowPrint("Classic Joker: +4", "mult")
    return state


def misprintJoker(state):
    misprintMult = random.randint(0, 24)
    state["mult"] += misprintMult
    ui.slowPrint("Misprint: +" + str(misprintMult), "mult")
    return state


def cavendishJoker(state):
    state["XMult"] += 3
    ui.slowPrint("Cavendish: X3", "XMult")
    if random.randrange(0, 999) == 67:
        print("Cavendish: 1 in 1000. You lose.")
        sys.exit(0)
    return state


def lustyJoker(state):
    if state["suitCount"]["H"] > 0:
        state["mult"] += state["suitCount"]["H"] * 3
        ui.slowPrint("Lusty Joker: +" + str(state["suitCount"]["H"]) + " * 3", "mult")
    return state


def greedyJoker(state):
    if state["suitCount"]["D"] > 0:
        state["mult"] += state["suitCount"]["D"] * 3
        ui.slowPrint("Greedy Joker: +" + str(state["suitCount"]["D"]) + " * 3", "mult")
    return state


def wrathfulJoker(state):
    if state["suitCount"]["S"] > 0:
        state["mult"] += state["suitCount"]["S"] * 3
        ui.slowPrint("Wrathful Joker: +" + str(state["suitCount"]["S"]) + " * 3", "mult")
    return state


def gluttonousJoker(state):
    if state["suitCount"]["C"] > 0:
        state["mult"] += state["suitCount"]["C"] * 3
        ui.slowPrint("Gluttonous Joker: +" + str(state["suitCount"]["C"]) + " * 3", "mult")
    return state


def smileyJoker(state):
    faceCardCount = 0
    for rank in state["noSuitHand"]:
        if rank in {11, 12, 13}:
            faceCardCount += 1
    if faceCardCount > 0:
        state["mult"] += faceCardCount * 5
        ui.slowPrint("Smiley Face: +" + str(faceCardCount) + " * 5", "mult")
    return state


def jollyJoker(state):
    if state["hasHand"]["hasPair"]:
        ui.slowPrint("Jolly Joker: +8", "mult")
        state["mult"] += 8
    return state


def zanyJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        ui.slowPrint("Zany Joker: +12", "mult")
        state["mult"] += 12
    return state


def wilyJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        ui.slowPrint("Wily Joker: +100", "chip")
        state["chip"] += 100
    return state


def drollJoker(state):
    if state["hasHand"]["hasFlush"]:
        ui.slowPrint("Droll Joker: +10", "mult")
        state["mult"] += 10
    return state


def mysticSummitJoker(state):
    if state["rs1"].currentDiscards == 0:
        ui.slowPrint("Mystic Summit: +15", "mult")
        state["mult"] += 15
    return state


def halfJoker(state):
    if len(state["scoredCards"]) <= 3:
        ui.slowPrint("Half Joker: +20", "mult")
        state["mult"] += 20
    return state


def grosMichelJoker(state):
    state["mult"] += 15
    ui.slowPrint("Gros Michel: +15", "mult")
    if random.randrange(0, 10) == 5:
        print("Gros Michel was destroyed.")
        state["playerJokers"] = [joker for joker in state["playerJokers"] if getJokerName(joker) != "Gros Michel"]
    return state


def evenStevenJoker(state):
    evenCount = 0
    for rank in state["noSuitHand"]:
        if rank % 2 == 0 and rank not in {11, 12, 13}:
            evenCount += 1
    state["mult"] += evenCount * 4
    text = "Even Steven: +" + str(evenCount) + " * 4"
    ui.slowPrint(text, "mult")
    return state


def oddToddJoker(state):
    oddCount = 0
    for rank in state["noSuitHand"]:
        if rank % 2 == 1 and rank not in {11, 12, 13}:
            oddCount += 1
    state["chip"] += oddCount * 31
    text = "Odd Todd: +" + str(oddCount) + " * 31"
    ui.slowPrint(text, "chip")
    return state


def scholarJoker(state):
    for rank in state["noSuitHand"]:
        if rank == 1:
            state["mult"] += 4
            state["chip"] += 20
    return state


def acrobatJoker(state):
    if state["rs1"].currentHands == 1:
        state["XMult"] += 3
        ui.slowPrint("Acrobat: X3", "XMult")
    return state


def bloodstoneJoker(state):
    for _ in range(state["suitCount"]["H"] + state["suitCount"]["X"]):
        if random.randrange(2) == 1:
            state["XMult"] += 1.5
            ui.slowPrint("Bloodstone: X1.5", "XMult")
    return state


def arrowheadJoker(state):
    state["chip"] += state["suitCount"]["S"] * 50
    ui.slowPrint("Arrowhead: +" + str(state["suitCount"]["S"] * 50), "chip")
    return state


def onyxAgateJoker(state):
    state["mult"] += state["suitCount"]["C"] * 7
    ui.slowPrint("Onyx Agate: +" + str(state["suitCount"]["C"] * 7), "mult")
    return state


def fibonacciJoker(state):
    fibCount = 0
    for rank in state["noSuitHand"]:
        if rank in {1, 2, 3, 5, 8}:
            fibCount += 1
    state["mult"] += fibCount * 8
    ui.slowPrint("Fibonacci: +" + str(fibCount * 8), "mult")
    return state


def spaceJoker(state):
    if random.randrange(2) == 1:
        ui.slowPrint("Space Joker: Upgraded hand")
        state["gs1"].increaseHandLevel(state["highestHandIndex"])
    return state


def stuntmanJoker(state):
    state["chip"] += 250
    ui.slowPrint("Stuntman: +250", "chip")
    return state


def trioJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        state["XMult"] += 3
        ui.slowPrint("The Trio: X3", "XMult")
    return state


def familyJoker(state):
    if state["hasHand"]["hasFourOfAKind"]:
        state["XMult"] += 4
        ui.slowPrint("The Family: X4", "XMult")
    return state


def orderJoker(state):
    if state["hasHand"]["hasStraight"]:
        state["XMult"] += 3
        ui.slowPrint("The Order: X3", "XMult")
    return state


def tribeJoker(state):
    if state["hasHand"]["hasFlush"]:
        state["XMult"] += 2
        ui.slowPrint("The Tribe: X2", "XMult")
    return state


def brainstormJoker(state):
    ui.slowPrint("Brainstorm: " + str(getJokerName(state["playerJokers"][0])))
    state["playerJokers"].append(state["playerJokers"][0])
    state["brainstormRemove"] = True
    return state


def tribouletJoker(state):
    royalCount = 0
    for rank in state["noSuitHand"]:
        if rank in {12, 13}:
            royalCount += 1
    state["XMult"] += royalCount * 2
    ui.slowPrint("Triboulet: +" + str(royalCount * 2), "XMult")
    return state


def getJokerName(joker):
    if isinstance(joker, (list, tuple)):
        return joker[0]
    return joker

def jokerCalculation(chip, mult, XMult, playerJokers, scoredCards, rs1, gs1) -> tuple:
    time.sleep(speeds[3])
    time.sleep(speeds[3])

    state = {
        "chip": chip,
        "mult": mult,
        "XMult": XMult,
        "playerJokers": playerJokers,
        "scoredCards": scoredCards,
        "rs1": rs1,
        "gs1": gs1,
        "highestHandIndex": rs1.highestHandIndex,
        "hasHand": rs1.hasHand,
        "noSuitHand": hf.removeSuits(scoredCards),
        "suitCount": hf.countSuits(scoredCards),
        "brainstormRemove": False,
    }

    jokerFunctions = {
        "Classic Joker": classicJoker,
        "Misprint": misprintJoker,
        "Cavendish": cavendishJoker,
        "Lusty Joker": lustyJoker,
        "Greedy Joker": greedyJoker,
        "Wrathful Joker": wrathfulJoker,
        "Gluttonous Joker": gluttonousJoker,
        "Smiley Joker": smileyJoker,
        "Jolly Joker": jollyJoker,
        "Zany Joker": zanyJoker,
        "Wily Joker": wilyJoker,
        "Droll Joker": drollJoker,
        "Mystic Summit": mysticSummitJoker,
        "Half Joker": halfJoker,
        "Gros Michel": grosMichelJoker,
        "Even Steven": evenStevenJoker,
        "Odd Todd": oddToddJoker,
        "Scholar": scholarJoker,
        "Acrobat": acrobatJoker,
        "Bloodstone": bloodstoneJoker,
        "Arrowhead": arrowheadJoker,
        "Onyx Agate": onyxAgateJoker,
        "Fibonacci": fibonacciJoker,
        "Space Joker": spaceJoker,
        "Stuntman": stuntmanJoker,
        "The Trio": trioJoker,
        "The Family": familyJoker,
        "The Order": orderJoker,
        "The Tribe": tribeJoker,
        "Brainstorm": brainstormJoker,
        "Triboulet": tribouletJoker,
    }

    for jokers in state["playerJokers"]:
        jokerName = getJokerName(jokers)
        jokerFunctionName = jokerFunctions.get(jokerName)
        if jokerFunctionName is not None:
            state = jokerFunctionName(state)
        elif DEBUG_MODE:
            print(jokerName)

    if state["brainstormRemove"]:
        state["playerJokers"].pop()
    return state["chip"], state["mult"], state["XMult"]
