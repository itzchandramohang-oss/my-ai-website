document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('assistant-form');
  const input = document.getElementById('assistant-input');
  const chatLog = document.getElementById('chat-log');
  const promptButtons = document.querySelectorAll('.prompt-button');

  if (!form || !input || !chatLog) {
    return;
  }

  const addMessage = (text, type) => {
    const msg = document.createElement('div');
    msg.className = `message ${type}`;
    msg.textContent = text;
    chatLog.appendChild(msg);
    chatLog.scrollTop = chatLog.scrollHeight;
  };

  const askAssistant = async (userMessage) => {
    addMessage(userMessage, 'user');
    input.value = '';
    input.disabled = true;

    try {
      const response = await fetch('/api/ai/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      const answer = data?.answer || 'I could not answer that right now. Please try again.';
      addMessage(answer, 'bot');
    } catch (error) {
      addMessage('I am having trouble responding right now. Please try again in a moment.', 'bot');
    } finally {
      input.disabled = false;
      input.focus();
    }
  };

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const value = input.value.trim();

    if (!value) {
      return;
    }

    askAssistant(value);
  });

  promptButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const value = button.textContent.trim();
      askAssistant(value);
    });
  });
});
