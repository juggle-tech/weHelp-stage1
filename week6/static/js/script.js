
/* Prevent emtpy input in signup form */
document.getElementById("signUpForm").addEventListener("submit", function(e) {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email1").value.trim();
    const pwd = document.getElementById("pwd1").value.trim();

    if (!name || !email || !pwd) {
        e.preventDefault();
        alert("No empty input allowed!")
        return;
    }
});


/* Prevent emtpy input in login form */
document.getElementById("loginForm").addEventListener("submit", function(e) {
    const email = document.getElementById("email2").value.trim();
    const pwd = document.getElementById("pwd2").value.trim();

    if (!email || !pwd) {
        e.preventDefault();
        alert("Email and password can not be empty!");
        return;
    }
});