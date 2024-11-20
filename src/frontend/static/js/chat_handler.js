// Selects the chat container
const chatContainer = document.getElementById("chat-container");

// Function to add a new message to the chat container
function addMessageToChat(message, sender, isOwnMessage) {
    // Create a wrapper for the message
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.classList.add("bubbleWrapper");

    // Create inline container for the message and username
    const inlineContainer = document.createElement("div");
    inlineContainer.classList.add("inlineContainer");
    if (isOwnMessage) inlineContainer.classList.add("own");

    // Create the chat bubble
    const bubble = document.createElement("div");
    bubble.classList.add(isOwnMessage ? "ownBubble" : "otherBubble");
    bubble.textContent = message;

    // Add the sender's username
    const username = document.createElement("span");
    username.classList.add("username");
    username.textContent = sender;

    // Add username above the message text
    bubble.prepend(username);
    inlineContainer.appendChild(bubble);
    bubbleWrapper.appendChild(inlineContainer);

    // Add timestamp (Lets solve do we use the timestamp from database or we create new here)
    const timestamp = document.createElement("span");
    timestamp.classList.add(isOwnMessage ? "own" : "other");
    timestamp.textContent = new Date().toLocaleTimeString();
    bubbleWrapper.appendChild(timestamp);

    // Append the bubble to the chat container
    chatContainer.appendChild(bubbleWrapper);

    // Scroll to the bottom of the chat container
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Function to simulate receiving messages from peers
function receivePeerMessage(message, sender) {
    addMessageToChat(message, sender, false);
}

// Handle form submission for your own messages
document.getElementById("form").addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page

    const messageInput = document.getElementById("message");
    const message = messageInput.value.trim(); // Get the message text

    if (!message) return;

    // Add the message to the chat as your own
    addMessageToChat(message, "You", true);

    // Send the message to the backend
    await fetch("/", {
        method: "POST",
        body: new URLSearchParams({ message }), // Send message as POST data
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    messageInput.value = ""; // Clear the input field
});