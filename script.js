document.getElementById('analysis-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const inputData = document.getElementById('inputData').value;
    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: inputData })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerText = `Analysis Result: ${data.result}`;
    })
    .catch(error => console.error('Error:', error));
});