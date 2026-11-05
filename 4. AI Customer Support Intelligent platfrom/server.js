const express = require('express');
const path = require('node:path');

const app = express();
const PORT = process.env.PORT || 3000;

const submissions = [];

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname)));

app.get('/api/health', (req, res) => {
  res.json({
    status: 'ok',
    message: 'Website backend is running',
    timestamp: new Date().toISOString(),
  });
});

app.get('/api/messages', (req, res) => {
  res.json({
    count: submissions.length,
    submissions,
  });
});

app.post('/api/contact', (req, res) => {
  const { name, email, message } = req.body || {};

  if (!name || !email || !message) {
    return res.status(400).json({
      success: false,
      message: 'Name, email, and message are required.',
    });
  }

  const submission = {
    id: Date.now(),
    name: String(name).trim(),
    email: String(email).trim(),
    message: String(message).trim(),
    createdAt: new Date().toISOString(),
  };

  submissions.push(submission);

  return res.status(200).json({
    success: true,
    message: 'Thanks! Your message has been received.',
    submission,
  });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
