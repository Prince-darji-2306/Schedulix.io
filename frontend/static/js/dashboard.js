document.addEventListener('DOMContentLoaded', () => {
    const healthBtn = document.getElementById('healthCheckBtn');
    const healthLink = document.getElementById('health-link');

    if (!healthBtn || !healthLink) return;

    healthLink.addEventListener('click', async (event) => {
        event.preventDefault();

        const originalText = healthBtn.innerText;
        healthBtn.innerText = 'Checking...';
        healthBtn.disabled = true;

        try {
            const healthResponse = await fetch(`${CONFIG.BACKEND_API_URL}/health/docs`);

            if (!healthResponse.ok) {
                throw new Error(`Health check failed with status ${healthResponse.status}`);
            }

            const healthData = await healthResponse.json();
            const docsPath = healthData.docs_url || '/docs';
            const docsUrl = docsPath.startsWith('http') ? docsPath : `${CONFIG.BACKEND_API_URL}${docsPath}`;

            const docsResponse = await fetch(docsUrl);
            if (docsResponse.ok) {
                window.open(docsUrl, '_blank');
            } else {
                window.open(`${CONFIG.BACKEND_API_URL}/health`, '_blank');
            }
        } catch (error) {
            console.error('Health check error:', error);
            alert('Backend is unreachable right now. Please try again.');
        } finally {
            healthBtn.innerText = originalText;
            healthBtn.disabled = false;
        }
    });
});
