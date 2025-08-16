async function loadSignals() {
    const response = await fetch('../signals.json');
    const data = await response.json();

    const stockList = document.getElementById('stock-list');
    const cryptoList = document.getElementById('crypto-list');

    stockList.innerHTML = '';
    cryptoList.innerHTML = '';

    data.stocks.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.ticker} - ${item.signal}`;
        stockList.appendChild(li);
    });

    data.crypto.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.ticker} - ${item.signal}`;
        cryptoList.appendChild(li);
    });
}

loadSignals();
setInterval(loadSignals, 60000); // refresh every 60 seconds
