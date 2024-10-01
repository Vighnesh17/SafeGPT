async function processPrompt() {
    const prompt = document.getElementById('prompt').value;
    try {
        const response = await axios.post('/process_prompt', { prompt });
        document.getElementById('response').innerText = response.data.response;
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('response').innerText = 'An error occurred.';
    }
}