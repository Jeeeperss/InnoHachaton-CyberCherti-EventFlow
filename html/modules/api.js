//AUTH
export async function login(email, password) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    credentials: 'include',  });
  return(await response.json());
}

export async function logout(token) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/auth/logout`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    }
  });
  return(await response);
}

export async function register(email, password) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email: email,
      password: password
    })
  });
  return(await response.json());
}

export function getToken(){
  return(localStorage.getItem('access_token'));
}

//ROOM
export async function createRoom(token, password, opening_time) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/room/?password=${encodeURIComponent(password)}&${opening_time ? `opening_time=${encodeURIComponent(opening_time)}`:''}`,
  {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
  });
  return(await response.json());
}

export async function getRooms() {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/room`, {
    method: 'GET'
  });
  return(await response.json());
} 

export async function deleteRoom(token, room_id) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/room/?room_id=${encodeURIComponent(room_id)}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return(await response.json());
}

//MEMBERS
export async function getMembers(room_id) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/members/${encodeURIComponent(room_id)}`, {
    method: 'GET' 
  });
  return(await response.json());
}

export async function enterToRoom(token, room_id, password='') {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/members/enter/${encodeURIComponent(room_id)}?password=${encodeURIComponent(password)}`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return(await response.json());
}

export async function leaveRoom(token, room_id) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/members/leave/${encodeURIComponent(room_id)}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return(await response.json());
}

//USERS
export async function getMe(token) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/users/me`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return(await response.json());
}

//IMAGE
export async function generateImage(room_id) {
  const settings = await import("./settings.js")
  const response = await fetch(`${settings.api_server}/image/generate?room_id=${room_id}`, {
    method: 'GET'
  });
  return(await response.json());
}
