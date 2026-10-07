const modeInput = document.getElementById('mode');
const queryField = document.getElementById('query-field');
const imageField = document.getElementById('image-field');
const customerField = document.getElementById('customer-field');
const query = document.getElementById('query');
const label = document.getElementById('query-label');
const help = document.getElementById('query-help');
const mic = document.getElementById('mic-button');
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

function selectMode(mode) {
  modeInput.value = mode;
  document.querySelectorAll('.tab').forEach(button => {
    button.classList.toggle('active', button.dataset.mode === mode);
    button.setAttribute('aria-selected', button.dataset.mode === mode ? 'true' : 'false');
  });
  queryField.hidden = mode === 'image';
  imageField.hidden = mode !== 'image' && mode !== 'multimodal';
  customerField.hidden = mode !== 'order';
  mic.hidden = mode !== 'voice' || !SpeechRecognition;
  label.textContent = mode === 'voice' ? 'SPEAK OR TYPE A TRANSCRIPT' : mode === 'order' ? 'ORDER REQUEST' : 'WHAT ARE YOU LOOKING FOR?';
  query.placeholder = mode === 'voice' ? 'Try: find blue sports shoes' : mode === 'order' ? 'Try: find order O001 or latest order' : 'Try: black running shoes';
  help.textContent = mode === 'voice' ? 'Use the microphone when supported, or type a transcript to simulate speech-to-text.' : mode === 'order' ? 'Look up an order ID or ask for the latest order for a customer.' : 'Try a product, color, category or price limit such as “running shoes under 110 dollars”.';
}

document.querySelectorAll('.tab').forEach(button => button.addEventListener('click', () => selectMode(button.dataset.mode)));
selectMode(window.initialMode || 'text');

if (SpeechRecognition) {
  mic.addEventListener('click', () => {
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    mic.textContent = 'Listening…';
    recognition.onresult = event => { query.value = event.results[0][0].transcript; };
    recognition.onerror = () => { mic.textContent = '◉ Speak'; };
    recognition.onend = () => { mic.textContent = '◉ Speak'; };
    recognition.start();
  });
}
