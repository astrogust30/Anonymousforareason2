let tempUnit = '°C';
$(document).ready(function() {
    // Update Threshold
    $('#configure-alerts-form').submit(function(e) {
        e.preventDefault();
        const thresholdTemp = $('#threshold-temp').val();
        $.post('/update_threshold', { threshold_temp: thresholdTemp }, function(data) {
            alert(data.message);
        });
    });

    // Load Daily Summaries
    function loadDailySummaries() {
        $.get('/get_daily_summaries', function(data) {
            let summariesHtml = '';
            data.summaries.forEach(function(summary) {
                summariesHtml += `
                    <div class="summary">
                        <h4>${summary.city} (${summary.date})</h4>
                        <p>Average Temp: ${summary.avg_temp.toFixed(2)} ${tempUnit}</p>
                        <p>Max Temp: ${summary.max_temp.toFixed(2)} ${tempUnit}</p>
                        <p>Min Temp: ${summary.min_temp.toFixed(2)} ${tempUnit}</p>
                        <p>Average Humidity: ${summary.avg_humidity.toFixed(2)}%</p>
                        <p>Max Humidity: ${summary.max_humidity}%</p>
                        <p>Min Humidity: ${summary.min_humidity}%</p>
                        <p>Average Wind Speed: ${summary.avg_wind_speed.toFixed(2)} m/s</p>
                        <p>Max Wind Speed: ${summary.max_wind_speed} m/s</p>
                        <p>Min Wind Speed: ${summary.min_wind_speed} m/s</p>
                        <p>Dominant Weather: ${summary.dominant_weather}</p>
                    </div>
                    <hr>
                `;
            });
            $('#daily-summaries').html(summariesHtml);
        });
    }
    // Load Triggered Alerts
    function loadTriggeredAlerts() {
        $.get('/get_triggered_alerts', function(data) {
            let alertsHtml = '';
            data.alerts.forEach(function(alert) {
                alertsHtml += `<p><strong>${alert.city} (${alert.timestamp}):</strong> ${alert.alert_message}</p>`;
            });
            $('#triggered-alerts').html(alertsHtml);
        });
    }

    // Load Temperature Chart
    function loadTemperatureChart() {
        $.get('/get_temperature_data', function(data) {
            const ctx = document.getElementById('temperature-chart').getContext('2d');
            
            // Define an array of colors
            const colors = [
                'rgba(255, 99, 132, 1)',    // Red
                'rgba(54, 162, 235, 1)',   // Blue
                'rgba(255, 206, 86, 1)',   // Yellow
                'rgba(75, 192, 192, 1)',   // Green
                'rgba(153, 102, 255, 1)',  // Purple
                'rgba(255, 159, 64, 1)',   // Orange
                // Add more colors if you have more cities
            ];
            
            // Assign colors to each dataset
            data.datasets.forEach(function(dataset, index) {
                dataset.borderColor = colors[index % colors.length];
                dataset.backgroundColor = colors[index % colors.length];
                dataset.fill = false; // Keep the chart lines without filling under them
            });
            
            const chartData = {
                labels: data.timestamps,
                datasets: data.datasets
            };
            
            new Chart(ctx, {
                type: 'line',
                data: chartData,
                options: {
                    title: {
                        display: true,
                        text: 'Temperature Trends'
                    },
                    scales: {
                        xAxes: [{
                            type: 'time',
                            time: {
                                unit: 'day'
                            },
                            distribution: 'linear'
                        }],
                        yAxes: [{
                            scaleLabel: {
                                display: true,
                                labelString: `Temperature (${tempUnit || '°C'})`
                            }
                        }]
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                    },
                    legend: {
                        display: true,
                        position: 'bottom',
                    }
                }
            });
        });
    }
    function loadForecastSummaries() {
        $.get('/get_forecast_summaries', function(data) {
            let forecastsHtml = '';
            data.summaries.forEach(function(summary) {
                const weatherIcon = getWeatherIcon(summary.dominant_weather);
                const tempColorClass = getTemperatureColor(summary.avg_temp);
                const weatherBgClass = getWeatherBackground(summary.dominant_weather);
                
                forecastsHtml += `
                    <div class="col-sm-12 col-md-6 col-lg-4">
                        <div class="card mb-4 shadow-sm ${weatherBgClass}">
                            <div class="card-body">
                                <h5 class="card-title">${summary.city}</h5>
                                <div class="weather-icon mb-2">
                                    ${weatherIcon} ${summary.dominant_weather}
                                </div>
                                <p class="card-text">
                                    <i class="fas fa-thermometer-half"></i> <strong>Avg Temp:</strong> <span class="${tempColorClass}">${summary.avg_temp.toFixed(2)} ${tempUnit}</span><br>
                                    <i class="fas fa-tint"></i> <strong>Avg Humidity:</strong> ${summary.avg_humidity.toFixed(2)}%<br>
                                    <i class="fas fa-wind"></i> <strong>Avg Wind Speed:</strong> ${summary.avg_wind_speed.toFixed(2)} m/s<br>
                                </p>
                            </div>
                        </div>
                    </div>
                `;
            });
            $('#forecast-summaries').html('<div class="row">' + forecastsHtml + '</div>');
        });
    }
    function getWeatherIcon(condition) {
        const conditionLower = condition.toLowerCase();
        if (conditionLower.includes('clear')) {
            return '<i class="fas fa-sun"></i>';
        } else if (conditionLower.includes('cloud')) {
            return '<i class="fas fa-cloud"></i>';
        } else if (conditionLower.includes('rain')) {
            return '<i class="fas fa-cloud-showers-heavy"></i>';
        } else if (conditionLower.includes('snow')) {
            return '<i class="fas fa-snowflake"></i>';
        } else if (conditionLower.includes('thunderstorm')) {
            return '<i class="fas fa-bolt"></i>';
        } else {
            return '<i class="fas fa-smog"></i>';
        }
    }
    function getWeatherBackground(condition) {
        const conditionLower = condition.toLowerCase();
        if (conditionLower.includes('clear')) {
            return 'bg-warning'; // Yellow background
        } else if (conditionLower.includes('cloud')) {
            return 'bg-light'; // Light gray background
        } else if (conditionLower.includes('rain')) {
            return 'bg-primary text-white'; // Blue background with white text
        } else if (conditionLower.includes('snow')) {
            return 'bg-info text-white'; // Light blue background
        } else if (conditionLower.includes('thunderstorm')) {
            return 'bg-dark text-white'; // Dark background
        } else {
            return 'bg-secondary text-white'; // Gray background
        }
    }

    function getTemperatureColor(temp) {
        if (temp >= 30) {
            return 'text-danger'; // Red for hot temperatures
        } else if (temp >= 20) {
            return 'text-warning'; // Orange for warm temperatures
        } else if (temp >= 10) {
            return 'text-info'; // Light blue for mild temperatures
        } else {
            return 'text-primary'; // Blue for cold temperatures
        }
    }
    // Call the function to load forecast summaries
    loadForecastSummaries();
 

    loadDailySummaries();
    loadTriggeredAlerts();
    loadTemperatureChart();

    // Set intervals to refresh data
    setInterval(loadForecastSummaries, 60000); // Refresh every minute
    setInterval(loadDailySummaries, 60000); // Refresh every minute
    setInterval(loadTriggeredAlerts, 60000);
    setInterval(loadTemperatureChart, 60000);
});