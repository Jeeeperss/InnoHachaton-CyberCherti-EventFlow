const updateInterval = 5

const image = document.getElementById('generateImage');
const PasswordWindow = document.getElementById('PasswordWindow');
const PasswordForm = document.getElementById('PasswordForm');

const params = new URLSearchParams(window.location.search);
const id = Number(params.get('id'));

async function start() {
  const api = await import("../modules/api.js")
  const token = await api.getToken()
  const rooms = await api.getRooms()

  for(let i = 0; i < rooms.length; i++) {
    if (rooms[i].id === id){
      if (!rooms[i].is_active){//проверка активности комнаты
        alert('Room is not active!')
        window.location.href = '../list/roomList.html'
        return
      }
      
      const me = await api.getMe(token)//проверка необходимости входа
      const users = await api.getMembers(id)
      for(let i = 0; i < users.length; i++){
        if(users[i].email === me.email){ 
          setInterval(updateIteration, updateInterval * 1000);
          startWebSocket()
          return 
        }
      }

      //проверка пароля
      if(rooms[i].private){
        requestPassword()
      } else enterToRoom('')
          
    }
  }
}

function requestPassword(){
  PasswordWindow.style.display = "flex"
  PasswordForm.addEventListener('submit', function(event){
    event.preventDefault();
    PasswordWindow.style.display = "none"
    enterToRoom(PasswordForm.inputPassword.value)
  })
}


async function enterToRoom(password) {
  try{
    const api = await import("../modules/api.js")
    const token = await api.getToken()
    await api.enterToRoom(token, id, password)
    start()
    return
  } catch {
    alert("Error entering the room")
    window.location.href = '../list/roomList.html'
    return
  }
}

async function startWS() {
  setInterval(updateIteration, updateInterval * 1000);
  startWebSocket()
}

async function leaveRoom() {
  const api = await import("../modules/api.js")
  const token = await api.getToken()
  await api.leaveRoom(token, id)
  window.location.href = '../list/roomList.html'
}

async function deleteRoom() {
  const api = await import("../modules/api.js")
  const token = await api.getToken()
  await api.deleteRoom(token, id)
  window.location.href = '../list/roomList.html'
}

function updateIteration(){
  image.style.display = "flex"
  fetch(`/images/image_room_${id}.png?t=${new Date().getTime()}`)
      .then(response => response.blob())
      .then(blob => {
          const url = URL.createObjectURL(blob);
          image.src = url; // Устанавливаем новый источник для изображения
      })
      .catch(err => console.error('Error fetching image:', err));
}

start()
