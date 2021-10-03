function getToken(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

var csrftoken = getToken('csrftoken')

function getAllPosts() {
  cuser = GetCurrentUser()
  fetch('/posts')
    .then(response => response.json())
    .then(data => {

      const Div = document.createElement('div');

      data.forEach(function (obj) {

        Div.innerHTML += `
     <div class = "border border-primary" style = "margin:10px">
      <h4 onclick="get_profile(${obj.user_id})">${obj.user}</h4>
      </br>
      <h2>${obj.content}</h2>
      </br>
      ${obj.timestamp}
      </br>
      <button id="like-btn-${obj.id}" style="background-color:white" onclick = "Like(${obj.id})">Like</button>
      <span id="count-btn-${obj.id}">0</span>
      
      </div>`
        // document.querySelector('.index_body').appendChild(Div)
      })
      document.querySelector('.index_body').appendChild(Div)
    })
}

window.onload = getAllPosts()


function get_profile(user_id) {

  document.querySelector('.profile_body').innerHTML = "";
  fetch(`profile/${user_id}`)
    .then(response => response.json())
    .then(data => {
      document.querySelector('.index_body').style.display = 'none';
      document.querySelector('.profile_body').style.display = 'block';
      document.querySelector('.following_posts').style.display = `none`;


      const current_user = GetCurrentUser();


      const Div = document.createElement('div');


      Div.innerHTML = `<h2>Username:  ${data[0].user}</h2> </br>`
      Div.innerHTML += `<div id="followers" style="margin-left:10px">` + followers(user_id) + `</div>`
      Div.innerHTML += `<div id="insert_btn">${insertFollowBtn(user_id)}</div>`





      data.forEach(function (obj) {

        Div.innerHTML += `
       <div class = "border border-primary" style="margin:10px">
        <h4> ${obj.user}</h4> 
         </br>
        <h2>${obj.content}</h2>
         </br>
         ${obj.timestamp} 
         </br>
         
       </div>
     `
      })
      document.querySelector('.profile_body').appendChild(Div)


    })
}

function GetCurrentUser() {
  cuser_id = JSON.parse(document.getElementById('cuser_id').textContent);
  return cuser_id
}

function insertFollowBtn(user_id) {
  const cuser_id = GetCurrentUser();
  if (cuser_id != user_id) {
    fetch(`is_follower/${cuser_id}/${user_id}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.result)
        if (data.result == false) {
          document.querySelector('#insert_btn').innerHTML += `<button  onclick="Followed(${user_id})" class="btn btn-outline-primary" style="margin:10px">Follow</button>`

        } else {
          document.querySelector('#insert_btn').innerHTML += `<button  onclick="unFollowed(${user_id})" class="btn btn-outline-danger" style="margin:10px">Unfollow</button>`

        }
      })
    return ""
  } else {
    return ""
  }
}

function followers(user_id) {
  fetch(`follow/${user_id}`)
    .then(response => response.json())
    .then(data => {
      document.querySelector('#followers').innerHTML += `<strong>Followers: ${data.followers}</strong> </br>`
      document.querySelector('#followers').innerHTML += `<strong>Following: ${data.following}</strong> </br>`
    })

  return ""
}

function Followed(user_id) {
  fetch(`follow/${user_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      cuser_id: user_id
    })
  })
  get_profile(user_id)
}


function unFollowed(user_id) {
  fetch(`unfollow/${user_id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
    },
    body: JSON.stringify({
      cuser_id: user_id
    })
  })
  get_profile(user_id)
}





document.querySelector('#following').addEventListener('click', function () {
  document.querySelector('.following_posts').innerHTML = ''
  fetch('following_posts')
    .then(response => response.json())
    .then(data => {
      document.querySelector('.index_body').style.display = 'none';
      document.querySelector('.profile_body').style.display = 'none';
      document.querySelector('.following_posts').style.display = 'block';
      const Div = document.createElement('div');
      Div.innerHTML = `<h1>Following Posts</h1></br>`

      data.forEach(function (obj) {

        Div.innerHTML += `
     <div class = "border border-primary" style = "margin:10px">
      <h4 onclick="get_profile(${obj.user_id})">${obj.user}</h4>
      </br>
      <h2>${obj.content}</h2>
      </br>
      ${obj.timestamp}
      </br>
     
      </div>`
      })
      document.querySelector('.following_posts').appendChild(Div)
    })
})

function Like(post_id) {
  console.log('hello')
  if (document.querySelector(`#like-btn-${post_id}`).style.backgroundColor == 'white') {
    fetch(`like/${post_id}`, {
      method: "PUT",
      body: JSON.stringify({
        like: true
      })
    })
    document.querySelector(`#like-btn-${post_id}`).style.backgroundColor == "red"
    fetch(`like/${post_id}`)
      .then(response => response.json())
      .then(data => {
        document.querySelector(`#count-btn-${post_id}`).innerHTML = data.likes
      })

  } else {
    fetch(`like/${post_id}`, {
      method: "PUT",

      body: JSON.stringify({
        like: false
      })
    })
    document.querySelector(`#like-btn-${post_id}`).style.backgroundColor == "white"
    fetch(`like/${post_id}`)
      .then(response => response.json())
      .then(data => {
        document.querySelector(`#count-btn-${post_id}`).innerHTML = data.likes
      })
  }


}