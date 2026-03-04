async function handleAuth(event, type) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    const submitBtn = event.target.querySelector('button');
    const originalText = submitBtn.innerText;
    submitBtn.innerText = 'Processing...';
    submitBtn.disabled = true;

    try {
        const response = await fetch(`${CONFIG.BACKEND_API_URL}/api/${type}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (response.ok) {
            if (type === 'login' && result.access_token) {
                localStorage.setItem('token', result.access_token);
            }
            alert(`${type === 'login' ? 'Welcome back!' : 'Registration successful!'}`);
            window.location.href = `${type === 'login' ? '/dashboard.html' : '/index.html'}`;

        } else {
            alert(`Error: ${result.detail || 'Something went wrong'}`);
        }
    } catch (error) {
        console.error('Auth Error:', error);
        alert('Failed to connect to backend API');
    } finally {
        submitBtn.innerText = originalText;
        submitBtn.disabled = false;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => handleAuth(e, 'login'));
    }

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => handleAuth(e, 'register'));
    }
});
