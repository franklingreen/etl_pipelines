import datetime
import inspect
import os
import sys
import warnings
from dataclasses import dataclass
from typing import Optional, Tuple, Any

import pandas as pd
import tabulate as tb

from system.utils.printer_utils import Color


def timestamp() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def colored(text: str, color: Color) -> str:
    return f"{color}{text}{Color.RESET}"


@dataclass
class Now:
    process: str
    script: str

    def __post_init__(self):
        self.process = self.process.upper()
        self.script = self.script.upper()

    def _prefix(self) -> str:
        return (
            f"{Color.BOLD}{Color.CYAN}{timestamp()}{Color.RESET} - "
            f"{colored(self.process, Color.BLUE)} » {colored(self.script, Color.BLUE)} -"
        )

    def _format(self, color: Color, *msg: str) -> str:
        return f"{self._prefix()} {colored(' '.join(msg), color)}"

    # --- printing API ---
    def print_info(self, *msg: str, color: Optional[Color] | None = None) -> None:
        if color:
            print(self._format(color, *msg))
        else:
            print(self._format(Color.NONE, *msg))

    def print_success(self, *msg: str) -> None:
        print(self._format(Color.GREEN, *msg))

    def print_warning(self, *msg: str) -> None:
        print(self._format(Color.RED, *msg))

    # alias
    def print(self, *msg: str) -> None:
        self.print_info(*msg)

    def pprint(self, obj: Any) -> None:
        print(self._prefix())
        from pprint import pprint
        pprint(obj)

    def print_current_line(self, do_print: bool = True) -> Optional[str]:
        frame = inspect.currentframe().f_back
        line = frame.f_lineno
        result = f"line: {line}"
        if do_print:
            self.print_info(result, color=Color.MAGENTA)
            return None
        return result

    def print_caller(self, do_print: bool = True) -> Optional[Tuple[str, str]]:
        if sys.version_info >= (3, 11):
            warnings.warn("print_caller is not implemented for Python >= 3.11")
            return None

        caller = inspect.stack()[1]
        func = caller.function
        file = os.path.basename(caller.filename)

        if do_print:
            print(self._prefix(), f"caller: {func}, file: {file}")
            return None
        return func, file


class DataFramePrint:
    @staticmethod
    def format(df: pd.DataFrame, length: int = 100) -> str:
        return tb.tabulate(df.head(length), headers="keys", tablefmt="psql")

    @staticmethod
    def print(df: pd.DataFrame, length: int = 100) -> None:
        print(DataFramePrint.format(df, length))


class ProgressBarPrint:
    utf_8s = ["█", "▏", "▎", "▍", "▌", "▋", "▊", "█"]

    def __init__(self, bar_width: int = 60, title: str = "", print_perc: bool = True):
        self.bar_width = bar_width
        self.title = title
        self.print_perc = print_perc
        self.max_ticks = bar_width * 8

    def _compute_bar(self, step: int, total: int) -> str:
        total = max(total, 1)
        perc = min(100.0, 100 * step / total)

        num_ticks = int(round(perc / 100 * self.max_ticks))
        full = num_ticks // 8
        partial = num_ticks % 8

        bar = self.utf_8s[0] * full
        if partial > 0:
            bar += self.utf_8s[partial]

        bar += "▒" * int(self.bar_width - len(bar))

        prefix = f"{self.title}: " if self.title else ""
        bar_colored = f"\x1b[0;32m{bar}\x1b[0m"

        if self.print_perc:
            bar_colored += f" {perc:6.2f} %"

        return prefix + bar_colored

    def print(self, step: int, total_steps: int) -> None:
        bar = self._compute_bar(step, total_steps)
        end = "\n" if step >= total_steps else ""
        sys.stdout.write("\r" + bar + end)
        sys.stdout.flush()


if __name__ == "__main__":
    printer = Now("process", "script")
    printer.print_info("hello world")
    printer.print_success("hello world")
    printer.print_warning("hello world")
    printer.print_current_line()