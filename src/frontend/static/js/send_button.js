const button = document.createElement("button");

    // Set button text
    button.innerText = "Click Me";

    // Add an action for when the button is clicked
    button.onclick = function() {
        alert("Button was clicked!");
    };

    // Append the button to a container or directly to the body
    document.getElementById("button-container").appendChild(button);