#!/usr/bin/env python3
"""
splitsmart — a tiny Splitwise-style expense splitter for the terminal.

Add the people in your group, log who paid for what, and let it work out
the simplest set of payments that squares everyone up. All data lives in a
single JSON file next to the script, so there's no database to set up.

Commands:
    python splitsmart.py add-member <name>
    python splitsmart.py add-expense --payer <name> --amount <n> --for "<desc>" [--split a,b,c]
    python splitsmart.py balances
    python splitsmart.py settle
    python splitsmart.py history
    python splitsmart.py reset

If --split is omitted, the expense is shared equally among everyone in the group.
"""

import argparse
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "splitsmart_data.json"


# ---------- storage ----------

def load_data():
    if DATA_FILE.exists() and DATA_FILE.stat().st_size > 0:
        return json.loads(DATA_FILE.read_text())
    return {"members": [], "expenses": []}


def save_data(data):
    DATA_FILE.write_text(json.dumps(data, indent=2))


# ---------- commands ----------

def add_member(data, name):
    name = name.strip()
    if not name:
        sys.exit("Member name can't be empty.")
    if name in data["members"]:
        sys.exit(f"'{name}' is already in the group.")
    data["members"].append(name)
    save_data(data)
    print(f"Added {name}. Group is now: {', '.join(data['members'])}")


def add_expense(data, payer, amount, desc, split):
    if payer not in data["members"]:
        sys.exit(f"'{payer}' isn't in the group yet. Add them with add-member first.")
    if amount <= 0:
        sys.exit("Amount must be greater than zero.")

    if split:
        participants = [s.strip() for s in split.split(",") if s.strip()]
    else:
        participants = list(data["members"])

    if not participants:
        sys.exit("No participants to split between. Add members first.")

    unknown = [p for p in participants if p not in data["members"]]
    if unknown:
        sys.exit(f"These names aren't in the group: {', '.join(unknown)}")

    data["expenses"].append({
        "payer": payer,
        "amount": round(amount, 2),
        "desc": desc,
        "participants": participants,
    })
    save_data(data)
    share = amount / len(participants)
    print(f"Logged: {payer} paid {amount:.2f} for '{desc}', "
          f"split {len(participants)} ways ({share:.2f} each).")


def compute_balances(data):
    """Net balance per person. Positive = they are owed money."""
    balances = {m: 0.0 for m in data["members"]}
    for e in data["expenses"]:
        share = e["amount"] / len(e["participants"])
        balances[e["payer"]] += e["amount"]
        for p in e["participants"]:
            balances[p] -= share
    return {m: round(b, 2) for m, b in balances.items()}


def show_balances(data):
    if not data["members"]:
        print("No members yet. Add someone with: add-member <name>")
        return
    balances = compute_balances(data)
    print("Balances (positive = owed to them, negative = they owe):")
    for m, b in sorted(balances.items(), key=lambda kv: kv[1], reverse=True):
        flag = "  is owed" if b > 0 else ("     owes" if b < 0 else "  settled")
        print(f"  {m:<12}{flag} {abs(b):>8.2f}")


def settle(data):
    """Greedy minimal settle-up: match biggest debtor to biggest creditor."""
    balances = compute_balances(data)
    debtors = sorted(([m, b] for m, b in balances.items() if b < -0.005),
                     key=lambda kv: kv[1])
    creditors = sorted(([m, b] for m, b in balances.items() if b > 0.005),
                       key=lambda kv: kv[1], reverse=True)

    if not debtors and not creditors:
        print("Everyone is settled up. Nothing to pay.")
        return

    print("Simplest way to settle up:")
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor, owed = debtors[i]
        creditor, due = creditors[j]
        pay = min(-owed, due)
        print(f"  {debtor} pays {creditor} {pay:.2f}")
        debtors[i][1] += pay
        creditors[j][1] -= pay
        if abs(debtors[i][1]) < 0.005:
            i += 1
        if abs(creditors[j][1]) < 0.005:
            j += 1


def show_history(data):
    if not data["expenses"]:
        print("No expenses logged yet.")
        return
    print("Expense history:")
    for n, e in enumerate(data["expenses"], 1):
        who = ", ".join(e["participants"])
        print(f"  {n}. {e['payer']} paid {e['amount']:.2f} for '{e['desc']}' (split: {who})")


def reset(data):
    save_data({"members": [], "expenses": []})
    print("Group reset. All members and expenses cleared.")


# ---------- cli ----------

def main():
    parser = argparse.ArgumentParser(description="A tiny Splitwise-style expense splitter.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add-member", help="Add a person to the group")
    p_add.add_argument("name")

    p_exp = sub.add_parser("add-expense", help="Log an expense")
    p_exp.add_argument("--payer", required=True, help="Who paid")
    p_exp.add_argument("--amount", required=True, type=float, help="How much")
    p_exp.add_argument("--for", dest="desc", required=True, help="What it was for")
    p_exp.add_argument("--split", help="Comma-separated names; defaults to everyone")

    sub.add_parser("balances", help="Show net balance per person")
    sub.add_parser("settle", help="Show the simplest set of payments")
    sub.add_parser("history", help="List all logged expenses")
    sub.add_parser("reset", help="Clear all data")

    args = parser.parse_args()
    data = load_data()

    if args.command == "add-member":
        add_member(data, args.name)
    elif args.command == "add-expense":
        add_expense(data, args.payer, args.amount, args.desc, args.split)
    elif args.command == "balances":
        show_balances(data)
    elif args.command == "settle":
        settle(data)
    elif args.command == "history":
        show_history(data)
    elif args.command == "reset":
        reset(data)


if __name__ == "__main__":
    main()
