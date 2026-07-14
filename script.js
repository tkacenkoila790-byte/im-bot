const tg = window.Telegram.WebApp;
tg.expand();

// Встроенный ваш Telegram ID
const ADMIN_ID = 8455479648; 

const balanceAmountElement = document.querySelector('.balance-amount');
const statusElement = document.querySelector('.status');
const user = tg.initDataUnsafe?.user;

if (user) {
    if (Number(user.id) === ADMIN_ID) {
        balanceAmountElement.innerText = "∞ USD";
        statusElement.innerText = (user.first_name || "Админ") + " (Владелец)";
    } else {
        balanceAmountElement.innerText = "0.00 USD";
        statusElement.innerText = user.first_name || "Пользователь";
    }
} else {
    balanceAmountElement.innerText = "0.00 USD";
    statusElement.innerText = "Гость";
}

function toggleSettings() {
    const modal = document.getElementById('settingsModal');
    modal.style.display = modal.style.display === 'flex' ? 'none' : 'flex';
}

function changeTheme() {
    const theme = document.getElementById('themeSelect').value;
    if (theme === 'light') {
        document.body.classList.remove('dark-theme');
        document.body.classList.add('light-theme');
    } else {
        document.body.classList.remove('light-theme');
        document.body.classList.add('dark-theme');
    }
}

function openP2P() {
    alert("Открытие P2P Маркета: здесь пользователи смогут размещать свои объявления об обмене.");
}

let gameInterval;
function startRocket() {
    clearInterval(gameInterval);
    const rocket = document.getElementById('rocket');
    const multiplierText = document.getElementById('multiplier');
    
    let currentMultiplier = 1.00;
    let posX = 10;
    let posY = 10;

    rocket.style.transform = `translate(0px, 0px) rotate(0deg)`;
    const crashPoint = (Math.random() * 4 + 1.1).toFixed(2);

    gameInterval = setInterval(() => {
        currentMultiplier += 0.02;
        multiplierText.innerText = currentMultiplier.toFixed(2) + 'x';

        if (posX < 220) posX += 2.0;
        if (posY < 110) posY += 1.3;
        
        rocket.style.bottom = `${10 + posY}px`;
        rocket.style.left = `${10 + posX}px`;
        rocket.style.transform = `rotate(-20deg)`;

        if (currentMultiplier >= crashPoint) {
            clearInterval(gameInterval);
            multiplierText.style.color = '#e74c3c';
            multiplierText.innerText = `ВЗРЫВ: ${currentMultiplier.toFixed(2)}x`;
            rocket.style.transform = `scale(0) rotate(0deg)`;
            
            setTimeout(() => {
                multiplierText.style.color = '#2ecc71';
                multiplierText.innerText = '1.00x';
                rocket.style.bottom = '10px';
                rocket.style.left = '10px';
                rocket.style.transform = `scale(1) rotate(0deg)`;
            }, 2000);
        }
    }, 50);
}
