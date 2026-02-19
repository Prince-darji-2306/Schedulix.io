document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');

    if (taskForm) {
        taskForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const token = localStorage.getItem('token');
            if (!token) {
                alert('You must be logged in to add tasks');
                window.location.href = '/login';
                return;
            }

            const formData = new FormData(taskForm);
            const data = Object.fromEntries(formData.entries());

            const spinner = document.getElementById('spinner');
            if (spinner) spinner.style.display = 'flex';

            const submitBtn = taskForm.querySelector('button');
            submitBtn.innerText = 'Creating...';
            submitBtn.disabled = true;

            try {
                const response = await fetch('/api/tasks', {
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
                    window.location.href = '/tasks';
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
                const response = await fetch('/api/tasks', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                const tasks = await response.json();

                if (response.ok) {
                    tasksTableBody.innerHTML = tasks.map(task => {
                        let plan = "No plan generated";
                        if (task.ai_plan_json && task.ai_plan_json.final_plan) {
                            plan = task.ai_plan_json.final_plan;
                        }
                        return `
                        <tr>
                            <td><strong>${task.title}</strong></td>
                            <td>${task.description || 'N/A'}</td>
                            <td>${task.deadline || 'N/A'}</td>
                            <td>
                                <button onclick="window.showPlan(\`${encodeURIComponent(task.title)}\`, \`${encodeURIComponent(plan)}\`)" class="status-badge status-todo">View Plan</button>
                            </td>
                        </tr>
                    `}).join('');
                }
            } catch (error) {
                console.error('Fetch Error:', error);
            }
        };

        window.showPlan = (title, encodedPlan) => {
            const modal = document.getElementById('planModal');
            const modalTitle = document.getElementById('modalTitle');
            const planBody = document.getElementById('planBody');

            if (modal && modalTitle && planBody) {
                modalTitle.innerText = `Plan for: ${decodeURIComponent(title)}`;
                // Use marked to parse the plan
                planBody.innerHTML = marked.parse(decodeURIComponent(encodedPlan));
                modal.style.display = 'flex';
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
