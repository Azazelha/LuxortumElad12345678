// Функції для роботи з індикатором настрою світу

/**
 * Оновлює відображення настрою світу на сторінці
 * @param {Object} data - Дані про настрій світу з API
 */
function updateWorldMoodDisplay(data) {
    // Оновлюємо назву та емодзі настрою
    const moodName = document.getElementById('mood-name');
    const moodEmoji = document.getElementById('mood-emoji');
    
    if (moodName) moodName.textContent = getMoodName(data.mood);
    if (moodEmoji) moodEmoji.textContent = getMoodEmoji(data.mood);
    
    // Оновлюємо інтенсивність
    const intensityFill = document.getElementById('intensity-fill');
    if (intensityFill) {
        intensityFill.style.width = `${data.intensity * 100}%`;
        intensityFill.parentElement.className = `intensity-bar ${data.mood}`;
    }
    
    // Оновлюємо ефекти
    for (const [effect, value] of Object.entries(data.effects)) {
        updateEffect(effect, value);
    }
    
    // Оновлюємо події
    const eventList = document.getElementById('event-list');
    if (eventList) {
        eventList.innerHTML = '';
        
        data.events.forEach(event => {
            const eventElement = createEventElement(event);
            eventList.appendChild(eventElement);
        });
    }
}

/**
 * Створює HTML елемент для події
 * @param {Object} event - Подія 
 * @returns {HTMLElement} - HTML елемент з подією
 */
function createEventElement(event) {
    const eventItem = document.createElement('div');
    eventItem.className = 'event-item';
    
    const impactClass = getEventImpact(event.impact);
    
    eventItem.innerHTML = `
        <div class="event-impact ${impactClass}">${event.impact === 'positive' ? '+' : event.impact === 'negative' ? '-' : '='}</div>
        <div class="event-content">
            <div class="event-name">${event.name}</div>
            <div class="event-timestamp">${formatTimestamp(event.timestamp)}</div>
        </div>
    `;
    
    return eventItem;
}

/**
 * Оновлює відображення ефекту на сторінці
 * @param {string} effectName - Назва ефекту 
 * @param {number} value - Значення ефекту
 */
function updateEffect(effectName, value) {
    const effectElement = document.getElementById(`effect-${effectName}`);
    if (!effectElement) return;
    
    const effectValue = effectElement.querySelector('.effect-value');
    if (!effectValue) return;
    
    effectValue.textContent = value > 0 ? `+${value.toFixed(1)}` : value.toFixed(1);
    
    // Визначаємо клас ефекту в залежності від значення
    let effectClass = 'effect-neutral';
    if (value > 0) {
        effectClass = 'effect-positive';
    } else if (value < 0) {
        effectClass = 'effect-negative';
    }
    
    effectValue.className = `effect-value ${effectClass}`;
}

/**
 * Повертає локалізовану назву настрою
 * @param {string} mood - Код настрою 
 * @returns {string} - Локалізована назва
 */
function getMoodName(mood) {
    const moodNames = {
        'ecstatic': 'Екстатичний',
        'joyful': 'Радісний',
        'peaceful': 'Мирний',
        'neutral': 'Нейтральний',
        'anxious': 'Тривожний',
        'melancholic': 'Меланхолійний',
        'sad': 'Сумний',
        'angry': 'Гнівний',
        'chaotic': 'Хаотичний'
    };
    
    return moodNames[mood] || 'Невідомий';
}

/**
 * Повертає емодзі, що відповідає настрою
 * @param {string} mood - Код настрою 
 * @returns {string} - Емодзі
 */
function getMoodEmoji(mood) {
    const moodEmojis = {
        'ecstatic': '😍',
        'joyful': '😊',
        'peaceful': '😌',
        'neutral': '😐',
        'anxious': '😟',
        'melancholic': '😔',
        'sad': '😢',
        'angry': '😡',
        'chaotic': '🌀'
    };
    
    return moodEmojis[mood] || '❓';
}

/**
 * Повертає CSS клас для візуалізації впливу події
 * @param {string} impact - Вплив події (positive, neutral, negative) 
 * @returns {string} - CSS клас
 */
function getImpactLabel(impact) {
    switch (impact) {
        case 'positive':
            return 'impact-positive';
        case 'negative':
            return 'impact-negative';
        default:
            return 'impact-neutral';
    }
}

/**
 * Форматує часову мітку для відображення
 * @param {number} timestamp - Unix timestamp в мілісекундах
 * @returns {string} - Форматована дата і час
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `${day}.${month}.${year} ${hours}:${minutes}`;
}

/**
 * Отримує дані про настрій світу з API
 */
function fetchWorldMood() {
    fetch('/api/world-mood')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateWorldMoodDisplay(data);
        })
        .catch(error => {
            console.error('Error fetching world mood:', error);
        });
}

/**
 * Повертає CSS клас для відображення впливу події
 * @param {string} mood - Тип впливу 
 * @returns {string} - CSS клас
 */
function getEventImpact(mood) {
    if (mood === 'positive') return 'impact-positive';
    if (mood === 'negative') return 'impact-negative';
    return 'impact-neutral';
}