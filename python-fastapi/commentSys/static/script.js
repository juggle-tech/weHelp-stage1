// 新增留言
async function postMessage() {
    let name = document.querySelector("#name").value;
    let content = document.querySelector("#content").value;
    let response = await fetch("/api/message", {
        method: "POST",
        body: JSON.stringify({ "author": name, "content": content}
        )
    });
    
    // 取得 {"OK": True} if success
    let result = await response.json();
    if (result.ok) {
        console.log("送出成功，準備重新取得留言");
        getMessages();
    }
}


// 取得留言
async function getMessages() {
    let response = await fetch("/api/message", {
        method: "GET"
    });

    let result = await response.json();
    let board = document.getElementById("board");
    board.innerHTML = "";

    for (let i = result.length - 1; i >= 0; i--) {
        let card = document.createElement("div");
        card.className = "message-card";

        let authorEl = document.createElement("p");
        authorEl.className = "message-author";
        authorEl.textContent = result[i].author;

        let contentEl = document.createElement("p");
        contentEl.className = "message-content";
        contentEl.textContent = result[i].content;

        let deleteBtn = document.createElement("button");
        deleteBtn.className = "delete-btn";
        deleteBtn.textContent = "X";
        deleteBtn.onclick = () => deleteMessage(result[i].id);

        card.appendChild(deleteBtn);
        card.appendChild(authorEl);
        card.appendChild(contentEl);
        board.appendChild(card);
    }
}


// 刪除留言
async function deleteMessage(id) {
    let response = await fetch("/api/message/" + id, {
        method: "DELETE"
    });

    let result = await response.json();
    if (result.ok) {
        getMessages(); // 刪除成功後重新取得最新留言列表
    }
}

getMessages();
