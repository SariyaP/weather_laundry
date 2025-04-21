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
  if (!condition) return {
    title: '❓',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };

  condition = condition.toLowerCase();

  if (condition.includes('sunny')) return {
    title: '☀️',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };

  if (condition.includes('rain')) return {
    title: '🌧️',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };

  if (condition.includes('storm')) return {
    title: '🌩️',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };

  if (condition.includes('cloud')) return {
    title: '☁️',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };

  return {
    title: '⛅',
    backgroundColor: 'transparent',
    borderColor: 'transparent',
    textColor: 'white'
  };
}


  fetch('http://127.0.0.1:8080/laundry-api/v1/forecast-weather-conditions')
    .then(response => response.json())
    .then(data => {
      const events = data.map(entry => {
        const style = getConditionStyle(entry.predicted_condition);
        return {
          title: style.title,
          date: entry.date,
          backgroundColor: style.backgroundColor,
          borderColor: style.borderColor,
          textColor: style.textColor,
            className: 'weather-icon-event'
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
      },
      dateClick: function (info) {
      //     modify to add click on calendar, show anything yay :D
          alert("You clicked on: " + info.dateStr);
      }
    });


      calendar.render();
    })
    .catch(error => {
      console.error('Error fetching forecast:', error);
    });
});