const btn = document.querySelector('.send-button');
var  inputField = document.getElementById('message');
const content = document.querySelector('.message');
const conversation_view = document.querySelector('.conversation_view');
let messages = [];

window.addEventListener('load', ()=>{
  speak("Initializing SIFRA...");
});

function speak(text){
    const text_speak = new SpeechSynthesisUtterance(text);

    text_speak.rate = 1;
    text_speak.volume = 1;
    text_speak.pitch = 1;

    window.speechSynthesis.speak(text_speak);
}
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition =  new SpeechRecognition();
//recognising audio
recognition.onresult = (event)=>{
    const currentIndex = event.resultIndex;
    const transcript = event.results[currentIndex][0].transcript;
    content.textContent = transcript;
  
    takeCommand(transcript.toLowerCase());
}

btn.addEventListener('click', () => {
  content.setAttribute('placeholder', 'Listening...');
  recognition.start();
});

let answer;

function takeCommand(message){
    const url = 'http://localhost:5051/ask_in_text';
    const requestOptions = {
    method: 'POST',
    headers: new Headers({
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json',
    }),
    body: JSON.stringify({ question: message }), // Assuming 'message' is defined elsewhere
    redirect: 'follow',
    };

    fetch(url, requestOptions)
    .then(response => response.json()) // Parse response as JSON
    .then(data => {
        const answer2 = data['result']; // Assign the value of 'result' to 'answer'
        console.log('Answer:', answer2);
        messages.push({user: message, assistant: answer2});
        messages.shift();
        answer = answer2;
        console.log('Data:', data);
    })
    .then(data => updateConversationView())
    .catch(error => console.error('Error:', error));
    speak(answer);
}

inputField.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        console.log("Enter Button Pressed")
        event.preventDefault();
        sendTextMessage();
    }
});

function sendTextMessage() {
    const message = 
    inputField.value.trim();
    if (message !== "") {
        const answer3 = answer;
        // For now, just show the user's message
        // Placeholder for receiving and showing the answer from the search engine
        takeCommand(message.toLowerCase());
        messages.push({user: message, assistant: answer3});
    updateConversationView();
        content.value = "";
    }
}

function updateConversationView() {
    conversation_view.innerHTML = "";
    messages.forEach(msg => {
        const user_message_element = document.createElement("div");
        user_message_element.className = "message user";
        user_message_element.textContent = "USER :  " + msg.user;
        conversation_view.appendChild(user_message_element);

        if (msg.assistant !== "") {
            const assistant_message_element = document.createElement("div");
            assistant_message_element.className = "message assistant";
            assistant_message_element.textContent = "SIFRA :  " + msg.assistant;
            conversation_view.appendChild(assistant_message_element);
        }
    });
    conversation_view.scrollTop = conversation_view.scrollHeight;
}
