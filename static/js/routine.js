document.addEventListener('DOMContentLoaded', async () => {
    fetchRoutine();
});

async function fetchRoutine() {
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
            data.routine.forEach((task) => {
                const parentCard = document.createElement('div');
                parentCard.className = 'routine-parent-card';
                parentCard.id = `task-card-${task.id}`;

                let subtasksHtml = '';
                task.subtasks.forEach(st => {
                    subtasksHtml += `
                        <div class="subtask-item ${st.is_completed ? 'completed' : ''}">
                            <div class="check-container">
                                <input type="checkbox" class="custom-checkbox" id="check-${st.id}" 
                                    ${st.is_completed ? 'checked' : ''} 
                                    onchange="toggleSubtask(${st.id}, this, ${task.id})">
                            </div>
                            <div class="routine-content">
                                <span class="time-badge">${st.time_to}</span>
                                <div class="routine-title">${st.subtask}</div>
                                <div class="routine-desc">${st.description}</div>
                            </div>
                        </div>
                    `;
                });

                parentCard.innerHTML = `
                    <div class="routine-parent-header" onclick="toggleAccordion(${task.id})">
                        <div class="routine-parent-info">
                            <h3>${task.title}</h3>
                            <p>${task.description || 'No description'}</p>
                        </div>
                        <div class="expand-icon">▼</div>
                    </div>
                    <div class="subtask-list" id="sublist-${task.id}">
                        ${subtasksHtml}
                    </div>
                `;
                routineList.appendChild(parentCard);
            });
        } else {
            routineList.innerHTML = `<div id="empty-msg">No active routines for today. Go to Tasks and approve an AI plan!</div>`;
        }
    } catch (error) {
        console.error('Routine Error:', error);
        routineList.innerHTML = `<div id="empty-msg">Error fetching your routine. Please try again.</div>`;
    }
}

function toggleAccordion(taskId) {
    const card = document.getElementById(`task-card-${taskId}`);
    card.classList.toggle('expanded');
}

async function toggleSubtask(subtaskId, checkbox, taskId) {
    const token = localStorage.getItem('token');
    const item = checkbox.closest('.subtask-item');
    const is_completed = checkbox.checked;

    if (is_completed) {
        item.classList.add('completed');
    } else {
        item.classList.remove('completed');
    }

    try {
        const response = await fetch(`/api/subtasks/${subtaskId}/toggle`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_completed })
        });

        const result = await response.json();

        // If parent task is completed, refresh the whole list after a short delay
        if (result.task_completed) {
            setTimeout(() => {
                alert('Great job! Parent task completed.');
                fetchRoutine();
            }, 500);
        }
    } catch (error) {
        console.error('Toggle Error:', error);
    }
}
