function toggleChat() {

    let chatbox = document.getElementById("chatbotBox");
    let chat = document.getElementById("chatMessages");

    if (chatbox.style.display === "block") {
        chatbox.style.display = "none";
    } 
    else {

        chatbox.style.display = "block";

        if(chat.innerHTML.trim() === ""){

            chat.innerHTML += "<p><b>NutriSense Bot:</b> <i>Typing...</i></p>";

            setTimeout(function(){

                chat.innerHTML =
                "<p><b>NutriSense Bot:</b> How can I help you today?<br>You can ask about food calories, diabetes-friendly foods, or healthy diet.</p>";

                chat.scrollTop = chat.scrollHeight;

            },1200);
        }
    }
}


function sendMessage(){

    let input = document.getElementById("userMessage");
    let message = input.value;

    if(message.trim() === "") return;

    let chat = document.getElementById("chatMessages");

    chat.innerHTML += "<p><b>You:</b> " + message + "</p>";

    chat.scrollTop = chat.scrollHeight;

    chat.innerHTML += "<p id='typing'><b>Bot:</b> <i>Typing...</i></p>";

    fetch("/foodchat",{
        method:"POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("typing").remove();

        chat.innerHTML += "<p><b>Bot:</b> " + data.response + "</p>";

        chat.scrollTop = chat.scrollHeight;

    });

    input.value="";
}


/* ENTER KEY SUPPORT */

document.addEventListener("DOMContentLoaded", function(){

    let input = document.getElementById("userMessage");

    input.addEventListener("keypress", function(event){

        if(event.key === "Enter"){
            event.preventDefault();
            sendMessage();
        }

    });

});


/* SUGGESTION BUTTON FUNCTION */

function askSuggestion(text){

    document.getElementById("userMessage").value = text;

    sendMessage();

}