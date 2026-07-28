// clock.js
let count = 0;
setInterval(() => {
  count++;
  document.getElementById('clock').textContent = count;
}, 50);