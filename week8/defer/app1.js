const el = document.getElementById("app");
setTimeout(() => {
  el.textContent = doSomething();
}, 2000);