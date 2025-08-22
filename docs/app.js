const cryptoToggle = document.getElementById("crypto-toggle");
const stocksToggle = document.getElementById("stocks-toggle");
const resultsContainer = document.getElementById("results");
const triggerLogContainer = document.getElementById("trigger-log");

let currentAssetType = "crypto";

cryptoToggle.addEventListener("click", () => {
  currentAssetType = "crypto";
  loadResults();
});

stocksToggle.addEventListener("click", () => {
  currentAssetType = "stock";
  loadResults();
});

async function loadResults() {
  const file = currentAssetType === "crypto"
    ? "data/latest_crypto.json"
    : "data/latest_stocks.json";

  try {
    const response = await fetch(file);
    const data = await response.json();
    renderResults(data);
  } catch (error) {
    resultsContainer.innerHTML = `<p>Error loading ${currentAssetType} data.</p>`;
  }
}

function renderResults(data) {
  resultsContainer.innerHTML = "";

  data.forEach(asset => {
    const card = document.createElement("div");
    card.className = "asset-card";

    card.innerHTML = `
      <h3>${asset.ticker}</h3>
      <p>Price: $${asset.price}</p>
      <p>Change: ${asset.change}%</p>
      <p>Volume: ${asset.volume}</p>
      <p>RSI: ${asset.rsi}</p>
      <p>RVOL: ${asset.rvol}</p>
      <p>AI Score: ${asset.ai_score}/10 (${asset.confidence})</p>
      <p>SL: $${asset.risk.stop_loss} | TP: $${asset.risk.take_profit}</p>
      <p>Sentiment: ${asset.sentiment.score}</p>
      <p><a href="https://www.tradingview.com/symbols/${asset.ticker}" target="_blank">Chart</a></p>
      <p><a href="${asset.catalyst.headline}" target="_blank">News</a></p>
      <p><a href="${asset.catalyst.tweet}" target="_blank">Tweet</a></p>
      <p><a href="${asset.catalyst.reddit}" target="_blank">Reddit</a></p>
    `;

    resultsContainer.appendChild(card);
  });
}

async function loadTriggerLog() {
  try {
    const response = await fetch("data/trigger_log.json");
    const log = await response.json();

    triggerLogContainer.innerHTML = log.map(entry => `
      <div class="log-entry">
        <strong>${entry.ticker}</strong> — ${entry.reason} (${entry.score})<br>
        <small>${entry.timestamp}</small>
      </div>
    `).join("");
  } catch (error) {
    triggerLogContainer.innerHTML = "<p>Error loading trigger log.</p>";
  }
}

// Initial load
loadResults();
loadTriggerLog();
