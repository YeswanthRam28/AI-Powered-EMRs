const BASE_URL = 'http://127.0.0.1:8000/nlp/';
const fetchResultsBtn = document.getElementById('fetchResultsBtn');
const resultsList = document.getElementById('resultsList');

fetchResultsBtn.addEventListener('click', async () => {
    resultsList.innerHTML = "Fetching...";
    try {
        const res = await fetch(BASE_URL);
        if(!res.ok) throw new Error('Failed to fetch NLP results');
        const data = await res.json();
        resultsList.innerHTML = "";
        const results = data.results || data;
        if(!results.length) {
            resultsList.textContent = "No NLP results found.";
            return;
        }
        results.forEach((item, index) => {
            const li = document.createElement('li');
            li.innerHTML = `<strong>${index + 1}. [${item.task || "N/A"}]</strong> ${item.input_text || ""} → ${item.result || ""}`;
            resultsList.appendChild(li);
        });
    } catch(err) {
        resultsList.textContent = "Error fetching NLP results.";
        console.error(err);
    }
});
