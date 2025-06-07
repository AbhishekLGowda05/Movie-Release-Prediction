document.getElementById("predict-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const genre = document.getElementById("genre").value;
  const platform = document.getElementById("platform").value;
  const region = document.getElementById("region").value;

  const loadingEl = document.getElementById("loading");
  const resultEl = document.getElementById("result");

  loadingEl.style.display = "block";
  resultEl.innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ genre, platform, region })
    });

    const data = await response.json();
    loadingEl.style.display = "none";

    if (data.error) {
      resultEl.innerHTML = `<div class="alert alert-danger"><strong>Error:</strong> ${data.error}</div>`;
    } else {
      const scores = data.confidence_scores;
      const seasons = Object.keys(scores);
      const values = Object.values(scores);

      resultEl.innerHTML = `
        <div class="alert alert-success shadow-sm">
          <h4 class="alert-heading">📅 Recommended Release Season: <strong>${data.predicted_season}</strong></h4>
          <p>📊 Confidence chart shown below:</p>
        </div>
      `;

      // Remove previous chart if any
      if (window.chartInstance) {
        window.chartInstance.destroy();
      }

      const ctx = document.getElementById("confidenceChart").getContext("2d");
      window.chartInstance = new Chart(ctx, {
        type: "bar",
        data: {
          labels: seasons,
          datasets: [{
            label: "Prediction Confidence (%)",
            data: values,
            backgroundColor: "#4e73df"
          }]
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
              max: 100
            }
          }
        }
      });
    }
  } catch (err) {
    loadingEl.style.display = "none";
    resultEl.innerHTML = `<div class="alert alert-danger">❌ Failed to connect to the backend.</div>`;
    console.error(err);
  }
});
