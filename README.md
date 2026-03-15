# 🎲 From Zero to GenLayer: Building a P2P Betting Platform

> **A complete hands-on tutorial** that takes you from zero blockchain knowledge to deploying a fully functional decentralized P2P betting dApp on GenLayer — the first Intelligent Blockchain.

---

## 📋 Table of Contents

1. [What You Will Build](#what-you-will-build)
2. [What You Will Learn](#what-you-will-learn)
3. [Understanding GenLayer's Core Concepts](#understanding-genlayers-core-concepts)
   - [What Are Intelligent Contracts?](#what-are-intelligent-contracts)
   - [Optimistic Democracy](#optimistic-democracy)
   - [The Equivalence Principle](#the-equivalence-principle)
4. [Project Architecture](#project-architecture)
5. [Prerequisites](#prerequisites)
6. [Part 1 — Setting Up GenLayer Studio](#part-1--setting-up-genlayer-studio)
7. [Part 2 — Writing the Intelligent Contract](#part-2--writing-the-intelligent-contract)
8. [Part 3 — Testing in GenLayer Studio](#part-3--testing-in-genlayer-studio)
9. [Part 4 — Building the Frontend with genlayer-js](#part-4--building-the-frontend-with-genlayer-js)
10. [Part 5 — Deploying to Testnet](#part-5--deploying-to-testnet)
11. [How Optimistic Democracy Powers This App](#how-optimistic-democracy-powers-this-app)
12. [Project Structure](#project-structure)
13. [Troubleshooting](#troubleshooting)
14. [Next Steps](#next-steps)
15. [Resources](#resources)

---

## What You Will Build

A **P2P Betting Platform** where two friends can place a trustless bet on any real-world event — a sports match, a news outcome, a crypto price — and GenLayer's Intelligent Contract automatically resolves who wins by reading live data from the Internet and reasoning about it using an LLM.

No referee. No centralized oracle. No fees to a platform. Just two wallets, a contract, and consensus.

**Live demo flow:**

```
Alice bets 10 tokens that Real Madrid wins tonight.
Bob bets 10 tokens that Barcelona wins.
After the match, anyone calls resolve_bet().
The contract fetches the live score from the web.
An LLM reasons about who won.
5 validators independently reach consensus.
The winner receives 20 tokens automatically.
```

---

## What You Will Learn

By completing this tutorial you will be able to:

- Explain what Optimistic Democracy is and why it enables non-deterministic consensus
- Explain the Equivalence Principle and how validators agree on subjective outcomes
- Use GenLayer Studio to write, simulate, and debug an Intelligent Contract
- Write a Python Intelligent Contract that fetches live web data and calls an LLM
- Build a React frontend that connects to your contract using `genlayer-js`
- Deploy a contract to the GenLayer testnet (Testnet Bradbury)

---

## Understanding GenLayer's Core Concepts

Before writing a single line of code, it's essential to understand what makes GenLayer fundamentally different from any blockchain you've worked with before.

### What Are Intelligent Contracts?

Traditional smart contracts (like Solidity on Ethereum) are **deterministic** — every node runs the same code, reads the same state, and always arrives at the same result. This is great for tokens and financial logic, but it means contracts can never:

- Read a website
- Understand natural language
- Make a judgment call
- Process anything that doesn't have a single provable answer

**Intelligent Contracts** break all of these limitations. They are smart contracts written in Python that can:

- Fetch live data from any URL on the Internet
- Call Large Language Models (LLMs) to reason about that data
- Return results that are subjective or probabilistic
- Still reach verifiable, trustless consensus through Optimistic Democracy

### Optimistic Democracy

Optimistic Democracy is GenLayer's consensus mechanism designed specifically for non-deterministic operations. Here is how it works step by step:

```
                    ┌─────────────────────────────────────┐
                    │         Transaction Submitted        │
                    └──────────────────┬──────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │  Random Validator Group Selected     │
                    │  (e.g. 5 validators)                 │
                    └──────────────────┬──────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │  Leader executes the transaction     │
                    │  (fetches web data, calls LLM)       │
                    └──────────────────┬──────────────────┘
                                       │
                    ┌──────────────────▼──────────────────┐
                    │  Other validators run their own LLMs │
                    │  and apply the Equivalence Principle  │
                    └──────────────────┬──────────────────┘
                                       │
                         ┌─────────────┴──────────────┐
                         │                            │
               ┌─────────▼────────┐        ┌─────────▼────────┐
               │ Majority agrees  │        │ Disagreement →   │
               │ → Provisionally  │        │ Appeal Process   │
               │   Accepted       │        │ (doubles voters) │
               └─────────┬────────┘        └──────────────────┘
                         │
               ┌─────────▼────────┐
               │  Finality Window │
               │  passes → Final  │
               └──────────────────┘
```

Key properties of Optimistic Democracy:

- Validators who vote incorrectly have their **staked tokens slashed**
- Validators who vote correctly **earn rewards**
- If a result is contested, the validator set **doubles** on each appeal
- The system is economically designed so honest validators always profit

### The Equivalence Principle

This is the magic that makes non-deterministic consensus possible. When a Leader validator calls an LLM and gets an answer, other validators also call their own LLMs. They don't need to get **identical** answers — they need to get **equivalent** answers.

There are two types:

**Comparative Equivalence** — used for quantifiable outputs:

```python
# Example: Bet resolution score check
# Leader says: "Real Madrid won 3-1"
# Validator 2 says: "Real Madrid won 3-1"   ✅ Identical
# Validator 3 says: "Real Madrid won 3-1"   ✅ Identical
# All agree → consensus reached
```

**Non-Comparative Equivalence** — used for qualitative outputs:

```python
# Example: Dispute text analysis
# Leader says: "Based on the evidence, Party A fulfilled the contract terms"
# Validator 2: "The documentation shows Party A completed all deliverables"
# Validator 3: "Party A met the required conditions per the agreement"
# Different words, same meaning → Validators assess if it's equivalent ✅
```

As a developer, **you define what counts as equivalent** in your contract's prompt. This is one of the most important skills you will practice in this tutorial.

---

## Project Architecture

```
p2p-betting-genlayer/
├── contracts/
│   └── p2p_betting.py          # The Intelligent Contract (Python)
├── frontend/
│   ├── src/
│   │   ├── App.jsx             # Main React component
│   │   ├── components/
│   │   │   ├── CreateBet.jsx   # Bet creation form
│   │   │   ├── ActiveBets.jsx  # List of open bets
│   │   │   └── ResolveBet.jsx  # Trigger bet resolution
│   │   └── genlayer.js         # genlayer-js client setup
│   ├── package.json
│   └── vite.config.js
├── tests/
│   └── test_betting.py         # Contract unit tests
└── README.md
```

---

## Prerequisites

Before starting, make sure you have the following installed:

- **Node.js** v18 or higher
- **Python** 3.11 or higher
- **Docker Desktop** (required for GenLayer Studio)
- A modern browser (Chrome recommended for Studio)
- Basic knowledge of Python and JavaScript/React

No prior blockchain experience is needed. This tutorial explains everything from the ground up.

---

## Part 1 — Setting Up GenLayer Studio

GenLayer Studio is a browser-based IDE that simulates the full GenLayer network locally. It runs multiple validator nodes in Docker, lets you deploy contracts, execute transactions, and watch validators reach consensus in real time.

### Step 1.1 — Install the GenLayer CLI

```bash
npm install -g @genlayer/cli
```

Verify the installation:

```bash
genlayer --version
```

### Step 1.2 — Initialize GenLayer Studio

```bash
genlayer init
```

This command pulls the Docker images for the GenLayer validator nodes and sets up your local environment. It will take a few minutes the first time.

### Step 1.3 — Start the Studio

```bash
genlayer up
```

Open your browser and navigate to `http://localhost:8080`. You should see the GenLayer Studio interface.

### Step 1.4 — Exploring the Studio

The Studio has four main panels:

**Left panel — Contract Editor**
This is where you write your Python Intelligent Contract. It has syntax highlighting and real-time error detection.

**Top right — Validators**
You can see the 5 simulated validator nodes. Each one runs a different LLM provider. In the studio you can configure which models each validator uses — this is key for understanding how the Equivalence Principle works in practice.

**Bottom right — Logs**
Every validator logs its execution in real time. When you call a transaction, you can watch each validator independently fetch web data, call its LLM, and vote on the result.

**Center — Contract State**
After deploying a contract, this panel shows the current state of all stored variables.

> **Tip:** Before moving on, click on the "Validators" tab and observe that each validator is configured with a different LLM provider (e.g., openai/gpt-4o, mistralai/mistral-large, etc.). This is intentional — the Equivalence Principle is designed to work across different models, not the same one.

---

## Part 2 — Writing the Intelligent Contract

Now we write the heart of the application: the Intelligent Contract.

### Step 2.1 — Understanding the Contract Design

Our betting contract needs to do the following:

1. Allow two parties to create a bet with a description of the event
2. Allow both parties to lock in their wager
3. When called to resolve, **fetch live data from the web** about the event outcome
4. **Ask an LLM** to reason about who won based on that data
5. Transfer the winnings to the correct party

The non-deterministic part (steps 3 and 4) is where GenLayer shines — and where the Equivalence Principle is applied.

### Step 2.2 — The Full Contract

Create a file at `contracts/p2p_betting.py`:

```python
# contracts/p2p_betting.py
# GenLayer P2P Betting Platform — Intelligent Contract
# Tutorial: From Zero to GenLayer

from genlayer import IContract, public, private
from genlayer.py.types import Address
import json


class Bet:
    """Represents a single bet between two parties."""
    def __init__(
        self,
        creator: str,
        opponent: str,
        event_description: str,
        creator_prediction: str,
        opponent_prediction: str,
        wager_amount: int,
        resolution_url: str,
    ):
        self.creator = creator
        self.opponent = opponent
        self.event_description = event_description
        self.creator_prediction = creator_prediction
        self.opponent_prediction = opponent_prediction
        self.wager_amount = wager_amount
        self.resolution_url = resolution_url
        self.creator_funded = False
        self.opponent_funded = False
        self.resolved = False
        self.winner = None
        self.resolution_reasoning = None


class P2PBetting(IContract):
    """
    A trustless P2P betting platform powered by GenLayer's Intelligent Contracts.
    
    Two parties can bet on any real-world event. When resolve_bet() is called,
    the contract fetches live data from a provided URL and uses an LLM to 
    determine the outcome — resolved through Optimistic Democracy consensus.
    """

    def __init__(self):
        # Storage: maps bet_id (str) to a Bet dict
        self.bets: dict[str, dict] = {}
        self.bet_counter: int = 0

    @public
    def create_bet(
        self,
        opponent_address: str,
        event_description: str,
        creator_prediction: str,
        opponent_prediction: str,
        resolution_url: str,
    ) -> str:
        """
        Create a new bet. The caller is the creator.
        
        Args:
            opponent_address: Wallet address of the opposing party
            event_description: Plain English description of the event 
                               (e.g., "Real Madrid vs Barcelona, March 15 2026")
            creator_prediction: What the creator is betting on
                               (e.g., "Real Madrid wins")
            opponent_prediction: What the opponent is betting on
                                (e.g., "Barcelona wins or draw")
            resolution_url: A URL where the outcome can be verified
                           (e.g., "https://www.bbc.com/sport/football")
        
        Returns:
            bet_id: A unique string ID for this bet
        """
        bet_id = str(self.bet_counter)
        self.bet_counter += 1

        caller = str(self.contract_runner.from_address)

        self.bets[bet_id] = {
            "creator": caller,
            "opponent": opponent_address,
            "event_description": event_description,
            "creator_prediction": creator_prediction,
            "opponent_prediction": opponent_prediction,
            "wager_amount": 0,
            "resolution_url": resolution_url,
            "creator_funded": False,
            "opponent_funded": False,
            "resolved": False,
            "winner": None,
            "resolution_reasoning": None,
        }

        return bet_id

    @public
    def fund_bet(self, bet_id: str) -> str:
        """
        Fund a bet by sending tokens. Both parties must fund before resolution.
        The amount sent (msg.value) is recorded as the wager.
        """
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        bet = self.bets[bet_id]
        assert not bet["resolved"], "Bet is already resolved"

        caller = str(self.contract_runner.from_address)
        value = self.contract_runner.value  # tokens sent with the transaction

        assert value > 0, "You must send tokens to fund the bet"

        if caller == bet["creator"]:
            assert not bet["creator_funded"], "Creator has already funded"
            bet["creator_funded"] = True
            bet["wager_amount"] = value
            return f"Creator funded bet {bet_id} with {value} tokens"

        elif caller == bet["opponent"]:
            assert not bet["opponent_funded"], "Opponent has already funded"
            assert value == bet["wager_amount"], (
                f"Opponent must match the creator's wager of {bet['wager_amount']} tokens"
            )
            bet["opponent_funded"] = True
            return f"Opponent funded bet {bet_id} with {value} tokens"

        else:
            raise Exception("You are not a participant in this bet")

    @public
    def resolve_bet(self, bet_id: str) -> str:
        """
        Resolve a bet by fetching live event data and asking an LLM who won.
        
        THIS IS THE INTELLIGENT PART — This method:
        1. Fetches live data from the resolution_url
        2. Asks an LLM to determine the winner based on the event description
        3. The result goes through Optimistic Democracy consensus across 5 validators
        4. Each validator independently fetches data and calls its own LLM
        5. The Equivalence Principle ensures they all reach the same conclusion
        
        This method can be called by anyone after both parties have funded.
        """
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        bet = self.bets[bet_id]

        assert not bet["resolved"], "Bet is already resolved"
        assert bet["creator_funded"] and bet["opponent_funded"], (
            "Both parties must fund the bet before it can be resolved"
        )

        # ── STEP 1: Fetch live data from the web ─────────────────────────────
        # get_webpage() is a GenLayer built-in that fetches a URL
        # Every validator will independently call this URL
        event_data = get_webpage(bet["resolution_url"], mode="text")

        # ── STEP 2: Ask an LLM to determine the winner ───────────────────────
        # This is the non-deterministic operation.
        # The Equivalence Principle in the prompt below defines what counts
        # as an "equivalent" answer across different validators' LLMs.
        
        prompt = f"""
You are an impartial judge for a P2P bet. Your task is to determine the winner.

BET DETAILS:
Event: {bet['event_description']}
Creator's prediction: {bet['creator_prediction']}
Opponent's prediction: {bet['opponent_prediction']}

LIVE DATA FROM THE WEB (fetched from {bet['resolution_url']}):
{event_data[:3000]}

INSTRUCTIONS:
Based strictly on the live data above, determine who won the bet.
You must respond ONLY with a valid JSON object in this exact format:
{{
  "winner": "<creator_address_or_opponent_address>",
  "winner_label": "<creator or opponent>",
  "reasoning": "<one sentence explaining why>"
}}

Where:
- "winner" is either "{bet['creator']}" (creator) or "{bet['opponent']}" (opponent)
- "winner_label" is either "creator" or "opponent"
- "reasoning" is a single sentence based only on the factual data provided

EQUIVALENCE NOTE: Two answers are equivalent if they identify the same winner,
regardless of exact wording in the reasoning. Focus on who the data says won.

If the data is insufficient or inconclusive, respond with:
{{"winner": "none", "winner_label": "draw", "reasoning": "Insufficient data to determine winner"}}
"""

        result_text = call_llm(prompt)

        # ── STEP 3: Parse the LLM response ───────────────────────────────────
        try:
            # Strip markdown code fences if present
            clean = result_text.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            result = json.loads(clean.strip())
        except json.JSONDecodeError:
            raise Exception(f"LLM returned invalid JSON: {result_text[:200]}")

        winner_address = result.get("winner")
        winner_label = result.get("winner_label", "unknown")
        reasoning = result.get("reasoning", "No reasoning provided")

        # ── STEP 4: Record the result and transfer winnings ──────────────────
        bet["resolved"] = True
        bet["winner"] = winner_address
        bet["resolution_reasoning"] = reasoning

        if winner_label in ("creator", "opponent") and winner_address not in ("none", None):
            total_pot = bet["wager_amount"] * 2
            # Transfer the full pot to the winner
            self.contract_runner.transfer(Address(winner_address), total_pot)
            return (
                f"Bet resolved! Winner: {winner_label} ({winner_address}). "
                f"Reasoning: {reasoning}. "
                f"Transferred {total_pot} tokens."
            )
        else:
            # In case of a draw, refund both parties
            self.contract_runner.transfer(Address(bet["creator"]), bet["wager_amount"])
            self.contract_runner.transfer(Address(bet["opponent"]), bet["wager_amount"])
            return f"Bet resolved as draw. Both parties refunded. Reasoning: {reasoning}"

    @public
    def get_bet(self, bet_id: str) -> dict:
        """Read the full state of a bet."""
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        return self.bets[bet_id]

    @public
    def get_all_bets(self) -> dict:
        """Read all bets. Useful for the frontend."""
        return self.bets

    @public
    def get_bet_count(self) -> int:
        """Returns total number of bets ever created."""
        return self.bet_counter
```

### Step 2.3 — Key Concepts in the Contract

Let's break down the most important parts:

**`get_webpage(url, mode="text")`**
This is a GenLayer built-in function. Every validator independently calls this URL and gets the live content. This is native web access — no oracle needed.

**`call_llm(prompt)`**
This sends the prompt to whatever LLM that specific validator is configured with. Different validators may use GPT-4o, Mistral, Llama, etc. The Equivalence Principle in your prompt is what ensures they all reach the same conclusion.

**The Equivalence Note in the prompt**
This line is critical:
```
EQUIVALENCE NOTE: Two answers are equivalent if they identify the same winner,
regardless of exact wording in the reasoning.
```
This instructs the LLM (and therefore each validator's reasoning process) on what counts as an equivalent answer. It is your contract's definition of truth.

**Structured JSON output**
By forcing the LLM to return JSON, you make comparison across validators straightforward and reduce ambiguity in the Equivalence Principle evaluation.

---

## Part 3 — Testing in GenLayer Studio

Now we load the contract into the Studio and interact with it.

### Step 3.1 — Load the Contract

In the Studio's left panel (Contract Editor), paste the full contract code or use the "Load File" button to import `contracts/p2p_betting.py`.

### Step 3.2 — Deploy the Contract

Click the **"Deploy"** button. The Studio will simulate deploying the contract to your local network. You will see:

- A contract address assigned (e.g., `0x742d35Cc...`)
- The initial state `{"bets": {}, "bet_counter": 0}` in the State panel
- All 5 validator logs showing the deployment transaction

### Step 3.3 — Create a Bet

In the "Write Contract" section, select the `create_bet` method and fill in the parameters:

```
opponent_address:    "0xOpponentAddressHere"
event_description:   "UEFA Champions League Final 2026"
creator_prediction:  "Real Madrid wins"
opponent_prediction: "Manchester City wins or draw"
resolution_url:      "https://www.bbc.com/sport/football"
```

Click **"Execute Transaction"**. Watch the validator logs — you will see all 5 validators execute the transaction and reach consensus. Since this is deterministic (no LLM call), consensus is immediate.

The state will update to show:

```json
{
  "bets": {
    "0": {
      "creator": "0xYourAddress",
      "opponent": "0xOpponentAddress",
      "event_description": "UEFA Champions League Final 2026",
      "creator_prediction": "Real Madrid wins",
      "opponent_prediction": "Manchester City wins or draw",
      "resolved": false,
      "winner": null
    }
  },
  "bet_counter": 1
}
```

### Step 3.4 — Observe Optimistic Democracy on Resolve

Fund the bet from both sides, then call `resolve_bet("0")`. This is the interesting part.

Watch the logs carefully:

```
[Validator 1 - Leader] Fetching URL: https://www.bbc.com/sport/football
[Validator 1 - Leader] Calling LLM (openai/gpt-4o)...
[Validator 1 - Leader] Result: {"winner": "0xCreator", "winner_label": "creator", "reasoning": "Real Madrid won 2-0"}

[Validator 2] Fetching URL: https://www.bbc.com/sport/football
[Validator 2] Calling LLM (mistralai/mistral-large)...
[Validator 2] Checking equivalence with leader result...
[Validator 2] AGREE ✅

[Validator 3] Calling LLM (meta-llama/llama-3...)...
[Validator 3] AGREE ✅

[Validator 4] AGREE ✅
[Validator 5] AGREE ✅

[Consensus] Majority reached. Transaction accepted.
```

You just witnessed Optimistic Democracy in action — 5 different LLMs, same conclusion.

---

## Part 4 — Building the Frontend with genlayer-js

Now we build a React frontend that connects to the deployed contract.

### Step 4.1 — Initialize the Project

```bash
cd frontend
npm install
```

The `package.json` already includes the required dependencies:

```json
{
  "dependencies": {
    "@genlayer/js": "latest",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "vite": "^5.0.0"
  }
}
```

### Step 4.2 — Configure the GenLayer Client

Create `frontend/src/genlayer.js`:

```javascript
// frontend/src/genlayer.js
import { createClient, simulator } from "@genlayer/js";

// Connect to the local Studio simulator
// Replace with testnet config when deploying to Testnet Bradbury
export const client = createClient({
  ...simulator,
  // The contract address you got after deploying in Studio
  // Update this after deployment
});

export const CONTRACT_ADDRESS = "0xYourContractAddressHere";
```

### Step 4.3 — The Main App Component

Create `frontend/src/App.jsx`:

```jsx
// frontend/src/App.jsx
import { useState, useEffect } from "react";
import { client, CONTRACT_ADDRESS } from "./genlayer";
import CreateBet from "./components/CreateBet";
import ActiveBets from "./components/ActiveBets";

export default function App() {
  const [bets, setBets] = useState({});
  const [loading, setLoading] = useState(true);
  const [account, setAccount] = useState(null);

  // Connect wallet on mount
  useEffect(() => {
    const init = async () => {
      try {
        const accounts = await client.getAccounts();
        if (accounts.length > 0) setAccount(accounts[0]);
        await refreshBets();
      } catch (err) {
        console.error("Failed to initialize:", err);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const refreshBets = async () => {
    // Read contract state — no transaction needed, this is free
    const result = await client.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_all_bets",
      args: [],
    });
    setBets(result || {});
  };

  if (loading) return <div className="loading">Connecting to GenLayer...</div>;

  return (
    <div className="app">
      <header>
        <h1>🎲 P2P Betting on GenLayer</h1>
        <p className="subtitle">Trustless bets powered by Intelligent Contracts</p>
        {account && (
          <p className="account">
            Connected: {account.address.slice(0, 6)}...{account.address.slice(-4)}
          </p>
        )}
      </header>

      <main>
        <CreateBet
          client={client}
          contractAddress={CONTRACT_ADDRESS}
          account={account}
          onBetCreated={refreshBets}
        />
        <ActiveBets
          bets={bets}
          client={client}
          contractAddress={CONTRACT_ADDRESS}
          account={account}
          onAction={refreshBets}
        />
      </main>
    </div>
  );
}
```

### Step 4.4 — The CreateBet Component

Create `frontend/src/components/CreateBet.jsx`:

```jsx
// frontend/src/components/CreateBet.jsx
import { useState } from "react";

export default function CreateBet({ client, contractAddress, account, onBetCreated }) {
  const [form, setForm] = useState({
    opponent: "",
    event: "",
    myPrediction: "",
    theirPrediction: "",
    resolutionUrl: "",
  });
  const [status, setStatus] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!account) return alert("Connect your wallet first");

    setSubmitting(true);
    setStatus("Submitting transaction... Waiting for validator consensus...");

    try {
      // Write to the contract — this triggers Optimistic Democracy
      const txHash = await client.writeContract({
        address: contractAddress,
        functionName: "create_bet",
        args: [
          form.opponent,
          form.event,
          form.myPrediction,
          form.theirPrediction,
          form.resolutionUrl,
        ],
        account: account.address,
      });

      setStatus(`Transaction submitted: ${txHash}`);

      // Wait for the transaction to be finalized by consensus
      const receipt = await client.waitForTransactionReceipt({ hash: txHash });

      if (receipt.status === "FINALIZED") {
        setStatus("Bet created successfully! Waiting for opponent to fund.");
        onBetCreated();
        setForm({ opponent: "", event: "", myPrediction: "", theirPrediction: "", resolutionUrl: "" });
      } else {
        setStatus(`Transaction status: ${receipt.status}`);
      }
    } catch (err) {
      setStatus(`Error: ${err.message}`);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <section className="create-bet">
      <h2>Create a New Bet</h2>

      <div className="form-group">
        <label>Opponent Wallet Address</label>
        <input
          placeholder="0x..."
          value={form.opponent}
          onChange={(e) => setForm({ ...form, opponent: e.target.value })}
        />
      </div>

      <div className="form-group">
        <label>Event Description</label>
        <input
          placeholder="e.g. Real Madrid vs Barcelona, La Liga, April 2026"
          value={form.event}
          onChange={(e) => setForm({ ...form, event: e.target.value })}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Your Prediction</label>
          <input
            placeholder="e.g. Real Madrid wins"
            value={form.myPrediction}
            onChange={(e) => setForm({ ...form, myPrediction: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>Opponent's Prediction</label>
          <input
            placeholder="e.g. Barcelona wins or draw"
            value={form.theirPrediction}
            onChange={(e) => setForm({ ...form, theirPrediction: e.target.value })}
          />
        </div>
      </div>

      <div className="form-group">
        <label>Resolution URL</label>
        <input
          placeholder="https://www.bbc.com/sport/football"
          value={form.resolutionUrl}
          onChange={(e) => setForm({ ...form, resolutionUrl: e.target.value })}
        />
        <small>The contract will fetch this URL to determine the winner</small>
      </div>

      <button
        onClick={handleSubmit}
        disabled={submitting}
        className="btn-primary"
      >
        {submitting ? "Waiting for consensus..." : "Create Bet"}
      </button>

      {status && <p className="status">{status}</p>}
    </section>
  );
}
```

### Step 4.5 — The ActiveBets Component

Create `frontend/src/components/ActiveBets.jsx`:

```jsx
// frontend/src/components/ActiveBets.jsx
import { useState } from "react";

export default function ActiveBets({ bets, client, contractAddress, account, onAction }) {
  const [resolving, setResolving] = useState(null);
  const [statuses, setStatuses] = useState({});

  const fundBet = async (betId) => {
    const wager = prompt("Enter the wager amount (tokens):");
    if (!wager) return;

    setStatuses((s) => ({ ...s, [betId]: "Funding... waiting for consensus..." }));

    try {
      const txHash = await client.writeContract({
        address: contractAddress,
        functionName: "fund_bet",
        args: [betId],
        account: account.address,
        value: parseInt(wager),
      });

      await client.waitForTransactionReceipt({ hash: txHash });
      setStatuses((s) => ({ ...s, [betId]: "Funded successfully!" }));
      onAction();
    } catch (err) {
      setStatuses((s) => ({ ...s, [betId]: `Error: ${err.message}` }));
    }
  };

  const resolveBet = async (betId) => {
    setResolving(betId);
    setStatuses((s) => ({
      ...s,
      [betId]: "Resolving... validators are fetching live data and calling LLMs...",
    }));

    try {
      // This is the expensive call — it triggers web fetch + LLM across all validators
      const txHash = await client.writeContract({
        address: contractAddress,
        functionName: "resolve_bet",
        args: [betId],
        account: account.address,
      });

      // Resolution can take longer — validators need to fetch the URL and call LLMs
      const receipt = await client.waitForTransactionReceipt({
        hash: txHash,
        timeout: 120000, // 2 minutes timeout for LLM resolution
      });

      if (receipt.status === "FINALIZED") {
        setStatuses((s) => ({ ...s, [betId]: "Bet resolved! Check the winner below." }));
        onAction();
      }
    } catch (err) {
      setStatuses((s) => ({ ...s, [betId]: `Error: ${err.message}` }));
    } finally {
      setResolving(null);
    }
  };

  const betEntries = Object.entries(bets);

  if (betEntries.length === 0) {
    return (
      <section className="active-bets">
        <h2>Active Bets</h2>
        <p className="empty">No bets yet. Create one above!</p>
      </section>
    );
  }

  return (
    <section className="active-bets">
      <h2>Active Bets</h2>
      {betEntries.map(([betId, bet]) => (
        <div key={betId} className={`bet-card ${bet.resolved ? "resolved" : "active"}`}>
          <div className="bet-header">
            <span className="bet-id">Bet #{betId}</span>
            <span className={`bet-status ${bet.resolved ? "status-resolved" : "status-active"}`}>
              {bet.resolved ? "Resolved" : bet.creator_funded && bet.opponent_funded ? "Funded — Ready to Resolve" : "Awaiting Funding"}
            </span>
          </div>

          <p className="event-desc">{bet.event_description}</p>

          <div className="predictions">
            <div className="prediction creator">
              <span className="label">Creator</span>
              <span className="address">{bet.creator.slice(0, 8)}...</span>
              <span className="pred">{bet.creator_prediction}</span>
              <span className={`funded ${bet.creator_funded ? "yes" : "no"}`}>
                {bet.creator_funded ? "✅ Funded" : "⏳ Pending"}
              </span>
            </div>
            <div className="vs">VS</div>
            <div className="prediction opponent">
              <span className="label">Opponent</span>
              <span className="address">{bet.opponent.slice(0, 8)}...</span>
              <span className="pred">{bet.opponent_prediction}</span>
              <span className={`funded ${bet.opponent_funded ? "yes" : "no"}`}>
                {bet.opponent_funded ? "✅ Funded" : "⏳ Pending"}
              </span>
            </div>
          </div>

          {bet.resolved && (
            <div className="resolution">
              <p className="winner">
                🏆 Winner: <strong>{bet.winner?.slice(0, 10)}...</strong>
              </p>
              <p className="reasoning">
                <em>"{bet.resolution_reasoning}"</em>
              </p>
              <p className="resolution-note">
                Resolved by Optimistic Democracy — 5 validators reached consensus
              </p>
            </div>
          )}

          {!bet.resolved && (
            <div className="bet-actions">
              {account?.address === bet.creator && !bet.creator_funded && (
                <button onClick={() => fundBet(betId)} className="btn-fund">
                  Fund as Creator
                </button>
              )}
              {account?.address === bet.opponent && !bet.opponent_funded && (
                <button onClick={() => fundBet(betId)} className="btn-fund">
                  Fund as Opponent
                </button>
              )}
              {bet.creator_funded && bet.opponent_funded && (
                <button
                  onClick={() => resolveBet(betId)}
                  disabled={resolving === betId}
                  className="btn-resolve"
                >
                  {resolving === betId
                    ? "Validators resolving... (LLMs running)"
                    : "Resolve Bet (fetch live data)"}
                </button>
              )}
            </div>
          )}

          {statuses[betId] && <p className="tx-status">{statuses[betId]}</p>}
        </div>
      ))}
    </section>
  );
}
```

### Step 4.6 — Run the Frontend

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Part 5 — Deploying to Testnet

Once you are happy with your local testing, deploy to GenLayer's Testnet Bradbury.

### Step 5.1 — Configure Testnet in genlayer.js

```javascript
// frontend/src/genlayer.js
import { createClient, testnet } from "@genlayer/js";

export const client = createClient({
  ...testnet,
  // Add your wallet configuration here
});
```

### Step 5.2 — Deploy the Contract via CLI

```bash
# Configure the network
genlayer config set network testnet

# Deploy
genlayer deploy contracts/p2p_betting.py

# Output:
# Deploying to Testnet Bradbury...
# Contract deployed at: 0xYourContractAddress
# Transaction hash: 0xDeployTxHash
```

### Step 5.3 — Update the Contract Address

Copy the deployed address and update `CONTRACT_ADDRESS` in `frontend/src/genlayer.js`.

---

## How Optimistic Democracy Powers This App

Here is a summary of what happens under the hood every time `resolve_bet()` is called:

```
User calls resolve_bet("0")
        │
        ▼
GenLayer selects 5 random validators
        │
        ├── Validator 1 (Leader, GPT-4o)
        │   ├── Fetches resolution_url
        │   ├── Calls LLM with prompt
        │   └── Returns: {"winner": "0xAlice", "winner_label": "creator", ...}
        │
        ├── Validator 2 (Mistral)
        │   ├── Fetches resolution_url independently
        │   ├── Calls its own LLM
        │   ├── Applies Equivalence Principle to Leader's answer
        │   └── AGREE ✅
        │
        ├── Validator 3 (Llama)
        │   └── AGREE ✅
        │
        ├── Validator 4 (Claude)
        │   └── AGREE ✅
        │
        └── Validator 5 (Gemini)
            └── AGREE ✅

Majority reached → Transaction FINALIZED
Winner receives 2x wager automatically
```

The Equivalence Principle ensures that even though each LLM may phrase the answer differently ("Alice won", "The creator's prediction was correct", "Real Madrid won as the creator predicted"), they all identify the same winner — and that is sufficient for consensus.

---

## Project Structure

```
p2p-betting-genlayer/
├── contracts/
│   └── p2p_betting.py           # Full Intelligent Contract
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── genlayer.js          # Client configuration
│   │   └── components/
│   │       ├── CreateBet.jsx
│   │       ├── ActiveBets.jsx
│   │       └── ResolveBet.jsx
│   ├── package.json
│   └── vite.config.js
├── tests/
│   └── test_betting.py
└── README.md
```

---

## Troubleshooting

**Docker is not running**
GenLayer Studio requires Docker. Make sure Docker Desktop is running before executing `genlayer up`.

**Contract fails to resolve**
Check the resolution URL — it must be publicly accessible and contain relevant information about the event. The LLM needs enough context to determine a winner.

**Validators disagree**
If you see disagreement in the logs, review your Equivalence Note in the prompt. Make it more specific about what counts as an equivalent answer. A clearer prompt produces more consistent consensus.

**Frontend cannot connect**
Make sure the Studio is running (`genlayer up`) and the contract address in `genlayer.js` matches the address shown after deployment.

**Transaction times out on resolve**
LLM resolution can take up to 60 seconds in the Studio. This is normal — each validator is independently fetching a URL and calling an LLM. Increase the timeout in `waitForTransactionReceipt` if needed.

---

## Next Steps

Now that you have completed this tutorial, here are ideas for extending the project:

**Add more event types** — The contract currently works for any event. Try adding specialized resolution logic for financial markets (checking a price API) or sports with structured data sources.

**Add a time lock** — Prevent resolution before a certain block height or timestamp to ensure the event has actually concluded.

**Build a bet discovery UI** — Add a way for users to browse open bets and join as opponents, turning this into a proper marketplace.

**Add reputation scoring** — Track which users create bets that resolve correctly and build an on-chain reputation system.

**Explore the Appeal Process** — In the Studio, try triggering a disagreement by modifying a validator's LLM response and observe how the appeal mechanism escalates the validator set.

---

## Resources

Official Documentation: https://docs.genlayer.com
GenLayer Studio: http://localhost:8080 (after `genlayer up`)
GenLayer Boilerplate: https://github.com/genlayerlabs/genlayer-boilerplate
GenLayerJS SDK Reference: https://docs.genlayer.com/developers/decentralized-applications/genlayer-js
Optimistic Democracy Deep Dive: https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy
Equivalence Principle: https://docs.genlayer.com/understand-genlayer-protocol/core-concepts/optimistic-democracy/equivalence-principle

**Community**

Discord: https://discord.gg/8Jm4v89VAu
X (Twitter): https://x.com/GenLayer
Website: https://www.genlayer.com

---

*Built as part of the GenLayer "From Zero to GenLayer" tutorial mission. All code is open source and free to fork.*
