import random
import time
import sys

from pick import pick

import hand_functions as hf
import text_ui as ui


speeds = [0.01, 0.05, 0.075, 0.3, 0.5, 0.75, 1] #seconds
DEBUG_MODE = False

def classicJoker(state):
    state["mult"] += 4
    ui.slowPrint("Classic Joker: +4", "mult", state["currentSpeed"])
    return state


def misprintJoker(state):
    misprintMult = random.randint(0, 24)
    state["mult"] += misprintMult
    ui.slowPrint("Misprint: +" + str(misprintMult), "mult", state["currentSpeed"])
    return state


def cavendishJoker(state):
    state["XMult"] += 3
    ui.slowPrint("Cavendish: X3", "XMult", state["currentSpeed"])
    if random.randrange(0, 999) == 67:
        print("Cavendish: 1 in 1000. You lose.")
        sys.exit(0)
    return state


def lustyJoker(state):
    if state["suitCount"]["H"] > 0:
        state["mult"] += state["suitCount"]["H"] * 3
        ui.slowPrint("Lusty Joker: +" + str(state["suitCount"]["H"]) + " * 3", "mult", state["currentSpeed"])
    return state


def greedyJoker(state):
    if state["suitCount"]["D"] > 0:
        state["mult"] += state["suitCount"]["D"] * 3
        ui.slowPrint("Greedy Joker: +" + str(state["suitCount"]["D"]) + " * 3", "mult", state["currentSpeed"])
    return state


def wrathfulJoker(state):
    if state["suitCount"]["S"] > 0:
        state["mult"] += state["suitCount"]["S"] * 3
        ui.slowPrint("Wrathful Joker: +" + str(state["suitCount"]["S"]) + " * 3", "mult", state["currentSpeed"])
    return state


def gluttonousJoker(state):
    if state["suitCount"]["C"] > 0:
        state["mult"] += state["suitCount"]["C"] * 3
        ui.slowPrint("Gluttonous Joker: +" + str(state["suitCount"]["C"]) + " * 3", "mult", state["currentSpeed"])
    return state


def smileyJoker(state):
    faceCardCount = 0
    for rank in state["noSuitHand"]:
        if rank in {11, 12, 13}:
            faceCardCount += 1
    if faceCardCount > 0:
        state["mult"] += faceCardCount * 5
        ui.slowPrint("Smiley Face: +" + str(faceCardCount) + " * 5", "mult", state["currentSpeed"])
    return state


def jollyJoker(state):
    if state["hasHand"]["hasPair"]:
        ui.slowPrint("Jolly Joker: +8", "mult", state["currentSpeed"])
        state["mult"] += 8
    return state


def zanyJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        ui.slowPrint("Zany Joker: +12", "mult", state["currentSpeed"])
        state["mult"] += 12
    return state


def wilyJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        ui.slowPrint("Wily Joker: +100", "chip", state["currentSpeed"])
        state["chip"] += 100
    return state


def drollJoker(state):
    if state["hasHand"]["hasFlush"]:
        ui.slowPrint("Droll Joker: +10", "mult", state["currentSpeed"])
        state["mult"] += 10
    return state


def mysticSummitJoker(state):
    if state["rs1"].currentDiscards == 0:
        ui.slowPrint("Mystic Summit: +15", "mult", state["currentSpeed"])
        state["mult"] += 15
    return state


def halfJoker(state):
    if len(state["scoredCards"]) <= 3:
        ui.slowPrint("Half Joker: +20", "mult", state["currentSpeed"])
        state["mult"] += 20
    return state


def grosMichelJoker(state):
    state["mult"] += 15
    ui.slowPrint("Gros Michel: +15", "mult", state["currentSpeed"])
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
    ui.slowPrint(text, "mult", state["currentSpeed"])
    return state


def oddToddJoker(state):
    oddCount = 0
    for rank in state["noSuitHand"]:
        if rank % 2 == 1 and rank not in {11, 12, 13}:
            oddCount += 1
    state["chip"] += oddCount * 31
    text = "Odd Todd: +" + str(oddCount) + " * 31"
    ui.slowPrint(text, "chip", state["currentSpeed"])
    return state


def scholarJoker(state):
    for rank in state["noSuitHand"]:
        if rank == 1:
            state["mult"] += 4
            state["chip"] += 20
            ui.slowPrint("Scholar: +" + str(20) + " chips", "chip", state["currentSpeed"])
            ui.slowPrint("Scholar: +" + str(4) + " mult", "mult", state["currentSpeed"])
    return state


def acrobatJoker(state):
    if state["rs1"].currentHands == 1:
        state["XMult"] += 3
        ui.slowPrint("Acrobat: X3", "XMult", state["currentSpeed"])
    return state


def bloodstoneJoker(state):
    for _ in range(state["suitCount"]["H"] + state["suitCount"]["X"]):
        if random.randrange(2) == 1:
            state["XMult"] += 1.5
            ui.slowPrint("Bloodstone: X1.5", "XMult", state["currentSpeed"])
    return state


def arrowheadJoker(state):
    state["chip"] += state["suitCount"]["S"] * 50
    ui.slowPrint("Arrowhead: +" + str(state["suitCount"]["S"] * 50), "chip", state["currentSpeed"])
    return state


def onyxAgateJoker(state):
    state["mult"] += state["suitCount"]["C"] * 7
    ui.slowPrint("Onyx Agate: +" + str(state["suitCount"]["C"] * 7), "mult", state["currentSpeed"])
    return state


def fibonacciJoker(state):
    fibCount = 0
    for rank in state["noSuitHand"]:
        if rank in {1, 2, 3, 5, 8}:
            fibCount += 1
    state["mult"] += fibCount * 8
    ui.slowPrint("Fibonacci: +" + str(fibCount * 8), "mult", state["currentSpeed"])
    return state


def spaceJoker(state):
    if random.randrange(2) == 1:
        ui.slowPrint("Space Joker: Upgraded hand", None, state["currentSpeed"])
        state["gs1"].increaseHandLevel(state["rs1"].getHighestHandIndex())
    return state


def stuntmanJoker(state):
    state["chip"] += 250
    ui.slowPrint("Stuntman: +250", "chip", state["currentSpeed"])
    return state


def trioJoker(state):
    if state["hasHand"]["hasThreeOfAKind"]:
        state["XMult"] += 3
        ui.slowPrint("The Trio: X3", "XMult", state["currentSpeed"])
    return state


def familyJoker(state):
    if state["hasHand"]["hasFourOfAKind"]:
        state["XMult"] += 4
        ui.slowPrint("The Family: X4", "XMult", state["currentSpeed"])
    return state


def orderJoker(state):
    if state["hasHand"]["hasStraight"]:
        state["XMult"] += 3
        ui.slowPrint("The Order: X3", "XMult", state["currentSpeed"])
    return state


def tribeJoker(state):
    if state["hasHand"]["hasFlush"]:
        state["XMult"] += 2
        ui.slowPrint("The Tribe: X2", "XMult", state["currentSpeed"])
    return state


def brainstormJoker(state):
    ui.slowPrint("Brainstorm: " + str(getJokerName(state["playerJokers"][0])), None, state["currentSpeed"])
    state["playerJokers"].append(state["playerJokers"][0])
    state["brainstormRemove"] = True
    return state


def tribouletJoker(state):
    royalCount = 0
    for rank in state["noSuitHand"]:
        if rank in {12, 13}:
            royalCount += 1
    state["XMult"] += royalCount * 2
    ui.slowPrint("Triboulet: +" + str(royalCount * 2), "XMult", state["currentSpeed"])
    return state


def getJokerName(joker):
    if isinstance(joker, (list, tuple)):
        return joker[0]
    return joker

def jokerCalculation(scoreValues, playerJokers, scoredCards, rs1, gs1) -> tuple:
    time.sleep(speeds[3])
    time.sleep(speeds[3])

    state = {
        "chip": scoreValues[0],
        "mult": scoreValues[1],
        "XMult": scoreValues[2],
        "playerJokers": playerJokers,
        "scoredCards": scoredCards,
        "rs1": rs1,
        "gs1": gs1,
        "hasHand": rs1.hasHand,
        "noSuitHand": hf.removeSuits(scoredCards),
        "suitCount": hf.countSuits(scoredCards),
        "brainstormRemove": False,
        "currentSpeed": speeds[2],
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

    jokersProcced = 0

    for jokers in state["playerJokers"]:
        if jokersProcced >= 2:
            state["currentSpeed"] = speeds[1]
        if jokersProcced >= 6:
            state["currentSpeed"] = speeds[0]
        if jokersProcced >= 12:
            state["currentSpeed"] = 0.005

        jokerName = getJokerName(jokers)
        jokerFunctionName = jokerFunctions.get(jokerName)
        if jokerFunctionName is not None:
            jokersProcced += 1
            state = jokerFunctionName(state)
        elif DEBUG_MODE:
            print(jokerName)

    if state["brainstormRemove"]:
        state["playerJokers"].pop()
    return state["chip"], state["mult"], state["XMult"]

def jokerSelection(jokerState):
    currentJokerShop = jokerShop(jokerState)
    selected = []
    # tuple of strings with the joker name and description for the current joker shop
    options = tuple(map(lambda item: item[0] + " - " + item[1][0], currentJokerShop))

    while len(selected) != 3:
        title = "Select 3 jokers (press SPACE to select, ENTER to continue): "
        selected = pick(options, title, multiselect=True, min_selection_count=3)

    for i in selected:
        jokerState.playerJokers.append(currentJokerShop[i[1]])

    ui.printJokers(jokerState.playerJokers)

def jokerShop(jokerState) -> list:
    #allJokers = commonJokers | uncommonJokers | rareJokers
    currentJokerShop = []

    for i in range(8):
        #check for running out of jokers.
        if not (jokerState.commonJokers and jokerState.uncommonJokers and jokerState.rareJokers):
            jokerState.initJokerPool()
        rng = random.randrange(0, 100)
        if i < 3 or rng < 50:
            key, value = random.choice(list(jokerState.commonJokers.items()))
            del jokerState.commonJokers[key]
        elif rng > 85:
            key, value = random.choice(list(jokerState.rareJokers.items()))
            del jokerState.rareJokers[key]
        else:
            key, value = random.choice(list(jokerState.uncommonJokers.items()))
            del jokerState.uncommonJokers[key]
        currentJokerShop.append((key, value))

    return currentJokerShop

def jokerDeckApplication(js1, gs1, rs1):
    gs1.setDefaultTotals(gs1.selectedDeck)  # Set the default totals based on the selected deck
    # apply jokers that affect deck, hand
    for jokers in js1.playerJokers:
        match jokers[0]:
            case "Stuntman":
                gs1.totalValues[0] -= 2
            case "Four Fingers":
                js1.updateFourFingers()
            case "Troubadour":
                gs1.totalValues[0] += 2
                gs1.totalValues[1] -= 1
            case "Merry Andy":
                gs1.totalValues[2] += 3
                gs1.totalValues[0] -= 1
            case _:
                pass
    gs1.overflowTotals()
    # Assigns currentHands and currentDiscards to the game state's total hands, total discards
    rs1.resetRound(gs1.totalValues[1], gs1.totalValues[2])
