import { useState, useEffect } from "react";
import { client, CONTRACT_ADDRESS } from "./genlayer";
import CreateBet from "./components/CreateBet";
import ActiveBets from "./components/ActiveBets";

export default function App() {
  const [bets, setBets] = useState({});
  const [loading, setLoading] = useState(true);
  const [account, setAccount] = useState(null);

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
