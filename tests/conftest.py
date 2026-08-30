# tests/conftest.py

import pytest

@pytest.fixture
def tingus():
    pass

@pytest.fixture
def straightFlushFourFingers():
    hand = ["1H", "2H", "3H", "4D", "7H"]
    playerJokers = ["Four Fingers"]
    return hand, playerJokers

@pytest.fixture
def secretPokerHands():
    return [
            ['1S', '1H', '1H', '1C', '1D'], # 0 5OAK
            ['7D', '7D', '7D', '4D', '4D'], # 1 Flush House
            ['1S', '1S', '1S', '1S', '1S'], # 2 Flush Five
            ['1D', '1D', '1D', '2D', '2H'], # 3 Flush House Four Fingers
            ['10C', '10S', '10S', '10S', '10S'], # 4 Flush Five Four Fingers
            ['1D', '1D', '1D', '2X', '2H'], # 5 Flush House Four Fingers Wild Card
            ['10C', '10S', '10X', '10S', '10S'], # 6 Flush Five Four Fingers Wild Card
            ['12X', '12X', '12X', '12X', '12X'], # 7 Flush Five Four Fingers ALL Wild Card
        ]
