window.timeLog = [];
function logTime(label) {
    const time = performance.now().toFixed(1);
    window.timeLog.push({ label, time });
    const el = document.getElementById('log');
    if (el) {
        el.innerHTML = window.timeLog
        .map(e => `<p>${e.label}: ${e.time} ms</p>`)
        .join('');
    }
    console.log(label, time);
}

logTime('log.js code executed');