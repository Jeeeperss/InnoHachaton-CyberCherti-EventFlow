const animateMenu = document.getElementById('animateMenu');
const loginForm = document.getElementById('loginForm')
const registrationForm = document.getElementById('registrationForm')

function toLogin() {
  animateMenu.style.animation = `toLogin 2s forwards`;  
}

function toRegister() {
  animateMenu.style.animation = `toRegister 2s forwards`;  
}

loginForm.addEventListener('submit', async function(event) {
  event.preventDefault();
  const api = await import("./api.js")
  const result = await api.login(loginForm.email.value, loginForm.password.value)
  console.log(result)

  if(result.detail == undefined){
    localStorage.setItem('access_token', result.access_token);
    window.location.href = 'roomList.html';
  } else
  if (result.detail === 'LOGIN_BAD_CREDENTIALS'){
    alert('Incorrect login or password!')
  } else {
    alert(result.detail[0].msg)
  }

})

registrationForm.addEventListener('submit', async function(event) {
  event.preventDefault();
  if (registrationForm.password.value === registrationForm.retypePassword.value){
    const api = await import("./api.js")
    const result = api.register(registrationForm.email.value, registrationForm.password.value)
    console.log(result)

    if(result.detail == undefined){
      alert(`Registration Successfully\n${result.email}`);
      toLogin();
    } else
    if (result.detail === 'REGISTER_USER_ALREADY_EXISTS'){
      alert('Register user already exists!')
    } else {
      alert(result.detail[0].msg)
    }
  } else {
    alert("Passwords do not match")
  }
});

document.addEventListener("DOMContentLoaded", () => {
  const textBoxes = document.querySelectorAll('.text-box');
  
  textBoxes.forEach((box, index) => {
      setTimeout(() => {
          box.style.transform = 'translateY(-50%) translateX(-10px)'; 
          box.style.opacity = '1'; 
      }, index * 1500); 
  });
});
