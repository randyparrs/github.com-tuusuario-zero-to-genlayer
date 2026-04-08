# { "Depends": "py-genlayer:test" }

import json
from genlayer import *


class P2PBetting(gl.Contract):

    owner: Address
    bet_counter: u256
    bet_data: DynArray[str]  # flat key:value storage "bet_{id}_{field}:value"

    def __init__(self, owner_address: Address):
        self.owner = owner_address
        self.bet_counter = u256(0)

    @gl.public.view
    def get_bet(self, bet_id: str) -> str:
        creator = self._get_field(bet_id, "creator")
        if not creator:
            return "Bet not found"
        return (
            f"ID: {bet_id} | "
            f"Event: {self._get_field(bet_id, 'event')} | "
            f"Creator prediction: {self._get_field(bet_id, 'creator_prediction')} | "
            f"Opponent prediction: {self._get_field(bet_id, 'opponent_prediction')} | "
            f"Resolved: {self._get_field(bet_id, 'resolved')} | "
            f"Winner: {self._get_field(bet_id, 'winner')} | "
            f"Reasoning: {self._get_field(bet_id, 'reasoning')}"
        )

    @gl.public.view
    def get_bet_count(self) -> u256:
        return self.bet_counter

    @gl.public.view
    def get_platform_summary(self) -> str:
        return (
            f"P2P Betting Platform\n"
            f"Total Bets: {int(self.bet_counter)}"
        )

    @gl.public.write
    def create_bet(
        self,
        opponent_address: Address,
        event_description: str,
        creator_prediction: str,
        opponent_prediction: str,
        resolution_url: str,
    ) -> str:
        caller = str(gl.message.sender_address)
        bet_id = str(int(self.bet_counter))

        self._set_field(bet_id, "creator", caller)
        self._set_field(bet_id, "opponent", str(opponent_address))
        self._set_field(bet_id, "event", event_description)
        self._set_field(bet_id, "creator_prediction", creator_prediction)
        self._set_field(bet_id, "opponent_prediction", opponent_prediction)
        self._set_field(bet_id, "resolution_url", resolution_url)
        self._set_field(bet_id, "resolved", "false")
        self._set_field(bet_id, "winner", "")
        self._set_field(bet_id, "reasoning", "")

        self.bet_counter = u256(int(self.bet_counter) + 1)
        return f"Bet {bet_id} created! Event: {event_description}"

    @gl.public.write
    def resolve_bet(self, bet_id: str) -> str:
        creator = self._get_field(bet_id, "creator")
        assert creator, "Bet not found"
        assert self._get_field(bet_id, "resolved") == "false", "Already resolved"

        event = self._get_field(bet_id, "event")
        creator_prediction = self._get_field(bet_id, "creator_prediction")
        opponent_prediction = self._get_field(bet_id, "opponent_prediction")
        resolution_url = self._get_field(bet_id, "resolution_url")
        opponent = self._get_field(bet_id, "opponent")

        def leader_fn():
            response = gl.nondet.web.get(resolution_url)
            event_data = response.body.decode("utf-8")[:3000]

            prompt = f"""You are an impartial judge for a P2P bet. Determine the winner.

BET DETAILS:
Event: {event}
Creator's prediction: {creator_prediction}
Opponent's prediction: {opponent_prediction}

LIVE DATA FROM THE WEB (from {resolution_url}):
{event_data}

Based strictly on the live data, determine who won the bet.
Respond ONLY with a JSON object:
{{
  "winner_label": "creator",
  "reasoning": "one sentence explaining why based on the data"
}}

Rules:
- winner_label: exactly "creator", "opponent", or "draw"
- reasoning: one sentence based only on the factual data
- If data is insufficient use "draw"
No extra text."""

            result = gl.nondet.exec_prompt(prompt)
            clean = result.strip().replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)

            winner_label = data.get("winner_label", "draw")
            reasoning = data.get("reasoning", "")

            if winner_label not in ("creator", "opponent", "draw"):
                winner_label = "draw"

            return json.dumps({
                "winner_label": winner_label,
                "reasoning": reasoning
            }, sort_keys=True)

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False
            try:
                validator_raw = leader_fn()
                leader_data = json.loads(leader_result.calldata)
                validator_data = json.loads(validator_raw)
                return leader_data["winner_label"] == validator_data["winner_label"]
            except Exception:
                return False

        raw = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        data = json.loads(raw)

        winner_label = data["winner_label"]
        reasoning = data["reasoning"]

        if winner_label == "creator":
            winner_address = creator
        elif winner_label == "opponent":
            winner_address = opponent
        else:
            winner_address = "draw"

        self._set_field(bet_id, "resolved", "true")
        self._set_field(bet_id, "winner", winner_address)
        self._set_field(bet_id, "reasoning", reasoning)

        return (
            f"Bet {bet_id} resolved! "
            f"Winner: {winner_label} ({winner_address}). "
            f"Reasoning: {reasoning}"
        )

    def _get_field(self, bet_id: str, field: str) -> str:
        key = f"bet_{bet_id}_{field}:"
        for i in range(len(self.bet_data)):
            if self.bet_data[i].startswith(key):
                return self.bet_data[i][len(key):]
        return ""

    def _set_field(self, bet_id: str, field: str, value: str) -> None:
        key = f"bet_{bet_id}_{field}:"
        for i in range(len(self.bet_data)):
            if self.bet_data[i].startswith(key):
                self.bet_data[i] = f"{key}{value}"
                return
        self.bet_data.append(f"{key}{value}")
