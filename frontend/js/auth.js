
async function handleCredentialResponse(response) {
    const data = jwt_decode(response.credential)

    await fetch("http://127.0.0.1:5000/login", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            token:response.credential
        })
    })
        .then(response => response.json())
        .then(jsonResponse=> {
            localStorage.setItem("access_token_cookie",jsonResponse["access_token"]);    
            addLogout();
        });   
    }

function loginButton(){
    google.accounts.id.renderButton(
        document.getElementById("buttonDiv"),
        { 
          theme: "outline", 
          size: "large"
        }  // customization attributes
      );
}

window.onload = function(){

    google.accounts.id.initialize({
      client_id: process.env.CLIENT_ID,
      callback: handleCredentialResponse
    });

    loginButton();
    google.accounts.id.prompt(); // also display the One Tap dialog
}

function addLogin(){
    let nav = document.getElementById("nav-form")
    let login_btn = document.createElement("div")
    let logout_btn = document.getElementById("logout_btn")
    let upload_btn = document.getElementById("upload_btn")

    login_btn.id = "buttonDiv"

    nav.removeChild(upload_btn)
    nav.removeChild(logout_btn)
    nav.appendChild(login_btn)

    loginButton();

    fetch("http://127.0.0.1:5000/logout", 
    {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(jsonResponse=> {
        console.log(jsonResponse)
    })

    localStorage.removeItem("access_token_cookie");
}


function addLogout(){
    let nav = document.getElementById("nav-form")
    let buttonDiv = document.getElementById("buttonDiv")
    let logout_btn = document.createElement("button")
    let upload_btn = document.createElement("button")

    upload_btn.className = "btn btn-outline-success me-2"
    upload_btn.type = "button"
    upload_btn.textContent = "Upload"
    upload_btn.id = "upload_btn"
    upload_btn.setAttribute("data-bs-toggle", "modal")
    upload_btn.setAttribute("data-bs-target", "#exampleModal")

    logout_btn.className = "btn btn-outline-success"
    logout_btn.type = "submit"
    logout_btn.textContent = "Logout"
    logout_btn.id = "logout_btn"
    logout_btn.setAttribute("onclick", "addLogin()")

    nav.removeChild(buttonDiv)
    nav.appendChild(upload_btn)
    nav.appendChild(logout_btn)
}