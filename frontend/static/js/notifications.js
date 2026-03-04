document.addEventListener('DOMContentLoaded', async () => {
    const notifList = document.getElementById('notif-list');
    const token = localStorage.getItem('token');

    if (!token) {
        window.location.href = '/index.html';
        return;
    }

    const fetchNotifications = async () => {
        try {
            const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/notifications`, {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();

            notifList.innerHTML = '';
            if (data.length > 0) {
                data.forEach(note => {
                    const div = document.createElement('div');
                    div.className = `notif-item ${note.is_read ? '' : 'unread'}`;
                    div.innerHTML = `
                        <div class="notif-header">
                            <div class="notif-time">${note.created_at}</div>
                            ${note.is_read ? '' : `<span class="mark-read" onclick="markRead(${note.id})">Mark as read</span>`}
                        </div>
                        <div class="notif-message">${note.message}</div>
                    `;
                    notifList.appendChild(div);
                });
            } else {
                notifList.innerHTML = '<div style="text-align: center; padding: 2rem; color: var(--text-muted);">No notifications yet.</div>';
            }
        } catch (error) {
            console.error('Error fetching notifications:', error);
        }
    };

    window.markRead = async (id) => {
        try {
            const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/notifications/${id}/read`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (response.ok) {
                fetchNotifications();
            }
        } catch (error) {
            console.error('Error marking as read:', error);
        }
    };

    fetchNotifications();
});
