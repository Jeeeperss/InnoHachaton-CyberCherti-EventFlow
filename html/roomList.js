async function logout(){
  const api = await import("./api.js")
  const token = await api.getToken()
  const result = await api.logout(token)
  if(!result.ok){
    alert(result.statusText)
  }
  window.location.href = 'login.html'
}
