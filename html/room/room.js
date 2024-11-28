async function enterToRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  token = await api.getToken()
  await api.enterToRoom(token, id)
}

async function leaveRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  token = await api.getToken()
  await api.leaveRoom(token, id)
  window.location.href = '../list/roomList.html'
}

async function deleteRoom() {
  const api = await import("../modules/api.js")
  const params = new URLSearchParams(window.location.search);
  const id = Number(params.get('id'));
  token = await api.getToken()
  await api.deleteRoom(token, id)
  window.location.href = '../list/roomList.html'
}

enterToRoom()
