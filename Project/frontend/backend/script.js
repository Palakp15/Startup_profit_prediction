const API_BASE = 'http://localhost:5001'; // ✅ backend running on port 5001

document.getElementById('predict-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const rd = parseFloat(document.getElementById('rd').value);
  const admin = parseFloat(document.getElementById('admin').value);
  const market = parseFloat(document.getElementById('market').value);
  const state = document.getElementById('state').value;

  if (isNaN(rd) || isNaN(admin) || isNaN(market)) {
    alert('Please enter valid numeric values.');
    return;
  }

  const payload = { rd_spend: rd, administration: admin, marketing_spend: market, state };
  showLoading(true);

  try {
    const res = await fetch(`${API_BASE}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!res.ok) throw new Error('Prediction request failed');

    const data = await res.json();

    showResult(data.prediction);
    updateChart(rd + admin + market, data.prediction);

    // ✅ NEW — update history
    updateHistory(
      { rd, admin, market },
      data.prediction
    );

  } catch (err) {
    alert('Error: ' + (err.message || err));
    console.error(err);
  } finally {
    showLoading(false);
  }
});

function showLoading(on) {
  document.getElementById('loading').classList.toggle('hidden', !on);
  document.getElementById('predict-btn').disabled = on;
}

function showResult(value) {
  document.getElementById('profit-value').textContent = '₹ ' + formatNumber(value);
  document.getElementById('result').classList.remove('hidden');
}

function formatNumber(n) {
  return Number(n).toLocaleString(undefined, { maximumFractionDigits: 2 });
}

/* ✅ Chart.js — dynamic chart */
const ctx = document.getElementById('profitChart').getContext('2d');
const chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Expenses', 'Predicted Profit'],
    datasets: [{
      label: '₹',
      data: [0, 0]
    }]
  },
  options: {
    responsive: true,
    plugins: { legend: { display: false } },
    scales: { y: { beginAtZero: true } }
  }
});

function updateChart(expenses, profit) {
  chart.data.datasets[0].data = [Math.round(expenses), Math.round(profit)];
  chart.update();
}

/* ✅ NEW — prediction history feature */
const historyList = [];

function updateHistory(input, prediction) {
  historyList.push({ input, prediction });

  const box = document.getElementById('history');
  box.innerHTML = historyList
    .map(item => `
      <div class="history-item">
        ₹${item.input.rd} + ₹${item.input.admin} + ₹${item.input.market}
        → <b>₹ ${formatNumber(item.prediction)}</b>
      </div>
    `)
    .join('');
}

/* Initialize sample */
updateChart(300000, 150000);
