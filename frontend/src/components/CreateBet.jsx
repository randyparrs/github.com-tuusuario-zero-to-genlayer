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
