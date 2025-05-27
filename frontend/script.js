document.getElementById("popularity").addEventListener("input", function () {
    document.getElementById("popularity-value").textContent = this.value;
});

document.getElementById("predict-form").addEventListener("submit", async function (e) {
    e.preventDefault();

    const genre = document.getElementById("genre").value;
    const popularity = parseFloat(document.getElementById("popularity").value);
    const vote_average = parseFloat(document.getElementById("vote_average").value);
    const vote_count = parseInt(document.getElementById("vote_count").value);

    // Show loading spinner
    document.getElementById("loading").style.display = "block";
    document.getElementById("result").style.display = "none";

    const payload = {
        popularity,
        vote_average,
        vote_count,
        season_Fall: 0,
        season_Spring: 0,
        season_Summer: 1,
        season_Winter: 0,
        genre_Action: genre === "Action" ? 1 : 0,
        genre_Comedy: genre === "Comedy" ? 1 : 0,
        genre_Drama: genre === "Drama" ? 1 : 0,
        genre_Romance: genre === "Romance" ? 1 : 0,
        genre_Horror: genre === "Horror" ? 1 : 0,
        genre_Thriller: genre === "Thriller" ? 1 : 0,
        genre_Other: genre === "Other" ? 1 : 0
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        document.getElementById("result").innerHTML = `
            <h4>🎉 Prediction Result</h4>
            <p><strong>Recommended Release Season:</strong> ${result.predicted_season}</p>
            <p><strong>Confidence:</strong> ${(parseFloat(result.confidence) * 100).toFixed(1)}%</p>
        `;
        document.getElementById("result").className = "alert alert-success";
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<p>❌ Error connecting to the server.</p>`;
        document.getElementById("result").className = "alert alert-danger";
    } finally {
        document.getElementById("loading").style.display = "none";
        document.getElementById("result").style.display = "block";
    }
});
function renderGenreChart() {
    const ctx = document.getElementById("genreChart").getContext("2d");

    const data = {
        labels: ["Action", "Comedy", "Drama", "Romance", "Horror", "Thriller", "Other"],
        datasets: [{
            label: "Genre Frequency",
            data: [15, 20, 10, 12, 8, 9, 6],  // Replace with real data later
            backgroundColor: [
                "#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#8DD776"
            ]
        }]
    };

    new Chart(ctx, {
        type: "bar",
        data: data,
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Render chart on page load
window.onload = renderGenreChart;
