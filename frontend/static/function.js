function setBackgroundColor() {
    const now = new Date();
    const hour = now.getHours();
    let backgroundColor;
    if (hour >= 6 && hour < 12) {
        backgroundColor = "linear-gradient(334deg,rgba(55, 132, 184, 1) 50%, rgba(247, 247, 200, 1) 100%)";
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

    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'dayGridMonth',
      headerToolbar: false,
      dayHeaders: true,
      height: 'auto',
      events: [
        { title: '☀️ Sunny', date: '2025-04-20', backgroundColor: '#FFD700' },
        { title: '🌧️ Rainy', date: '2025-04-21', backgroundColor: '#00BFFF' },
        { title: '☁️ Cloudy', date: '2025-04-22', backgroundColor: '#B0C4DE' },
        { title: '🌩️ Storm', date: '2025-04-23', backgroundColor: '#8B0000' }
      ],
      eventDidMount: function(info) {
        info.el.style.color = 'white';
        info.el.style.borderRadius = '6px';
        info.el.style.fontWeight = 'bold';
        info.el.style.textAlign = 'center';
      }
    });

    calendar.render();
  });
  const ctx = document.getElementById('tempTrendChart').getContext('2d');

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: ['05:00', '06:00', '06:01', '07:00', '08:00', '09:00'],
      datasets: [{
        data: [28, 28, null, 29, 30, 32],
        borderColor: '#ffffff',
        backgroundColor: 'rgba(255, 255, 255, 0.05)',
        fill: false,
        tension: 0.3,
        pointBackgroundColor: '#ffffff',
        pointRadius: 3,
        spanGaps: true
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { display: false },
        x: { display: false }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false }
      }
    }
  });