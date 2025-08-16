async function loadData() {
  const stockList = document.getElementById("stock-list");
  const cryptoList = document.getElementById("crypto-list");

  try {
    const stockRes = await fetch("data/latest_stocks.json");
    const stocks = await stockRes.json();

    const cryptoRes = await fetch("data/latest_crypto.json");
    const cryptos = await cryptoRes.json();

    stockList.innerHTML = "";
    cryptoList.innerHTML = "";

    stocks.forEach(s => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${s.ticker}</strong> - $${s.price} (${s.change_percent}%)
        <br>RSI: ${s.rsi}, RVOL: ${s.rvol}, VWAP Prox: ${s.vwap_proximity}
        <br>AI Score: ${s.ai_score} (${s.reason})
        <br>Risk: ${s.risk}
        <br>
        <a href="${s.sentiment_link}" target="_blank">Sentiment</a> | 
        <a href="${s.catalyst_link}" target="_blank">Catalyst</a> | 
        <a href="${s.news_link}" target="_blank">News</a> | 
        <a href="${s.tradingview_link}" target="_blank">Chart</a>
      `;
      stockList.appendChild(li);
    });

    cryptos.forEach(c => {
      const li = document.createElement("li");
      li.innerHTML = `
        <strong>${c.symbol}</strong> - $${c.price} (${c.change_percent}%)
        <br>RSI: ${c.rsi}, RVOL: ${c.rvol}, VWAP Prox: ${c.vwap_proximity}
        <br>AI Score: ${c.ai_score} (${c.reason})
        <br>Risk: ${c.risk}
        <br>
        <a href="${c.sentiment_link}" target="_blank">Sentiment</a> | 
        <a href="${c.catalyst_link}" target="_blank">Catalyst</a> | 
        <a href="${c.news_link}" target="_blank">News</a> | 
        <a href="${c.tradingview_link}" target="_blank">Chart</a>
      `;
      cryptoList.appendChild(li);
    });

  } catch (err) {
    console.error("Error loading data", err);
  }
}

setInterval(loadData, 60000);
loadData();
