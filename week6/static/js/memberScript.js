
/* Fetch API */
// Creare Msg
async function postMessage() {
    // Sent request to backend
    let content = document.getElementById("content").value;

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
    // Sent request to backend
    let response = await fetch("/api/message", {
        method: "GET"
    });

    // Get response from backend
    let result = await response.json();

    if (result.ok) {
        let board = document.getElementById("cards");
        // Clear board 
        board.innerHTML = "";

        const user = "{{ name }}";

        // Create container for each message
        for (let i = result.data.length - 1; i >= 0; i--) {
            
            let card = document.createElement("div");
            card.className = "card";
            
            let msgBlock = document.createElement("div");
            msgBlock.className = "msgBlock";

            let name = document.createElement("span");
            name.className = "msgName";
            name.textContent = result.data[i].name + ": ";
            msgBlock.appendChild(name);

            let msg = document.createElement("span");
            msg.className = "msg";
            msg.textContent = result.data[i].content;
            msgBlock.appendChild(msg);

            card.appendChild(msgBlock);

            if (result.data[i].self) {
                let deleteBtn = document.createElement("button");
                deleteBtn.className = "deleteBtn";
                deleteBtn.textContent = "X";
                deleteBtn.onclick = () => deleteMessage(result.data[i].id);
                
                card.appendChild(deleteBtn);
            }
            
            board.appendChild(card);
        }
    }
}


// Delete Msg
async function deleteMessage(id) {
    
}

getMessages();