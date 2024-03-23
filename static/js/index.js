let btn = document.getElementById("btn");
let res = document.getElementById("res");
let information = document.querySelector(".videos-information");
let container = document.querySelector(".form .container");
let input = document.getElementById("video-link");

btn.addEventListener('click', function () {
  if (input.value !== "") {
    if (input.value.match(/(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]{11})/)) {
      getDataVideo(input.value);
    } else {
      getPlayList(input.value);
    }
  }

  input.value = "";
});


function getDataVideo(url) {
  let enco = encodeURIComponent(url)
  fetch(`http://127.0.0.1:9000/download/video?url=${enco}&resolution=${res.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
  }).then(response => {
    if (!response.ok) {
      throw new Error("NetWork not 200 ok");
    }
    
      return response.json()
  }).then(data => {
    let info = document.createElement("div");
    info.className = "info";
    let image = document.createElement("div");
    image.className = "image";
    let img = document.createElement("img");
    img.src = data.thumbnail_url;
    img.alt = `Video pic`;
    let title_video = document.createElement("div");
    title_video.className = "title-video";
    let title = document.createElement("h5");
    title.className = "title";
    title.innerHTML = data.title

    // Append
    image.appendChild(img)
    title_video.appendChild(title)
    info.appendChild(image)
    info.appendChild(title_video)

    information.appendChild(info)

    // Create Message
    let message = document.createElement("div")
    message.className = "message"
    message.innerHTML = `${data.message}`

    container.appendChild(message)
  }).catch(error => {
    console.log(error)
  })
}


function getPlayList(url) {

  let enco = encodeURIComponent(url)
  fetch(`http://127.0.0.1:9000/download/play_list?url=${enco}&resolution=${res.value}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
  }).then(response => {
    if (!response.ok) {
      throw new Error("NetWork not 200 ok");
      }
      return response.json()
  }).then(data => {
    result = data.downloaded_videos;
    for (let i = 0; i < result.length; i++) {
        let info = document.createElement("div");
        info.className = "info";

        let image = document.createElement("div");
        image.className = "image";

        let img = document.createElement("img");
        img.src = result[i].thumbnail_url;
        img.alt = `Video pic`;

        let title_video = document.createElement("div");
        title_video.className = "title-video";

        let title = document.createElement("h5");
        title.className = "title";
        title.innerHTML = result[i].title

        // Append
        image.appendChild(img)
        title_video.appendChild(title)
        info.appendChild(image)
        info.appendChild(title_video)

        information.appendChild(info)

    }
    // Create Message
        let message = document.createElement("div")
        message.className = "message"
        message.innerHTML = `${result.message}`

        container.appendChild(message)
  }).catch(error => {
    console.log(error)
  })
}
