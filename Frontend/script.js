document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById('upload-form');
  const fileInput = document.getElementById('file-input');
  const loading = document.getElementById('loading');
  const output = document.getElementById('output');
  const transcript = document.getElementById('transcript');
  const summary = document.getElementById('summary');
  const actionItems = document.getElementById('action-items');
  const profanity = document.getElementById('profanity');

  // 👉 Set to your Render backend or localhost

  const BACKEND_URL = 'http://127.0.0.1:5000/upload';  // Uncomment for local testing

  form.addEventListener('submit', async function (e) {
    e.preventDefault();

    if (!fileInput.files.length) {
      alert('Please select a file to upload.');
      return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    loading.style.display = 'block';
    output.style.display = 'none';

    try {
      const response = await fetch(BACKEND_URL, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Upload failed: ${errText}`);
      }

      const data = await response.json();

      transcript.textContent = data.transcript || 'No transcript found.';
      summary.textContent = data.summary || 'No summary found.';

      actionItems.innerHTML = '';
      if (data.action_items && data.action_items.length > 0) {
        data.action_items.forEach(item => {
          const li = document.createElement('li');
          li.textContent = item;
          actionItems.appendChild(li);
        });
      } else {
        actionItems.innerHTML = '<li>No action items found.</li>';
      }

      profanity.textContent = data.contains_profanity
        ? '⚠️ Profanity detected in transcript.'
        : '✅ No profanity found.';

      loading.style.display = 'none';
      output.style.display = 'block';
      output.scrollIntoView({ behavior: 'smooth' });
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('❌ Upload failed: ' + error.message);
      loading.style.display = 'none';
    }
  });
});
