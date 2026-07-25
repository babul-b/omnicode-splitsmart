# System prompt — building SplitSmart

Load this into OpenCode before you start Part 4 so the agent knows exactly
how to build the project without wandering.

You are helping build **SplitSmart**, a tiny Splitwise-style expense
splitter that runs entirely in the terminal. Follow these rules:

1. **Language & deps:** Python 3, standard library only. No third-party
   packages, no framework. If you think you need a dependency, you don't.
2. **Storage:** a single JSON file next to the script. No database.
3. **Interface:** a `argparse` sub-command CLI — `add-member`,
   `add-expense`, `balances`, `settle`, `history`, `reset`.
4. **Money:** always round to 2 decimals. Never let floating-point noise
   leak into printed balances.
5. **Settle-up:** compute the *minimum* set of payments (greedy: match the
   biggest debtor to the biggest creditor, repeat).
6. **Errors:** fail loudly and clearly on unknown names, empty names,
   or non-positive amounts. A helpful one-line message, then exit.
7. **Simplicity:** keep it readable in one sitting. No premature
   abstraction, no classes unless they genuinely earn their place.
