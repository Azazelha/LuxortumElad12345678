/**
 * 3D-world-control.js
 * Скрипт для керування 3D світом Luxortum та відображення стану світу
 */

// Глобальні змінні сцени
let scene, camera, renderer, controls;
let skybox, terrain, water, buildings = [], characters = [];
let worldState = {
    mood: "neutral",
    intensity: 0.5,
    trend: "stable",
    effects: {}
};

// Кольори для різних настроїв світу
const moodColors = {
    ecstatic: 0xFFFF00,    // Яскраво-жовтий
    joyful: 0x00FF00,      // Зелений
    peaceful: 0x00FFFF,    // Блакитний
    neutral: 0xCCCCCC,     // Сірий
    anxious: 0xFF8C00,     // Оранжевий
    melancholic: 0x8A2BE2, // Пурпуровий
    sad: 0x0000FF,         // Синій
    angry: 0xFF0000,       // Червоний
    chaotic: 0xFF00FF      // Рожевий
};

// Функція ініціалізації 3D сцени
function init3DScene() {
    // Створюємо сцену
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000022); // Темно-синій фон

    // Створюємо камеру
    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    camera.position.set(0, 5, 10);

    // Створюємо рендерер
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;
    document.getElementById('scene-container').appendChild(renderer.domElement);

    // Додаємо OrbitControls для керування камерою
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.screenSpacePanning = false;
    controls.minDistance = 5;
    controls.maxDistance = 50;
    controls.maxPolarAngle = Math.PI / 2; // Обмежуємо кут нахилу камери

    // Додаємо освітлення
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(10, 20, 10);
    directionalLight.castShadow = true;
    scene.add(directionalLight);

    // Створюємо базову сцену
    createSkybox();
    createTerrain();
    createWater();
    createBuildings();
    createCharacters();

    // Додаємо обробник зміни розміру вікна
    window.addEventListener('resize', onWindowResize, false);

    // Запускаємо анімацію
    animate();
}

// Створення скайбоксу (неба)
function createSkybox() {
    const skyboxGeometry = new THREE.BoxGeometry(500, 500, 500);
    const skyboxMaterials = Array(6).fill().map(() => new THREE.MeshBasicMaterial({
        color: 0x87CEEB, // Блакитний колір неба
        side: THREE.BackSide
    }));
    skybox = new THREE.Mesh(skyboxGeometry, skyboxMaterials);
    scene.add(skybox);
}

// Створення території (землі)
function createTerrain() {
    const terrainGeometry = new THREE.PlaneGeometry(100, 100, 32, 32);
    terrainGeometry.rotateX(-Math.PI / 2); // Повертаємо площину горизонтально
    
    // Додаємо висоту для створення пагорбів
    const vertices = terrainGeometry.attributes.position.array;
    for (let i = 0; i < vertices.length; i += 3) {
        // Пропускаємо центральну частину, щоб там був рівний ландшафт
        const x = vertices[i];
        const z = vertices[i+2];
        const distanceFromCenter = Math.sqrt(x*x + z*z);
        
        if (distanceFromCenter > 20) {
            // Додаємо випадкову висоту поза центральною частиною
            vertices[i+1] = Math.sin(x / 5) * Math.cos(z / 5) * 2;
        }
    }

    const terrainMaterial = new THREE.MeshStandardMaterial({
        color: 0x3a7e4f, // Зелений колір трави
        roughness: 0.8,
        metalness: 0.2
    });
    terrain = new THREE.Mesh(terrainGeometry, terrainMaterial);
    terrain.receiveShadow = true;
    scene.add(terrain);
}

// Створення води
function createWater() {
    const waterGeometry = new THREE.PlaneGeometry(60, 60);
    waterGeometry.rotateX(-Math.PI / 2);
    
    const waterMaterial = new THREE.MeshStandardMaterial({
        color: 0x00BFFF, // Блакитний колір води
        transparent: true,
        opacity: 0.7,
        roughness: 0.1,
        metalness: 0.8
    });
    
    water = new THREE.Mesh(waterGeometry, waterMaterial);
    water.position.y = -0.1; // Розміщуємо трохи нижче за сушу
    water.receiveShadow = true;
    scene.add(water);
}

// Створення будівель
function createBuildings() {
    // Храм в центрі
    const templeGeometry = new THREE.CylinderGeometry(3, 3, 5, 6);
    const templeMaterial = new THREE.MeshStandardMaterial({ color: 0xF5F5DC }); // Бежевий колір
    const temple = new THREE.Mesh(templeGeometry, templeMaterial);
    temple.position.set(0, 2.5, 0);
    temple.castShadow = true;
    temple.receiveShadow = true;
    scene.add(temple);
    buildings.push(temple);

    // Дах храму
    const roofGeometry = new THREE.ConeGeometry(3.5, 2, 6);
    const roofMaterial = new THREE.MeshStandardMaterial({ color: 0xCD7F32 }); // Бронзовий колір
    const roof = new THREE.Mesh(roofGeometry, roofMaterial);
    roof.position.set(0, 6, 0);
    roof.castShadow = true;
    scene.add(roof);
    buildings.push(roof);

    // Додаємо колони навколо храму
    const columnGeometry = new THREE.CylinderGeometry(0.3, 0.3, 4, 8);
    const columnMaterial = new THREE.MeshStandardMaterial({ color: 0xF5F5DC });
    
    for (let i = 0; i < 6; i++) {
        const angle = (i / 6) * Math.PI * 2;
        const x = Math.cos(angle) * 4;
        const z = Math.sin(angle) * 4;
        
        const column = new THREE.Mesh(columnGeometry, columnMaterial);
        column.position.set(x, 2, z);
        column.castShadow = true;
        column.receiveShadow = true;
        scene.add(column);
        buildings.push(column);
    }

    // Додаємо будинки навколо
    const houseGeometry = new THREE.BoxGeometry(2, 2, 2);
    
    for (let i = 0; i < 8; i++) {
        const angle = (i / 8) * Math.PI * 2;
        const distance = 12;
        const x = Math.cos(angle) * distance;
        const z = Math.sin(angle) * distance;
        
        const houseMaterial = new THREE.MeshStandardMaterial({ 
            color: 0xD2B48C // Світло-коричневий колір
        });
        
        const house = new THREE.Mesh(houseGeometry, houseMaterial);
        house.position.set(x, 1, z);
        house.castShadow = true;
        house.receiveShadow = true;
        scene.add(house);
        buildings.push(house);
        
        // Дах будинку
        const houseRoofGeometry = new THREE.ConeGeometry(1.5, 1, 4);
        const houseRoofMaterial = new THREE.MeshStandardMaterial({ color: 0x8B4513 }); // Коричневий колір
        const houseRoof = new THREE.Mesh(houseRoofGeometry, houseRoofMaterial);
        houseRoof.position.set(x, 2.5, z);
        houseRoof.castShadow = true;
        scene.add(houseRoof);
        buildings.push(houseRoof);
    }
}

// Створення персонажів
function createCharacters() {
    const characterGeometry = new THREE.CapsuleGeometry(0.5, 1, 4, 8);
    
    // Створюємо 10 персонажів
    for (let i = 0; i < 10; i++) {
        // Обираємо випадкову позицію в межах світу
        const angle = Math.random() * Math.PI * 2;
        const distance = 5 + Math.random() * 10;
        const x = Math.cos(angle) * distance;
        const z = Math.sin(angle) * distance;
        
        const characterMaterial = new THREE.MeshStandardMaterial({
            color: 0xFFD700 + Math.random() * 0x909090 // Золотистий колір з варіаціями
        });
        
        const character = new THREE.Mesh(characterGeometry, characterMaterial);
        character.position.set(x, 1, z);
        character.castShadow = true;
        character.receiveShadow = true;
        character.userData = {
            speed: 0.01 + Math.random() * 0.02,
            direction: new THREE.Vector3(Math.random() - 0.5, 0, Math.random() - 0.5).normalize(),
            lastDirectionChange: 0
        };
        
        scene.add(character);
        characters.push(character);
    }
}

// Обробник зміни розміру вікна
function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

// Функція анімації
function animate() {
    requestAnimationFrame(animate);
    
    // Оновлюємо контролери
    controls.update();
    
    // Анімуємо воду (маленькі хвилі)
    if (water) {
        water.material.color.r = Math.sin(Date.now() * 0.001) * 0.1 + 0.1;
        water.material.color.g = Math.sin(Date.now() * 0.001) * 0.1 + 0.7;
        water.material.color.b = Math.sin(Date.now() * 0.001) * 0.1 + 0.9;
    }
    
    // Анімуємо персонажів
    const now = Date.now();
    characters.forEach(character => {
        // Випадкова зміна напрямку кожні 3-5 секунд
        if (now - character.userData.lastDirectionChange > 3000 + Math.random() * 2000) {
            character.userData.direction = new THREE.Vector3(
                Math.random() - 0.5, 
                0, 
                Math.random() - 0.5
            ).normalize();
            character.userData.lastDirectionChange = now;
        }
        
        // Рухаємо персонажа
        character.position.x += character.userData.direction.x * character.userData.speed;
        character.position.z += character.userData.direction.z * character.userData.speed;
        
        // Обмежуємо рух в межах світу
        const dist = Math.sqrt(character.position.x * character.position.x + character.position.z * character.position.z);
        if (dist > 20) {
            // Якщо вийшов за межі, повертаємо назад
            character.userData.direction.negate();
            character.userData.lastDirectionChange = now;
        }
        
        // Повертаємо персонажа в напрямку руху
        if (character.userData.direction.x !== 0 || character.userData.direction.z !== 0) {
            character.rotation.y = Math.atan2(
                character.userData.direction.x,
                character.userData.direction.z
            );
        }
    });
    
    // Анімуємо будівлі в залежності від настрою світу
    animateBuildingsByMood();
    
    // Рендерінг сцени
    renderer.render(scene, camera);
}

// Функція зміни сцени в залежності від настрою світу
function animateBuildingsByMood() {
    // Змінюємо колір неба
    const skyColor = moodColors[worldState.mood] || 0x87CEEB;
    for (let i = 0; i < skybox.material.length; i++) {
        skybox.material[i].color.setHex(
            blendColors(0x87CEEB, skyColor, worldState.intensity * 0.7)
        );
    }
    
    // Змінюємо колір та інтенсивність світла в залежності від настрою
    const lights = scene.children.filter(child => child instanceof THREE.Light);
    lights.forEach(light => {
        if (light instanceof THREE.AmbientLight) {
            // Для настроїв, які потребують менше світла (сумних, злих)
            if (['sad', 'melancholic', 'angry', 'chaotic'].includes(worldState.mood)) {
                light.intensity = 0.2 + (1 - worldState.intensity) * 0.3;
            } else {
                light.intensity = 0.3 + worldState.intensity * 0.3;
            }
        }
        
        if (light instanceof THREE.DirectionalLight) {
            light.color.setHex(blendColors(0xFFFFFF, skyColor, worldState.intensity * 0.3));
        }
    });
    
    // Анімуємо будівлі
    buildings.forEach((building, index) => {
        // Храм змінює колір залежно від настрою
        if (index === 0) { // Храм
            building.material.color.setHex(
                blendColors(0xF5F5DC, skyColor, worldState.intensity * 0.5)
            );
        }
        
        // Для хаотичного настрою трохи трясемо будівлі
        if (worldState.mood === 'chaotic') {
            building.position.y += Math.sin(Date.now() * 0.01 + index) * 0.01 * worldState.intensity;
        }
    });
    
    // Анімуємо персонажів
    characters.forEach((character, index) => {
        // Для радісного настрою персонажі рухаються швидше
        if (['ecstatic', 'joyful'].includes(worldState.mood)) {
            character.userData.speed = 0.02 + worldState.intensity * 0.03;
        } 
        // Для сумного настрою персонажі рухаються повільніше
        else if (['sad', 'melancholic', 'anxious'].includes(worldState.mood)) {
            character.userData.speed = 0.01 + worldState.intensity * 0.01;
        }
        // Для хаотичного настрою персонажі рухаються непередбачувано
        else if (worldState.mood === 'chaotic') {
            if (Math.random() > 0.95) {
                character.userData.direction = new THREE.Vector3(
                    Math.random() - 0.5, 
                    0, 
                    Math.random() - 0.5
                ).normalize();
            }
        }
    });
}

// Допоміжна функція для змішування кольорів
function blendColors(color1, color2, ratio) {
    const r1 = (color1 >> 16) & 0xFF;
    const g1 = (color1 >> 8) & 0xFF;
    const b1 = color1 & 0xFF;
    
    const r2 = (color2 >> 16) & 0xFF;
    const g2 = (color2 >> 8) & 0xFF;
    const b2 = color2 & 0xFF;
    
    const r = Math.round(r1 * (1 - ratio) + r2 * ratio);
    const g = Math.round(g1 * (1 - ratio) + g2 * ratio);
    const b = Math.round(b1 * (1 - ratio) + b2 * ratio);
    
    return (r << 16) | (g << 8) | b;
}

// Функція для оновлення стану світу
function updateWorldState(newState) {
    worldState = { ...worldState, ...newState };
    
    // Оновлюємо відображення стану світу в інтерфейсі
    document.getElementById('mood-value').textContent = getMoodName(worldState.mood);
    document.getElementById('intensity-value').textContent = `${Math.round(worldState.intensity * 100)}%`;
    document.getElementById('trend-value').textContent = getTrendName(worldState.trend);
    
    // Оновлюємо CSS класи
    document.getElementById('mood-value').className = `mood-value ${worldState.mood}`;
    document.getElementById('trend-value').className = `trend-value ${worldState.trend}`;
    
    // Оновлюємо індикатор інтенсивності
    document.getElementById('intensity-bar').style.width = `${worldState.intensity * 100}%`;
    
    // Оновлюємо список ефектів, якщо вони є
    if (worldState.effects) {
        const effectsList = document.getElementById('effects-list');
        effectsList.innerHTML = '';
        
        for (const [key, value] of Object.entries(worldState.effects)) {
            const li = document.createElement('li');
            const formattedValue = value > 0 ? `+${value}` : value;
            li.innerHTML = `<span>${getEffectName(key)}:</span> <span class="effect-value">${formattedValue}</span>`;
            effectsList.appendChild(li);
        }
    }
}

// Функція для отримання локалізованої назви настрою
function getMoodName(mood) {
    const moodNames = {
        'ecstatic': 'Екстатичний',
        'joyful': 'Радісний',
        'peaceful': 'Мирний',
        'neutral': 'Нейтральний',
        'anxious': 'Тривожний',
        'melancholic': 'Меланхолійний',
        'sad': 'Сумний',
        'angry': 'Злий',
        'chaotic': 'Хаотичний'
    };
    return moodNames[mood] || mood;
}

// Функція для отримання локалізованої назви тренду
function getTrendName(trend) {
    const trendNames = {
        'ascending': 'Покращується',
        'stable': 'Стабільний',
        'descending': 'Погіршується',
        'fluctuating': 'Коливається'
    };
    return trendNames[trend] || trend;
}

// Функція для отримання локалізованої назви ефекту
function getEffectName(effect) {
    const effectNames = {
        'happiness': 'Щастя',
        'stability': 'Стабільність',
        'creativity': 'Творчість',
        'knowledge': 'Знання',
        'harmony': 'Гармонія'
    };
    return effectNames[effect] || effect;
}

// Функція отримання стану світу з сервера
async function fetchWorldMood() {
    try {
        const response = await fetch('/api/world-mood');
        
        if (!response.ok) {
            throw new Error(`HTTP помилка! Статус: ${response.status}`);
        }
        
        const moodData = await response.json();
        updateWorldState(moodData);
        
    } catch (error) {
        console.error('Помилка під час отримання настрою світу:', error);
    }
}

// Функція для зміни настрою світу
async function changeWorldMood(newMood) {
    try {
        document.getElementById('update-status').textContent = 'Оновлення...';
        
        const response = await fetch('/api/world-mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ mood: newMood })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.message || `HTTP помилка! Статус: ${response.status}`);
        }
        
        if (result.status === 'success') {
            document.getElementById('update-status').textContent = 'Настрій оновлено успішно!';
            updateWorldState(result.data);
        } else {
            throw new Error(result.message || 'Помилка при оновленні настрою світу');
        }
        
    } catch (error) {
        console.error('Помилка під час оновлення настрою світу:', error);
        document.getElementById('update-status').textContent = '';
        document.getElementById('error-message').textContent = `Не вдалося оновити настрій світу: ${error.message}`;
        document.getElementById('error-message').style.display = 'block';
    }
}

// Функція для запуску автономної симуляції
async function runAutonomousSimulation() {
    try {
        document.getElementById('simulation-status').textContent = 'Запуск симуляції...';
        
        const response = await fetch('/api/run-autonomous-step');
        
        if (!response.ok) {
            throw new Error(`HTTP помилка! Статус: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.status === 'success') {
            document.getElementById('simulation-status').textContent = 'Симуляція успішно виконана!';
            document.getElementById('simulation-result').innerHTML = `
                <p><strong>Подія:</strong> ${result.event.name}</p>
                <p><strong>Опис:</strong> ${result.event.description}</p>
                <p><strong>Вплив:</strong> ${result.event.impact}</p>
            `;
            document.getElementById('simulation-result').style.display = 'block';
            
            // Оновлюємо стан світу
            updateWorldState(result.current_world_state);
        } else {
            throw new Error(result.message || 'Помилка при виконанні симуляції');
        }
        
    } catch (error) {
        console.error('Помилка під час виконання симуляції:', error);
        document.getElementById('simulation-status').textContent = '';
        document.getElementById('error-message').textContent = `Не вдалося виконати симуляцію: ${error.message}`;
        document.getElementById('error-message').style.display = 'block';
    }
}

// Ініціалізація при завантаженні сторінки
document.addEventListener('DOMContentLoaded', function() {
    // Ініціалізуємо 3D сцену
    init3DScene();
    
    // Отримуємо початковий стан світу
    fetchWorldMood();
    
    // Налаштовуємо обробники подій для кнопок
    document.querySelectorAll('.mood-buttons button').forEach(button => {
        button.addEventListener('click', function() {
            const mood = this.getAttribute('data-mood');
            changeWorldMood(mood);
        });
    });
    
    // Налаштовуємо обробник для кнопки автономної симуляції
    document.getElementById('run-simulation').addEventListener('click', runAutonomousSimulation);
    
    // Оновлюємо дані кожні 30 секунд
    setInterval(fetchWorldMood, 30000);
});