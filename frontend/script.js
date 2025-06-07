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
      let confidenceHTML = "";
      for (let season in data.confidence_scores) {
        confidenceHTML += `<li>${season}: ${data.confidence_scores[season]}%</li>`;
      }

      resultEl.innerHTML = `
        <div class="alert alert-success shadow-sm">
          <h4 class="alert-heading">📅 Recommended Release Season: <strong>${data.predicted_season}</strong></h4>
          <p>📊 Confidence Scores:</p>
          <ul>${confidenceHTML}</ul>
        </div>
      `;
    }
  } catch (err) {
    loadingEl.style.display = "none";
    resultEl.innerHTML = `<div class="alert alert-danger">❌ Failed to connect to the backend.</div>`;
    console.error(err);
  }
});
