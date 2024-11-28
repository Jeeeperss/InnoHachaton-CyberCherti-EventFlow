async function startWebSocket() {
  const settings = await import("../modules/settings.js")
  const ws_server = await settings.ws_server

  const params = new URLSearchParams(window.location.search);
  const roomId = Number(params.get('id'));

  const wsUrl = `${ws_server}/chat/ws/${roomId}`;

  const messagesDiv = document.getElementById('messages');
  const messageInput = document.getElementById('messageInput');
  const sendButton = document.getElementById('sendButton');

  // Подключение к WebSocket
  const socket = new WebSocket(wsUrl);

  // Открытие соединения
  socket.onopen = () => {
      console.log('Connected to WebSocket');
  };

  // Получение сообщения
  socket.onmessage = (event) => {
      const message = document.createElement('div');
      message.textContent = event.data;
      messagesDiv.appendChild(message);
  };

  // Обработка ошибок
  socket.onerror = (error) => {
      console.error('WebSocket error:', error);
  };

  // Закрытие соединения
  socket.onclose = () => {
      console.log('WebSocket connection closed');
  };

  // Отправка сообщения
  sendButton.addEventListener('click', () => {
    const message = messageInput.value.trim();
    if (message) {
        const payload = {
            sender_id: 1, // Замените на реальный ID пользователя
            content: message
        };

        // Сериализация объекта в JSON
        socket.send(JSON.stringify(payload));
        messageInput.value = ''; // Очистка поля ввода
    }
  });
}

startWebSocket()
