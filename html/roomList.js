const roomList = document.getElementById('roomList')

async function logout(){
  const api = await import("./api.js")
  const token = await api.getToken()
  const result = await api.logout(token)
  if(!result.ok){
    alert(result.statusText)
  }
  window.location.href = 'login.html'
}

let Rooms = []

async function updateRooms() {
  const api = await import("./api.js")
  Rooms = await api.getRooms()
  Rooms.push({
    //temp example
    "id":0,
    "opening_time": "2024-11-26 14:15",
    "is_active": true
  })
  Rooms.push({
    "id":0,
    "opening_time": "2024-11-26 14:15",
    "is_active": false
  })

  
  for(let i = 0; i < Rooms.length; i++){
    const roomDiv = document.createElement('div');
    const idDiv = document.createElement('div');
    const timeDiv = document.createElement('div');
    const statusDiv = document.createElement('div');
    const typeDiv = document.createElement('div');
    
    roomDiv.addEventListener('click', function() {
      const id = Rooms[i].id
      console.log(id);
    });

    idDiv.textContent = Rooms[i].id;
    timeDiv.textContent = Rooms[i].opening_time;
    statusDiv.textContent = Rooms[i].is_active;
    typeDiv.textContent = "public";
    
    roomDiv.className = 'room';
    idDiv.className = "roomId";
    timeDiv.className = "roomTime";
    statusDiv.className = "roomStatus";
    typeDiv.className = "roomType";
    
    roomList.appendChild(roomDiv);
    roomDiv.appendChild(idDiv)
    roomDiv.appendChild(timeDiv)
    roomDiv.appendChild(statusDiv)
    roomDiv.appendChild(typeDiv)

     
  }
}

updateRooms()
