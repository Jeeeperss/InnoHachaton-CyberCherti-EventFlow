async function enterToRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
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
        if(users[i].email === me.email){ return }
      }

      let password = ''//проверка пароля
      if(rooms[i].private){
        password = prompt("Password:")
      }
      try{
        await api.enterToRoom(token, id, password)
        return
      } catch {
        alert("Error entering the room")
        window.location.href = '../list/roomList.html'
      }
    }
  }
}

async function leaveRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  const token = await api.getToken()
  await api.leaveRoom(token, id)
  window.location.href = '../list/roomList.html'
}

async function deleteRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  const token = await api.getToken()
  await api.deleteRoom(token, id)
  window.location.href = '../list/roomList.html'
}

enterToRoom()
