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
        const month = now.toLocaleString('default', { month: 'long' });

        document.getElementById('current-date').innerHTML =
            `${month}, ${day}`;
   }
   setInterval(updateDate, 1000);