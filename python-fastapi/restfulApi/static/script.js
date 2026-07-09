// 新增留言
async function postMessage() {
    let response = await fetch("/api/message", {
        method: "POST",
        // 資料是寫死的，按按鈕後會存取下面的內容
        body: JSON.stringify({
            "author": "jung", 
            "content": "Test"}
        )
    });
    
    // 取得 {"OK": True} if success
    let result = await response.json();
    console.log(result);
}


// 取得留言
async function getMessages() {
    let response = await fetch("/api/message", {
        method: "GET"
    });

    let result = await response.json();
    console.log(result);
}


// 刪除留言
async function deleteMessage() {
    let response = await fetch("/api/message/2", {
        method: "DELETE"
    });

    let result = await response.json();
    console.log(result);
}
