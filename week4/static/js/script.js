/* Task 1: Login processing */

// Alert dialog for checkbox
const loginForm = document.getElementById("loginForm");

if (loginForm) {    // Only valid when in index.html
    loginForm.addEventListener("submit", function (e) {
        const checkbox = document.getElementById("agree");

        // Check if the box is checked
        if (!checkbox.checked) {
            e.preventDefault();
            alert("請勾選同意條款");
        }
    });
}



/* Task 4: Hotel search */

// Check if the input is valid and alert the user if it isn't
const hotelForm = document.getElementById("hotelForm");

if (hotelForm) {    // Only valid when in index.html
    hotelForm.addEventListener("submit", function (e) {
        const hotelInput = document.getElementById("hotel_num");

        // Check if the input is postive integer
        if (!/^[1-9]\d*$/.test(hotelInput.value)) {
            e.preventDefault();
            alert("請輸入正整數");
        }
    });
}



// Get user input and navigate to the corresponding page
async function getHotel() {

    // Get user input for hotel id
    const hotelNum = document.getElementById("hotel_num").value;
    // Redirect to /hotel/{hotelNum} page
    window.location.href = `/hotel/${hotelNum}`;
}
