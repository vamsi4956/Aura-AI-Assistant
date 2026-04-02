async function sendMessage() {
    const input = document.getElementById("input");
    const message = input.value.trim();

    if (!message) return;

    // 1. Show User Message
    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // 2. Show Aura's Response
        addMessage(data.response, "bot");

    } catch (error) {
        addMessage("Sorry, I'm having trouble connecting to the server.", "bot");
    }
}

function addMessage(text, type) {
    const chatbox = document.getElementById("chatbox");
    const div = document.createElement("div");
    div.className = `message ${type}`;
    div.innerText = text;
    
    chatbox.appendChild(div);
    
    // Smooth scroll to bottom
    chatbox.scrollTo({
        top: chatbox.scrollHeight,
        behavior: 'smooth'
    });
}

// Handle Enter Key
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("input").addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });
});