// Chat container
const chatContainer = document.getElementById("chat-container");

// Server-Sent Events (SSE) to listen for messages
const eventSource = new EventSource("/stream_messages");

// Function to add a new message to the chat container
function addMessageToChat(message, sender, isOwnMessage, timestamp) {
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.classList.add("bubbleWrapper");

    const inlineContainer = document.createElement("div");
    inlineContainer.classList.add("inlineContainer");
    if (isOwnMessage) inlineContainer.classList.add("own");

    const bubble = document.createElement("div");
    bubble.classList.add(isOwnMessage ? "ownBubble" : "otherBubble");
    bubble.textContent = message;

    const username = document.createElement("span");
    username.classList.add("username");
    username.textContent = sender;
    bubble.prepend(username);

    inlineContainer.appendChild(bubble);
    bubbleWrapper.appendChild(inlineContainer);

    const timeDisplay = document.createElement("span");
    timeDisplay.classList.add(isOwnMessage ? "own" : "other");
    timeDisplay.textContent = new Date(timestamp * 1000).toLocaleTimeString();
    bubbleWrapper.appendChild(timeDisplay);

    chatContainer.appendChild(bubbleWrapper);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Handle form submission
document.getElementById("form").addEventListener("submit", (event) => {
    event.preventDefault();
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();
    if (!message) return;

    const timestamp = Date.now() / 1000;

    // Add to local chat
    addMessageToChat(message, "You", true, timestamp);

    // Send message to the backend
    fetch("/send_message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            sender: "You",
            message: message,
            timestamp: timestamp,
        }),
    });

    messageInput.value = ""; // Clear the input field
});

// Fetch messages from the backend
fetch("/messages")
    .then((response) => response.json())
    .then((messages) => {
        messages.forEach((msg) => {
            addMessageToChat(msg.message, msg.sender, false, msg.timestamp);
        });
    });

// Listens for incoming messages from the server via Server-Sent Events (SSE)
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const { message, sender, timestamp } = data;
    addMessageToChat(message, sender, sender === "You", timestamp);
};
