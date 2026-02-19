document.addEventListener('DOMContentLoaded', async () => {
    const routineList = document.getElementById('routine-list');
    const token = localStorage.getItem('token');

    if (!token) {
        window.location.href = '/login';
        return;
    }

    try {
        const response = await fetch('/api/routine', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();

        routineList.innerHTML = ''; // Clear loading

        if (data.routine && data.routine.length > 0) {
            data.routine.forEach((item, index) => {
                const itemDiv = document.createElement('div');
                itemDiv.className = 'routine-item';
                itemDiv.innerHTML = `
                    <div class="check-container">
                        <input type="checkbox" class="custom-checkbox" id="check-${index}" onchange="toggleComplete(this)">
                    </div>
                    <div class="routine-content">
                        <span class="time-badge">${item.time}</span>
                        <div class="routine-title">${item.task}</div>
                        <div class="routine-desc">${item.description}</div>
                    </div>
                `;
                routineList.appendChild(itemDiv);
            });
        } else {
            routineList.innerHTML = `<div id="empty-msg">${data.message || 'No tasks found for today. Enjoy your day!'}</div>`;
        }
    } catch (error) {
        console.error('Routine Error:', error);
        routineList.innerHTML = `<div id="empty-msg">Error fetching your routine. Please try again.</div>`;
    }
});

function toggleComplete(checkbox) {
    const item = checkbox.closest('.routine-item');
    if (checkbox.checked) {
        item.classList.add('completed');
    } else {
        item.classList.remove('completed');
    }
}
