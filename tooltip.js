// Функції для роботи з контекстними підказками

/**
 * Отримує дані підказок з API для заданого елементу та типу персонажа
 * @param {string} elementId - ID HTML елементу, для якого потрібні підказки
 * @param {string} characterType - Тип персонажа (guide, prophet, lover, creator, destroyer)
 */
function fetchTooltips(elementId, characterType) {
    return fetch(`/api/tooltips?element_id=${elementId}&character_type=${characterType}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching tooltips:', error);
            return [];
        });
}