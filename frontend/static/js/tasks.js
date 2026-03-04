function roundHour(inputElement) {
    if (!inputElement.value) return;

    let [hour, minute] = inputElement.value.split(":").map(Number);

    // If minute >= 30, increase hour
    if (minute >= 30) {
        hour = (hour + 1) % 24;  // Handles 23 → 00
    }

    // Set minutes always to 00
    inputElement.value = String(hour).padStart(2, '0') + ":00";
}

document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');

    if (taskForm) {
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to add tasks');
                window.location.href = '/index.html';
                return;
            }

            const formData = new FormData(taskForm);
            const data = Object.fromEntries(formData.entries());
            console.log(data);
            const spinner = document.getElementById('spinner');
            if (spinner) spinner.style.display = 'flex';

            const submitBtn = taskForm.querySelector('button');
            submitBtn.innerText = 'Creating...';
            submitBtn.disabled = true;

            try {
                const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/tasks`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert('Success: Task created successfully!');
                    taskForm.reset();
                    window.location.href = '/tasks_todo.html';
                } else {
                    alert(`Error: ${result.detail || 'Failed to create task'}`);
                }
            } catch (error) {
                console.error('Task Error:', error);
                alert('Failed to connect to backend API');
            } finally {
                if (spinner) spinner.style.display = 'none';
                submitBtn.innerText = 'Create Task';
                submitBtn.disabled = false;
            }
        });
    }

    const tasksTableBody = document.getElementById('tasksTableBody');
    if (tasksTableBody) {
        const fetchTasks = async () => {
            const token = localStorage.getItem('token');
            if (!token) return;

            try {
                const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/tasks`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const tasks = await response.json();
                console.log('Fetched tasks:', tasks);

                if (response.ok) {
                    if (tasks.length === 0) {
                        tasksTableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 2rem; color: var(--text-muted);">No tasks found. Click "Add New Task" to get started!</td></tr>';
                        return;
                    }
                    tasksTableBody.innerHTML = tasks.map(task => {
                        let plan = "No plan generated";
                        if (task.ai_plan_json && task.ai_plan_json.final_plan) {
                            plan = task.ai_plan_json.final_plan;
                        }
                        return `
                        <tr>
                            <td><strong>${task.title}</strong></td>
                            <td class="task-description">${task.description || 'N/A'}</td>
                            <td>${(task.time || '00:00').substring(0, 5)} on ${task.deadline_date || 'N/A'} </td>
                            <td><span class="status-badge status-${(task.status || 'pending').toLowerCase()}">${task.status || 'Pending'}</span></td>
                            <td>
                                <button onclick="window.showPlan(\`${encodeURIComponent(task.title)}\`, \`${encodeURIComponent(plan)}\`, ${task.id}, ${task.plan_approved})" class="status-badge status-todo" id = 'viewplan'>View Plan</button>
                            </td>
                        </tr>
                    `}).join('');
                } else {
                    tasksTableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color: #ff4d4d; padding: 2rem;">Error: ${tasks.detail || 'Failed to fetch tasks'}</td></tr>`;
                }
            } catch (error) {
                console.error('Fetch Error:', error);
            }
        };

        window.showPlan = (title, encodedPlan, taskId, isApproved) => {
            const modal = document.getElementById('planModal');
            const modalTitle = document.getElementById('modalTitle');
            const planBody = document.getElementById('planBody');

            if (modal && modalTitle && planBody) {
                modalTitle.innerText = `Plan for: ${decodeURIComponent(title)}`;
                const planText = decodeURIComponent(encodedPlan);

                try {
                    const planObj = JSON.parse(planText);
                    // LangGraph stores JSON inside another JSON string sometimes
                    // But here it should be the final_plan string if coming from tasks list

                    if (planObj.markdown_plan) {
                        planBody.innerHTML = marked.parse(planObj.markdown_plan);
                    } else {
                        // Fallback for old plans
                        planBody.innerHTML = marked.parse(planText);
                    }
                } catch (e) {
                    planBody.innerHTML = marked.parse(planText);
                }

                modal.style.display = 'flex';

                // Toggle Approve Button
                const approveBtn = document.getElementById('approveBtn');
                if (approveBtn) {
                    approveBtn.style.display = isApproved ? 'none' : 'block';
                }

                // Store task info for approval
                window.currentTaskForApproval = {
                    id: taskId
                };
            }
        };

        window.approveCurrentPlan = async () => {
            if (!window.currentTaskForApproval) return;

            const btn = document.getElementById('approveBtn');
            const token = localStorage.getItem('token');

            if (!token) {
                alert('Session expired. Please login again.');
                window.location.href = '/index.html';
                return;
            }

            btn.innerText = 'Approving...';
            btn.disabled = true;

            try {
                const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/approve-plan`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        task_id: window.currentTaskForApproval.id
                    })
                });

                if (response.ok) {
                    alert('Plan approved! Subtasks have been scheduled.');
                    window.closeModal();
                    fetchTasks(); // Refresh to hide Approve Button later
                } else {
                    const result = await response.json();
                    alert(`Failed to approve plan: ${result.detail || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Approve Error:', error);
            } finally {
                btn.innerText = 'Approve Plan';
                btn.disabled = false;
            }
        };

        window.closeModal = () => {
            const modal = document.getElementById('planModal');
            if (modal) {
                modal.style.display = 'none';
            }
        };

        // Close on click outside
        window.onclick = (event) => {
            const modal = document.getElementById('planModal');
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        };

        fetchTasks();
    }
});
