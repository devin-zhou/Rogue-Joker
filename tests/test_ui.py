import os
import sys

from colorama import Fore, Back, Style

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '../src'))

import text_ui



def test_endOfCalcPrint_colours_only_label_not_newline(monkeypatch, capsys):
    monkeypatch.setattr(text_ui.time, "sleep", lambda *args, **kwargs: None)
    monkeypatch.setattr(text_ui, "slowPrint", lambda *args, **kwargs: None)

    text_ui.endOfCalcPrint(10, 2, 3)

    captured = capsys.readouterr().out
    assert "\n" + Fore.RED + Back.WHITE + "Total XMult:" + Style.RESET_ALL in captured
