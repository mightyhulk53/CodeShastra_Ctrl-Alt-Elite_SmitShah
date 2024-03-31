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

function takeCommand(message){
    let answer;
    if(message.includes('hey') || message.includes('hello')){
      speak("Hello Sir, How May I Help You?");
        answer = "Hello Sir, How May I Help You?";//answer from python
    }
    else {
        window.open(`https://www.google.com/search?q=${message.replace(" ", "+")}`, "_blank");
        speak("I found some information for " + message + " on google");
        answer = "I found some information for " + message + " on google";
    }

    messages.push({user: message, assistant: answer});
    updateConversationView();
}

inputField.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      console.log("hellooo")
        event.preventDefault();
        sendTextMessage();
    }
});

function sendTextMessage() {
    const message = 
    inputField.value.trim();
    if (message !== "") {
        // For now, just show the user's message
        // Placeholder for receiving and showing the answer from the search engine
        takeCommand(message.toLowerCase());
        messages.push({user: message, assistant: answer});
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
