// Initialize Socket.IO connection
const socket = io("http://localhost:5010");

// Select the chat container
const chatContainer = document.getElementById("chat-container");

// Function to add a new message to the chat container
function addMessageToChat(message, sender, isOwnMessage, timestamp) {
    alert("Adding message to chat:", message, sender);
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

// Listen for new messages from the backend
socket.on("new_message", (data) => {
    alert("Message received from backend:", data);
    const { message, sender, timestamp } = data;
    addMessageToChat(message, sender, sender === "You", timestamp);
});

// Handle form submission
document.getElementById("form").addEventListener("submit", (event) => {
    event.preventDefault();
    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim();
    if (!message) return;

    const timestamp = Date.now() / 1000; // Send current time
    addMessageToChat(message, "You", true, timestamp);

    // Emit the message to the backend
    socket.emit("send_message", { message, sender: "You" });

    messageInput.value = ""; // Clear the input field
});
