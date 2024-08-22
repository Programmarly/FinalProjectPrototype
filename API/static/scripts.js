document.getElementById('generate-feedback-btn').addEventListener('click', async () => {
    // Example data; in a real application, you'd collect this from a form or other input
    const requestData = {
        question_list: [
            "What is a machine learning model?",
            "Explain the concept of overfitting."
        ],
        answer_list: [
            "A machine learning model is an algorithm trained on data to make predictions or decisions.",
            "Overfitting occurs when a model learns the training data too well, including its noise and outliers, which affects its performance on new data."
        ]
    };

    try {
        const response = await fetch('/general-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }

        const data = await response.json();

        // Show the feedback and UUID form
        document.getElementById('feedback-text').textContent = data.feedback;
        document.getElementById('uuid-form').style.display = 'block';
        document.getElementById('download-btn').style.display = 'block';

        // Store the file ID in the download button
        document.getElementById('download-btn').setAttribute('data-file-id', data.file_id);

    } catch (error) {
        console.error('Error:', error);
    }
});

document.getElementById('download-btn').addEventListener('click', () => {
    const fileId = document.getElementById('download-btn').getAttribute('data-file-id');
    if (fileId) {
        window.location.href = `/download-report/${fileId}`;
    } else {
        console.error('File ID not found.');
    }
});

document.getElementById('download-report-btn').addEventListener('click', () => {
    const fileId = document.getElementById('uuid-input').value;
    if (fileId) {
        window.location.href = `/download-report/${fileId}`;
    } else {
        console.error('UUID not provided.');
    }
});
