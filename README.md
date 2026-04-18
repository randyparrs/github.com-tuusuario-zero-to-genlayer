<img width="1234" height="205" alt="image" src="https://github.com/user-attachments/assets/f11dfe16-91ba-427e-931f-4113b5935ab7" /># From Zero to GenLayer: Building a P2P Betting Platform

A complete hands-on tutorial that takes you from zero blockchain knowledge to deploying a fully functional decentralized P2P betting dApp on GenLayer, the first Intelligent Blockchain.

---

## Table of Contents

1. What You Will Build
2. What You Will Learn
3. Understanding GenLayer Core Concepts
4. Part 1 The Intelligent Contract
5. Part 2 Running in GenLayer Studio
6. Project Structure
7. Resources

---

## What You Will Build

A trustless P2P betting platform where two parties create a bet on any real world event, each party submits their prediction, the contract fetches live web data from a provided URL when resolve_bet is called, an LLM judges who won based on the real data, and Optimistic Democracy consensus ensures the verdict is fair because multiple validators independently verify and must agree.

### Example

```
Event:    Who won the 2022 FIFA World Cup?
Creator:  Argentina won
Opponent: France won
URL:      https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_Final

Result:   Creator wins, Argentina confirmed as champion
```

---

## What You Will Learn

How to write an Intelligent Contract with the GenLayer Python SDK, how to use gl.nondet.web.get to fetch real time web data, how to use gl.nondet.exec_prompt to call an LLM, how to implement the Equivalence Principle with gl.vm.run_nondet_unsafe, and how to deploy and test in GenLayer Studio.

---

## Understanding GenLayer Core Concepts

### Intelligent Contracts

Smart contracts that can access the internet and call AI models, making them capable of resolving real world events trustlessly.

### Optimistic Democracy

Multiple validators independently execute the contract. A transaction is only finalized when validators reach consensus, ensuring no single node can manipulate the outcome.

### Equivalence Principle

The resolve_bet function uses gl.vm.run_nondet_unsafe with a leader function and a validator function. The leader fetches web data and calls the LLM to determine the winner. The validator independently re-runs the same process. Results are equivalent if winner_label matches exactly as creator, opponent, or draw.

---

## Part 1 The Intelligent Contract

The core of the platform is contracts/p2p_betting.py.

### Key Functions

create_bet is a write function that creates a new bet between two parties.

resolve_bet is a write function that fetches web data and has the AI judge the winner.

get_bet is a view function that checks bet status and result.

get_bet_count is a view function that shows total bets created.

get_platform_summary is a view function that shows a platform overview.

### Equivalence Principle Implementation

```python
def leader_fn():
    response = gl.nondet.web.get(resolution_url)
    event_data = response.body.decode("utf-8")[:3000]
    result = gl.nondet.exec_prompt(prompt)
    return json.dumps({"winner_label": "creator", "reasoning": "..."}, sort_keys=True)

def validator_fn(leader_result) -> bool:
    if not isinstance(leader_result, gl.vm.Return):
        return False
    validator_raw = leader_fn()
    return leader_data["winner_label"] == validator_data["winner_label"]

result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
```

---

## Part 2 Running in GenLayer Studio

Go to GenLayer Studio at https://studio.genlayer.com and create a new file called p2p_betting.py. Paste the contract code from contracts/p2p_betting.py. Set execution mode to Normal Full Consensus. Deploy with your Studio address as owner_address.

Note: the contract in this repository uses the Address type in the constructor as required by genvm-lint. When deploying in GenLayer Studio use a version that receives str in the constructor and converts internally with Address(owner_address) since Studio requires primitive types to parse the contract schema correctly.

### Create and Resolve a Bet

Step 1: create_bet

Set opponent_address to your Studio address, event_description to Who won the 2022 FIFA World Cup, creator_prediction to Argentina won the 2022 FIFA World Cup, opponent_prediction to France won the 2022 FIFA World Cup, and resolution_url to https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_Final.

Step 2: resolve_bet with bet_id set to 0.

Step 3: get_bet with bet_id set to 0 to see the result showing Resolved true, Winner creator, and the reasoning confirming Argentina.

Note: the contract in this repository uses the Address type in the constructor as required by genvm-lint. When deploying in GenLayer Studio use a version that receives str in the constructor and converts internally with Address(owner_address) since Studio requires primitive types to parse the contract schema correctly.

---

## Project Structure

```
zero-to-genlayer/
├── contracts/
│   └── p2p_betting.py
└── README.md
```

---

## Resources

GenLayer Docs: https://docs.genlayer.com

Optimistic Democracy: https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy

Equivalence Principle: https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/equivalence-principle

GenLayer Studio: https://studio.genlayer.com

Discord: https://discord.gg/8Jm4v89VAu

X Twitter: https://x.com/GenLayer




