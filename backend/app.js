async function fetchSignals() {
    try {
        const response = await fetch("signals.json", { cache: "no-store" });
        if (!response.ok) throw new Error("Failed to load signals.json");
        const signals = await response.json();
        return signals;
    } catch (error) {
        console.error("Error fetching signals:", error);
        return [];
    }
}

function displaySignals(signals) {
    const stockList = document.getElementById("stock-list");
    const cryptoList = document.getElementById("crypto-list");

    stockList.innerHTML = "";
    cryptoList.innerHTML = "";

    signals.forEach(signal => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${signal.symbol}</strong> - $${signal.price} (${signal.change}%)
            | AI Score: ${signal.ai_score}
            | Risk: SL=${signal.risk.sl}, TP=${signal.risk.tp}, Pos=${signal.risk.position_size}
            <br>
            Sentiment: ${signal.sentiment}
            <br>
            <a href="https://www.tradingview.com/symbols/${signal.symbol}/" target="_blank">Chart</a>
            ${signal.news_url ? ` | <a href="${signal.news_url}" target="_blank">News</a>` : ""}
        `;

        if (signal.asset_type === "stock") stockList.appendChild(li);
        else if (signal.asset_type === "crypto") cryptoList.appendChild(li);
    });
}

async function refreshSignals() {
    const signals = await fetchSignals();
    displaySignals(signals);
}

// Initial load
refreshSignals();

// Auto-refresh every 45 minutes (2700000 ms)
setInterval(refreshSignals, 2700000);
