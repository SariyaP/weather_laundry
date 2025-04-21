function setBackgroundColor() {
    const now = new Date();
    const hour = now.getHours();
    let backgroundColor;
    if (hour >= 6 && hour < 12) {

        backgroundColor = "linear-gradient(334deg,rgba(55, 132, 184, 1) 50%, rgb(218, 200, 114) 100%)";
    } else if (hour >= 12 && hour < 20) {
        backgroundColor = "linear-gradient(155deg,rgba(55, 132, 184, 1) 50%, rgba(149, 216, 237, 1) 100%)";
    } else {
        backgroundColor = "linear-gradient(104deg,rgba(14, 70, 110, 1) 0%, rgba(62, 96, 150, 1) 56%, rgba(56, 56, 110, 1) 100%)";
    }
    document.body.style.background = backgroundColor;
}

setBackgroundColor();
setInterval(setBackgroundColor, 60000);

function updateTime() {
    const now = new Date();
    const hour = now.getHours();
    const minute = now.getMinutes()
    document.getElementById('current-time').innerHTML =
        `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
}

setInterval(updateTime, 1000);

function updateDate() {
    const now = new Date();
    const day = now.getDate();
    const month = now.toLocaleString('default', {month: 'long'});

    document.getElementById('current-date').innerHTML =
        `${month}, ${day}`;
}

setInterval(updateDate, 1000);
document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('weatherCalendar');

  function getConditionStyle(condition) {
    if (!condition) return { title: 'Unknown', backgroundColor: '#808080' };

    condition = condition.toLowerCase();
    if (condition.includes('sunny')) return { title: '☀️ Sunny', backgroundColor: '#df8e23' };
    if (condition.includes('rain')) return { title: '🌧️ Rainy', backgroundColor: '#348fae' };
    if (condition.includes('storm')) return { title: '🌩️ Storm', backgroundColor: '#426dbf' };
    if (condition.includes('cloud')) return { title: '☁️ Cloudy', backgroundColor: '#6081a1' };
    return { title: '⛅ Weather', backgroundColor: '#ADD8E6' };
  }

  fetch('http://127.0.0.1:8080/laundry-api/v1/forecast-weather-conditions')
    .then(response => response.json())
    .then(data => {
      const events = data.map(entry => {
        const style = getConditionStyle(entry.predicted_condition);
        return {
          title: `${style.title} ${entry.predicted_condition}`,
          date: entry.date,
          backgroundColor: style.backgroundColor
        };
      });

      const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        headerToolbar: false,
        dayHeaders: true,
        height: 'auto',
        events: events,
        eventDidMount: function (info) {
          info.el.style.color = 'white';
          info.el.style.borderRadius = '6px';
          info.el.style.fontWeight = 'bold';
          info.el.style.textAlign = 'center';
        }
      });

      calendar.render();
    })
    .catch(error => {
      console.error('Error fetching forecast:', error);
    });
});
  document.getElementById('estimate-btn').addEventListener('click', function() {
    const temp = document.getElementById('weather-data').getAttribute('data-temp');
    const humidity = document.getElementById('weather-data').getAttribute('data-humidity');
    const windSpeed = document.getElementById('weather-data').getAttribute('data-wind-speed');
    const thickness = document.getElementById('thickness').value;
    const url = `http://127.0.0.1:8080/laundry-api/v1/estimate-drying-time?temp=${temp}&humid=${humidity}&wind_kph=${windSpeed}&width=${thickness}`;

    fetch(url)
      .then(response => response.json())
      .then(data => {
        if (data.estimated_drying_time_hours !== undefined) {
          const dryingTime = parseFloat(data.estimated_drying_time_hours);
          const displayTime = dryingTime < 1 ? "< 1 hour" : `${dryingTime} hour${dryingTime === 1 ? '' : 's'}`;
          document.getElementById('drying-time-text').innerText = `Estimated drying time: ${displayTime}`;
        } else {
          document.getElementById('drying-time-text').innerText = 'Failed to estimate drying time. Please try again.';
          document.getElementById('drying-status-image').style.display = 'none';
        }
      })
      .catch(error => {
        console.error('Error estimating drying time:', error);
        document.getElementById('drying-time-text').innerText = 'Error occurred while estimating drying time.';
        document.getElementById('drying-status-image').style.display = 'none';
      });
  });
    let chartInstance;

  function fetchAndRender(metric) {
    fetch('http://127.0.0.1:8080/laundry-api/v1/api/hourly-avg')
      .then(response => response.json())
      .then(data => {
        const labels = data.map(entry => entry.hour).reverse();
        let values;

        if (metric === "temp") {
          values = data.map(entry => entry.avg_temp).reverse();
        } else if (metric === "humidity") {
          values = data.map(entry => entry.avg_humidity).reverse();
        } else if (metric === "wind") {
          values = data.map(entry => entry.avg_wind).reverse();
        }

        const datasets = {
          temp: { label: "Temperature (°C)", borderColor: "#ffd70c" },
          humidity: { label: "Humidity (%)", borderColor: "#66c9df" },
          wind: { label: "Wind Speed (kph)", borderColor: "#e18ec0" }
        };

        const ctx = document.getElementById('weatherChart').getContext('2d');

        if (chartInstance) chartInstance.destroy();

        chartInstance = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [{
              label: datasets[metric].label,
              data: values,
              borderColor: datasets[metric].borderColor,
              fill: false,
              tension: 0.3,
              pointRadius: 4,
              pointHoverRadius: 6
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                labels: { color: "white" }
              }
            },
            scales: {
              x: {
                ticks: { color: "white" }
              },
              y: {
                ticks: { color: "white" }
              }
            }
          }
        });
      })
      .catch(err => console.error("Failed to fetch data:", err));
  }

  document.addEventListener('DOMContentLoaded', function () {
    const selector = document.getElementById('metricSelector');
    fetchAndRender(selector.value);

    selector.addEventListener('change', () => {
      fetchAndRender(selector.value);
    });
  });