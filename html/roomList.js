const roomList = document.getElementById('roomList')

document.querySelector('.dropdown-toggle').addEventListener('click', function () {
  const dropdown = document.querySelector('.dropdown');
  dropdown.classList.toggle('open');
});



async function logout(){
  const api = await import("./api.js")
  const token = await api.getToken()
  const result = await api.logout(token)
  if(!result.ok){
    alert(result.statusText)
  }
  window.location.href = 'login.html'
}

async function createRoom(password, opening_time) {
  const api = await import("./api.js")
  try{
    const token = await api.getToken()
    const result = await api.logout(token, password, opening_time)
    
    console.log(result)
    if(result.ok){
      //переход в комнату
      updateRooms()
    }
    else {
      alert(`Request error:\n${result.statusText}`)
    }
  }
  catch (e) {
    alert(`Error creation rooms:\n${e}`)
  }
}

async function deleteRoom (room_id){
  const api = await import("./api.js")
  const token = await api.getToken()
  const result = await api.deleteRoom(token, room_id)
  console.log(result)
}

async function getToken (){
  const api = await import("./api.js")
  const token = await api.getToken()
  return(token)
}

async function getRooms() {
  const api = await import("./api.js")
  try{
    Rooms = await api.getRooms()
    return(Rooms)
  }
  catch (e) {
    alert(`Error getting rooms:\n${e}`)
    return([])
  }
}

async function updateRooms() { 
  let Rooms = await getRooms() 
  Rooms.push({
    //temp example
    "id":0,
    "is_active": true,
    "opening_time": "2024-11-26 14:15",
    "private": true
  })
  Rooms.push({
    //temp example
    "id":0,
    "is_active": true,
    "opening_time": "2024-11-26 14:15",
    "private": false
  })
  Rooms.push({
    "id":0,
    "is_active": false,
    "opening_time": "2024-11-26 14:15",
    "private": false
  })
  Rooms.push({
    "id":0,
    "is_active": false,
    "opening_time": "2024-11-26 14:15",
    "private": true
  })

  Rooms.forEach(room => {
    const roomDiv = document.createElement('div');
    roomDiv.className = `room ${room.is_active ? 'active' : 'inactive'} ${room.private ? 'private' : ''}`;
    // Opening Time
    const roomTime = document.createElement('div');
    roomTime.className = 'roomTime';
    roomTime.innerText = `Open: ${room.opening_time}`;
    roomDiv.appendChild(roomTime);

    roomList.appendChild(roomDiv);
});

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
  }
}

updateRooms()
