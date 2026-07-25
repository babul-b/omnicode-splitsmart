# OmniCode + SplitSmart 🧾

The companion repo for the 4-part Medium series **"The Ultimate Open-Source
AI Coding Stack."** It shows how to wire **OpenCode**, **OmniRoute**, and
**OpenRouter** into one cheap, resilient coding setup — and then uses that
setup to build a real little app: **SplitSmart**, a Splitwise-style expense
splitter you run from the terminal.

## The stack

| Tool | Role |
|---|---|
| **OpenCode** | The open-source AI coding agent you talk to (CLI or desktop). |
| **OpenRouter** | A hosted gateway: one API key, 300+ models, per-model billing. |
| **OmniRoute** | A self-hosted gateway that auto-routes, falls back, and compresses tokens across the providers you connect. |

## The series

1. **Part 1 — The Ultimate AI Coding Stack:** what each tool is, how they
   connect, and why the combination beats using any one alone.
2. **Part 2 — Setup & Hello World:** install all three, connect them with
   the corrected config in this repo, and fix a deliberately broken script
   to prove the setup works.
3. **Part 3 — Cost vs Performance:** the OmniRoute cost-saver combo — free
   models first, premium fallback only when needed — plus token compression
   and watching spend.
4. **Part 4 — Build SplitSmart:** build the expense splitter step by step
   with the stack, then push it to GitHub.

*(Article links go here once published.)*

## What's in this repo

```
omnicode-splitsmart/
├── .opencode/opencode.json         # points OpenCode at your local OmniRoute
├── omniroute/cost-saver-combo.json # free -> premium fallback + compression
├── prompts/splitsmart-system.md    # system prompt used to build the app
└── app/
    ├── splitsmart.py               # the finished project (Part 4)
    └── examples/hello-world.py     # the "fix the bug" test (Part 2)
```

## Quick start

```bash
# 1. Install OpenCode
npm i -g opencode-ai

# 2. Install and start OmniRoute (runs on http://localhost:20128)
npm i -g omniroute && omniroute

# 3. Copy .opencode/opencode.json into your project so OpenCode
#    routes through OmniRoute, then start it:
opencode

# 4. Try the finished app right now — no AI or keys needed:
cd app
python splitsmart.py add-member Alice
python splitsmart.py add-member Bob
python splitsmart.py add-expense --payer Alice --amount 60 --for "Groceries"
python splitsmart.py balances
python splitsmart.py settle
```

## SplitSmart commands

| Command | What it does |
|---|---|
| `add-member <name>` | Add a person to the group |
| `add-expense --payer <name> --amount <n> --for "<desc>" [--split a,b,c]` | Log an expense (splits equally across everyone if `--split` is omitted) |
| `balances` | Show each person's net balance |
| `settle` | Show the simplest set of payments to square up |
| `history` | List every logged expense |
| `reset` | Clear all data |

## License

MIT.
