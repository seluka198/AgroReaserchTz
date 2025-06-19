<!-- templates/forecast.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Rainfall Forecast</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

</head>
<body>
<h2>Rainfall Forecast for 2025–2027</h2>
<canvas id="rainChart" width="800" height="400"></canvas>

<script>
fetch('/forecast/')
    .then(response => response.json())
    .then(data => {
        const labels = data.forecast.map(item => item.month);
        const rainfall = data.forecast.map(item => item.rainfall);

        const ctx = document.getElementById('rainChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Rainfall (mm)',
                    data: rainfall,
                    borderColor: 'blue',
                    fill: false
                }]
            }
        });
    });
</script>
</body>
</html>
