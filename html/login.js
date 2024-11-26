const animateMenu = document.getElementById('animateMenu');

function toLogin() {
  animateMenu.style.animation = `toLogin 2s forwards`;  
}

function toRegister() {
  animateMenu.style.animation = `toRegister 2s forwards`;  
}

import("./settings.js").then((settings) => {
  const registrationForm = document.getElementById('registrationForm')
  registrationForm.addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    if (registrationForm.password.value === registrationForm.retypePassword.value){
      const response = await fetch(`${settings.api_server}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: registrationForm.email.value,
          password: registrationForm.password.value
        })
      });
      const result = await response.json();
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
}).catch(error => {
    console.error("Import ERROR:", error);
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
