# 🎲 From Zero to GenLayer: Building a P2P Betting Platform

> A complete hands-on tutorial that takes you from zero blockchain knowledge to deploying a fully functional decentralized P2P betting dApp on GenLayer — the first Intelligent Blockchain.

![GenLayer](https://img.shields.io/badge/GenLayer-Intelligent%20Contract-00c896?style=for-the-badge)
![Type](https://img.shields.io/badge/Type-Tutorial-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-green?style=for-the-badge)

---

## 📋 Table of Contents

1. [What You Will Build](#what-you-will-build)
2. [What You Will Learn](#what-you-will-learn)
3. [Understanding GenLayer's Core Concepts](#understanding-genlayers-core-concepts)
4. [Part 1 — The Intelligent Contract](#part-1--the-intelligent-contract)
5. [Part 2 — Running in GenLayer Studio](#part-2--running-in-genlayer-studio)
6. [Project Structure](#project-structure)
7. [Resources](#resources)

---

## What You Will Build

A trustless **P2P betting platform** where:

- Two parties create a bet on any real-world event
- Each party submits their prediction
- When `resolve_bet()` is called, the contract **fetches live web data** from a provided URL
- An **LLM judges** who won based on the real data
- **Optimistic Democracy consensus** ensures the verdict is fair — multiple validators independently verify and must agree

### Example

```
Event:    "Who won the 2022 FIFA World Cup?"
Creator:  "Argentina won"
Opponent: "France won"
URL:      https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_Final

Result:   Creator wins — Argentina confirmed as champion ✅
```

---

## What You Will Learn

- How to write an **Intelligent Contract** with the GenLayer Python SDK
- How to use `gl.nondet.web.get` to fetch real-time web data
- How to use `gl.nondet.exec_prompt` to call an LLM
- How to implement the **Equivalence Principle** with `gl.vm.run_nondet_unsafe`
- How to deploy and test in **GenLayer Studio**

---

## Understanding GenLayer's Core Concepts

### Intelligent Contracts
Smart contracts that can access the internet and call AI models — making them capable of resolving real-world events trustlessly.

### Optimistic Democracy ✅
Multiple validators independently execute the contract. A transaction is only finalized when validators reach consensus — ensuring no single node can manipulate the outcome.

### Equivalence Principle ✅
The `resolve_bet` function uses `gl.vm.run_nondet_unsafe(leader_fn, validator_fn)`:
- **Leader** fetches web data + calls LLM to determine the winner
- **Validator** independently re-runs the same process
- Results are equivalent if `winner_label` matches exactly (creator/opponent/draw)

---

## Part 1 — The Intelligent Contract

The core of the platform is `contracts/p2p_betting.py`.

### Key Functions

| Function | Type | Description |
|----------|------|-------------|
| `create_bet` | write | Create a new bet between two parties |
| `resolve_bet` | write | Fetch web data + AI judges the winner ✅ |
| `get_bet` | view | Check bet status and result |
| `get_bet_count` | view | Total bets created |
| `get_platform_summary` | view | Platform overview |

### Equivalence Principle Implementation

```python
def leader_fn():
    # Fetch live web data
    response = gl.nondet.web.get(resolution_url)
    event_data = response.body.decode("utf-8")[:3000]
    # LLM determines the winner
    result = gl.nondet.exec_prompt(prompt)
    return json.dumps({"winner_label": "creator", "reasoning": "..."}, sort_keys=True)

def validator_fn(leader_result) -> bool:
    if not isinstance(leader_result, gl.vm.Return):
        return False
    validator_raw = leader_fn()  # Re-run independently
    # winner_label must match exactly ✅
    return leader_data["winner_label"] == validator_data["winner_label"]

result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)  # ✅
```

---

## Part 2 — Running in GenLayer Studio

### Deploy the Contract

1. Go to [GenLayer Studio](https://studio.genlayer.com)
2. Create a new file `p2p_betting.py`
3. Paste the contract code from `contracts/p2p_betting.py`
4. Set Execution Mode to **Normal (Full Consensus)**
5. Deploy with your Studio address as `owner_address`

### Create and Resolve a Bet

```
Step 1: create_bet
  opponent_address:     0xYourStudioAddress
  event_description:    Who won the 2022 FIFA World Cup?
  creator_prediction:   Argentina won the 2022 FIFA World Cup
  opponent_prediction:  France won the 2022 FIFA World Cup
  resolution_url:       https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_Final

Step 2: resolve_bet
  bet_id: 0

Step 3: get_bet
  bet_id: 0
  → Result: Resolved: true | Winner: creator | Reasoning: Argentina confirmed...
```

---

## Project Structure

```
zero-to-genlayer/
├── contracts/
│   └── p2p_betting.py      ← Intelligent Contract (GenLayer Studio)
└── README.md
```

---

## Resources

- [GenLayer Docs](https://docs.genlayer.com)
- [Optimistic Democracy](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy)
- [Equivalence Principle](https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/equivalence-principle)
- [GenLayer Studio](https://studio.genlayer.com)
- [Discord](https://discord.gg/8Jm4v89VAu)
- [X (Twitter)](https://x.com/GenLayer)

---

*Built for the GenLayer Hackathon — Educational Content track.*
