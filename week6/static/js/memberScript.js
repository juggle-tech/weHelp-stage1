
/* Fetch API */
// Creare Msg
async function postMessage() {
    // Sent request to backend
    let content = document.getElementById("content").value;
    console.log(content)

    let response = await fetch("/api/message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "content": content
        })
    });

    // Get response from backend
    let result = await response.json();
    if (result.ok) {
        document.getElementById("content").value = "";
        getMessages();
    }
}


// Get Msg
async function getMessages() {
    
}


// Delete Msg
async function deleteMessage(id) {
    
}

getMessages();