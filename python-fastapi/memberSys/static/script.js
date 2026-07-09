// 註冊帳號
async function signup() {

    let name = document.querySelector("#signup-name").value;
    let email = document.querySelector("#signup-email").value;
    let password = document.querySelector("#signup-password").value;

    let response = await fetch("/api/member", {
        method: "POST", 
        // 壓成字串傳出去
        body: JSON.stringify({"name": name, "email": email, "password": password})
    })
    
    // response = 這次 HTTP 回應的物件 (包含了狀態碼(status)、標頭(headers)、以及尚未解析的回應內容)
    // 後端傳回來的 HTTP 回應內容,解析成 JavaScript 可以直接操作的物件,
    let result = await response.json();
    if (result.ok) {
        alert("註冊成功");
    } else {
        alert("註冊失敗");
    }
}


// 登入帳號
async function signin() {

    let email = document.querySelector("#signup-email").value;
    let password = document.querySelector("#signup-password").value;

    let response = await fetch("/api/member/auth", {
        method: "PUT",
        body: JSON.stringify({"email": email, "password": password})
    })

    let result = await response.json();
    if (result.ok) {
        window.location = "/member.html";   // 導向會員頁面
    } else {
        alert("登入失敗");
    }
}


// 檢查登入狀態
async function checkStatus() {
    let response = await fetch("/api/member/auth", {
        method: "GET",
    });

    let result = await response.json();
    if (result.ok) {    // 使用者已登入，顯示登入身分
        document.querySelector("#name").textContent = result.name;
    } else {
        window.location = "/";   // 強迫回首頁
    }
}

checkStatus();

