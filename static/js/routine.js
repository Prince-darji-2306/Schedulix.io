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
                        <input type="checkbox" class="custom-checkbox" id="check-${item.id}" 
                            ${item.is_completed ? 'checked' : ''} 
                            onchange="toggleSubtask(${item.id}, this)">
                    </div>
                    <div class="routine-content">
                        <span class="time-badge">${item.time_to}</span>
                        <div class="routine-title">${item.subtask} <small style="color:var(--text-muted); font-weight:400;">(${item.task_title})</small></div>
                        <div class="routine-desc">${item.description}</div>
                    </div>
                `;
                if (item.is_completed) itemDiv.classList.add('completed');
                routineList.appendChild(itemDiv);
            });
        } else {
            routineList.innerHTML = `<div id="empty-msg">${data.message || 'No approved routines for today. Go to Tasks and approve an AI plan!'}</div>`;
        }
    } catch (error) {
        console.error('Routine Error:', error);
        routineList.innerHTML = `<div id="empty-msg">Error fetching your routine. Please try again.</div>`;
    }
});

async function toggleSubtask(subtaskId, checkbox) {
    const token = localStorage.getItem('token');
    const item = checkbox.closest('.routine-item');
    const is_completed = checkbox.checked;

    if (is_completed) {
        item.classList.add('completed');
    } else {
        item.classList.remove('completed');
    }

    try {
        await fetch(`/api/subtasks/${subtaskId}/toggle`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_completed })
        });
    } catch (error) {
        console.error('Toggle Error:', error);
    }
}
