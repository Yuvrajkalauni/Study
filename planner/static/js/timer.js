let seconds = 0;
let interval = null;
let logId = null;

const timerDisplay = document.getElementById("timer");
const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");

function updateTimer() {
    seconds++;
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    timerDisplay.textContent =
        `${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
}

startBtn.onclick = async () => {
    startBtn.disabled = true;
    stopBtn.disabled = false;

    const response = await fetch("/api/start/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({ session_id: SESSION_ID })
    });

    const data = await response.json();
    logId = data.log_id;

    interval = setInterval(updateTimer, 1000);
};

stopBtn.onclick = async () => {
    clearInterval(interval);

    await fetch("/api/stop/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken()
        },
        body: new URLSearchParams({ log_id: logId })
    });

    stopBtn.disabled = true;
    startBtn.disabled = false;
};

//Add this at bottom of timer.js

function getCSRFToken() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}

