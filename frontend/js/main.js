
function addLogin(){
    let nav = document.getElementById("nav-form")
    let login_btn = document.createElement("button")
    let logout_btn = document.getElementById("logout_btn")
    let upload_btn = document.getElementById("upload_btn")

    login_btn.className = "btn btn-outline-success me-2"
    login_btn.type = "submit"
    login_btn.textContent = "Login"
    login_btn.id = "login_btn"
    login_btn.setAttribute("onclick", "login()")

    nav.removeChild(upload_btn)
    nav.removeChild(logout_btn)
    nav.appendChild(login_btn)
}

function login(){
    // var endUpload = fetch("http://127.0.0.1:5000/login", 
    //     {
    //         method: 'GET',
    //         headers: { 'Content-Type': 'application/json' }
    //     })
    //     .then(response => response.json())
    //     .then(jsonResponse=> {
    //         window.location.href = jsonResponse['response']
    //         console.log(jsonResponse)
    //     })
    //     .catch((err) => console.error(err));
    
    addLogout()
}

//document.getElementById("inputGroupFile02").addEventListener('change', 

async function upload (){
        const video_title = document.getElementById("video_title")
        const screenshot = document.getElementById("screenshot").files[0]
        const file = document.getElementById("inputGroupFile02").files[0]
        const chunksText = document.getElementById("video-information")
        const uploadBody = document.getElementById("uploading")
        const progressBar = document.createElement("div")
        const progressBarInner = document.createElement("div")

        const chunkSize = 1024*1024*10; //10MB 
        var numberOfChunks = Math.ceil(file.size/chunkSize);
        const upload_id = file.name+numberOfChunks
        var start=0; 
        var chunkEnd = Math.min.apply(null,[start + chunkSize , file.size])

        progressBarInner.setAttribute("class", "progress-bar bg-success")
        progressBarInner.setAttribute("style", "width: 6.25%")
        progressBar.setAttribute("class","progress")
        progressBar.setAttribute("role", "progressbar")
        progressBar.setAttribute("aria-label", "Success example")
        progressBar.setAttribute("aria-valuenow", "25")
        progressBar.setAttribute("aria-valuemin", "0")
        progressBar.setAttribute("aria-valuemax", "100")
        progressBar.appendChild(progressBarInner)

        console.log("Start:")

        let title = video_title.value.toLowerCase().replaceAll(" ","_")
        let ext = file.name.split(".")
        ext = ext[ext.length-1]
        let filename = title+"."+ext

        console.log(file)

        var uploadStart = await fetch("http://127.0.0.1:5000/upload_start", {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                filename:filename
            })
        })
            .then(response => response.json())
            .then(jsonResponse=> console.log(jsonResponse))
            .catch((err) => console.error(err));

        perc = parseFloat(Math.ceil(100/numberOfChunks));
        percWidth = perc
        chunksText.innerHTML = "There will be " + numberOfChunks + " chunks uploaded "
        uploadBody.appendChild(progressBar)

        for (let i=1; i<=numberOfChunks; i++){
            const blobData = file.slice(start, start+chunkSize, contentType="video/mp4");
            start += chunkSize

            const blobToBase64 = blob => {
                const reader = new FileReader();
                reader.readAsDataURL(blob);
                return new Promise(resolve => {
                  reader.onloadend = () => {
                    resolve(reader.result);
                  };
                });
              };
            var res = await blobToBase64(blobData)
            let new_res = res.split(/,(.*)/s)[1]

            const requestOptions = {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body:JSON.stringify({
                    chunk: new_res,
                    total_chunks:numberOfChunks,
                    chunk_index:i,
                    upload_id:upload_id
                })
            };

            var response = await fetch("http://127.0.0.1:5000/upload_parts", requestOptions)
                    .then(response => response.json())
                    .then(jsonResponse=> {
                        percWidth = Math.min.apply(null,[percWidth,100])
                        progressBarInner.style.width = percWidth + "%";
                        progressBarInner.innerHTML = percWidth + "%";
                        percWidth += perc
                        console.log(jsonResponse)
                    })
                    .catch((err) => console.error(err));
            
            console.log("chunk: "+i)
            //uploadPromises.push(response)

        }

        const blobToBase64 = blob => {
            const reader = new FileReader();
            reader.readAsDataURL(blob);
            return new Promise(resolve => {
                reader.onloadend = () => {
                resolve(reader.result);
                };
            });
            };
        var result = await blobToBase64(screenshot)
        
        let ext_img = screenshot.name.split(".")
        ext_img = ext_img[ext_img.length-1]
        let filename_img = title+"_screenshot."+ext_img

        var endUpload = await fetch("http://127.0.0.1:5000/upload_end", 
        {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {   filename:filename_img,
                    title:video_title.value,
                    screenshot:result
                })
        })
                .then(response => response.json())
                .then(jsonResponse=> console.log(jsonResponse))
                .catch((err) => console.error(err));
            
        console.log("End:")   
};

function addLogout(){
    let nav = document.getElementById("nav-form")
    let login_btn = document.getElementById("login_btn")
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

    nav.removeChild(login_btn)
    nav.appendChild(upload_btn)
    nav.appendChild(logout_btn)
}


function addItem(title,thumbnail,id,url){
    
    let mainArea = document.getElementById("main-area")
    var novoItem = document.createElement('div'); 
    
    novoItem.innerHTML = `<div class='child float-left-child'>
        <div class="card" style="width: 18rem;">
            <img class="card-img-top" width="286" height="180" src="${thumbnail}" alt="Card image cap"> 
            <div class="card-body">
                <a id="id_${id}" onclick="watchVideo('${url}')" href="#" class="btn btn-primary d-grid gap-2 justify-content-md-end">
                    <svg xmlns="http://www.w3.org/2000/svg" width="25" height="25" fill="currentColor" class="bi bi-play-btn" viewBox="0 0 16 16">
                        <path d="M6.79 5.093A.5.5 0 0 0 6 5.5v5a.5.5 0 0 0 .79.407l3.5-2.5a.5.5 0 0 0 0-.814z"/>
                        <path d="M0 4a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm15 0a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v8a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1z"/>
                    </svg>
                </a>
                <p class="card-title fw-semibold">${title}</p>
            </div>
        </div>
    </div>  `
    mainArea.prepend(novoItem)
}

function addVideos(jsonResponse){

    for (let resp in jsonResponse){
        let title = jsonResponse[resp]["title"]
        let id = jsonResponse[resp]["id"]
        let url = jsonResponse[resp]["url"]

        let thumbnail = jsonResponse[resp]["screenshot"];
        if (jsonResponse[resp]["screenshot"] == null){
            thumbnail = "download.svg" 
        }
        
        addItem(title, thumbnail, id, url)
    }

}

function index(){
    let main = document.getElementById("main-area")
    let main_watch = document.getElementById("main-area-watch")

    let btn_main_watch = document.getElementById("btn_main_watch")
    var video = document.getElementById("video")
    var source = document.getElementById("source")

    main.style.display = "block";

    main_watch.removeChild(btn_main_watch)
    main_watch.removeChild(video)
}

function watchVideo(url){

    let main = document.getElementById("main-area")
    let main_watch = document.getElementById("main-area-watch")
    let btn_main_watch = document.createElement("button")
    var video = document.createElement("video")
    var source = document.createElement("source")
    main.style.display = "none";

    btn_main_watch.textContent = "Back"
    btn_main_watch.setAttribute("onclick", "index()")
    btn_main_watch.id = "btn_main_watch"
    btn_main_watch.className = "btn btn-outline-success me-2"

    source.src = url
    source.type = "video/mp4"
    source.id = "source"
    video.setAttribute("controls","controls") 
    video.appendChild(source);
    video.id = "video"
    video.setAttribute("autoplay", "autoplay")
    
    main_watch.appendChild(btn_main_watch)
    main_watch.appendChild(video)

}


fetch("http://127.0.0.1:5000/", 
    {
        method: 'GET',
        headers: {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        },
    }).then(res=>{
            if(res.ok){
                return res.json()
            }else{
                alert("something is wrong")
            }
    }).then(jsonResponse=>{
            addVideos(jsonResponse)
            console.log(jsonResponse)
            
    }).catch((err) => console.error(err));
        