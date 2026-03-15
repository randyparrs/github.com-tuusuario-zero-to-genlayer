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
      const txHash = await client.writeContract({
        address: contractAddress,
        functionName: "resolve_bet",
        args: [betId],
        account: account.address,
      });

      const receipt = await client.waitForTransactionReceipt({
        hash: txHash,
        timeout: 120000,
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
              {bet.resolved ? "Resolved" : bet.creator_funded && bet.opponent_funded ? "Ready to Resolve" : "Awaiting Funding"}
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
                  {resolving === betId ? "Validators resolving..." : "Resolve Bet"}
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
