async function fetchData(type) {
    const url = `data/latest_${type}.json`;
    const response = await fetch(url);
    const data = await response.json();
    const list = document.getElementById(`${type}-list`);
    list.innerHTML = '';

    data.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.ticker}: ${item.message}`;
        list.appendChild(li);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    fetchData('stocks');
    fetchData('crypto');

    // Refresh every 10 minutes
    setInterval(() => {
        fetchData('stocks');
        fetchData('crypto');
    }, 10 * 60 * 1000);
});
