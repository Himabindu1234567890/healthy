function sendFoodMessage() {

    let message = document.getElementById("foodInput").value;

    fetch("/foodchat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {

        document.getElementById("foodChatBox").innerHTML +=
        "<p><b>You:</b> " + message + "</p>";

        document.getElementById("foodChatBox").innerHTML +=
        "<p><b>NutriBot:</b> " + data.response + "</p>";

    });

}