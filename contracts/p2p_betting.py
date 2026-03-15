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
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        bet = self.bets[bet_id]
        assert not bet["resolved"], "Bet is already resolved"

        caller = str(self.contract_runner.from_address)
        value = self.contract_runner.value

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
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        bet = self.bets[bet_id]

        assert not bet["resolved"], "Bet is already resolved"
        assert bet["creator_funded"] and bet["opponent_funded"], (
            "Both parties must fund the bet before it can be resolved"
        )

        event_data = get_webpage(bet["resolution_url"], mode="text")

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

        try:
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

        bet["resolved"] = True
        bet["winner"] = winner_address
        bet["resolution_reasoning"] = reasoning

        if winner_label in ("creator", "opponent") and winner_address not in ("none", None):
            total_pot = bet["wager_amount"] * 2
            self.contract_runner.transfer(Address(winner_address), total_pot)
            return (
                f"Bet resolved! Winner: {winner_label} ({winner_address}). "
                f"Reasoning: {reasoning}. "
                f"Transferred {total_pot} tokens."
            )
        else:
            self.contract_runner.transfer(Address(bet["creator"]), bet["wager_amount"])
            self.contract_runner.transfer(Address(bet["opponent"]), bet["wager_amount"])
            return f"Bet resolved as draw. Both parties refunded. Reasoning: {reasoning}"

    @public
    def get_bet(self, bet_id: str) -> dict:
        assert bet_id in self.bets, f"Bet {bet_id} does not exist"
        return self.bets[bet_id]

    @public
    def get_all_bets(self) -> dict:
        return self.bets

    @public
    def get_bet_count(self) -> int:
        return self.bet_counter
