const buttons = document.querySelectorAll('.input-button');
const modeStatus = document.querySelector('#mode-status');
const messages = document.querySelector('#messages');

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    buttons.forEach((item) => item.classList.remove('active'));
    button.classList.add('active');

    const inputType = button.dataset.type;
    modeStatus.textContent = `目前輸入方式：${inputType}`;
    appendUserMessage(`我想使用「${inputType}」與會說話的鴿子互動。`);
  });
});

function appendUserMessage(text) {
  const message = document.createElement('article');
  message.className = 'message user';
  message.innerHTML = `
    <span class="message-avatar">👤</span>
    <p>${escapeHtml(text)}</p>
  `;
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}
