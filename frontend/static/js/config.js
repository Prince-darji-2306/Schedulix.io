const CONFIG = {
    // Replace with your actual Render backend URL after deployment
    BACKEND_API_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? "http://localhost:8000"
        : "https://schedulix-io.onrender.com"
};
