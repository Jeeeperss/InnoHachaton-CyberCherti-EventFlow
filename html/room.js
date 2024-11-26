const table = document.getElementById('table');
const wardrobe = document.getElementById('wardrobe');
const inputPersone = document.getElementById('inputPersone');


function createPeople(peopleCount) {
  people=[]
  const angleIncrement = 360 / peopleCount;
  for (let i = 0; i < peopleCount; i++) {
      const personDiv = document.createElement('div');
      personDiv.classList.add('person');
      personDiv.innerText = i + 1;

      const angle = angleIncrement * i;
      const x = 150 * Math.cos(angle * Math.PI / 180);
      const y = 150 * Math.sin(angle * Math.PI / 180);

      personDiv.style.transform = `translate(${x}px, ${y}px)`;
      personDiv.style.setProperty('--initial-angle', angle + 'deg');//Начальный угол относительно стола
      personDiv.style.setProperty('--initial-angle-reverse', -angle + 'deg');

      table.appendChild(personDiv);
      person = {
        div: personDiv,
        angle: angle
      }
      people.push(person);
  }
return people
}

function goToCords(personIndex, X, Y) {
    if (Number(personIndex) < 1 || Number(personIndex) > peopleList.length){
      return
    }
    const person = people[personIndex-1];
    const personDiv = person.div;
    
    let angle = (Math.atan(Y/X) / Math.PI) * 180
    
    personDiv.style.setProperty('--destination-angle', angle + 'deg');
    personDiv.style.setProperty('--destination-angle-reverse', -angle + 'deg');
    personDiv.style.setProperty('--destination-radius', Math.sqrt((Y*Y)+(X*X)) + 'px');
    personDiv.style.animation = `moveToCords 5s forwards`; 

    // Через 5 секунд возвращаем человека назад
    setTimeout(() => {
        personDiv.style.animation = '';
    }, 5000);
}

let peopleList = createPeople(7)
