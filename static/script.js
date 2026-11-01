const cityInput = document.getElementById("cityInput");
const searchBtn = document.getElementById("searchBtn");
const message = document.getElementById("message");
const weatherResult = document.getElementById("weatherResult");

async function getWeather() {
    const city = cityInput.value.trim();

    if (!city) {
        message.textContent = "Please enter a city name.";
        weatherResult.hidden = true;
        return;
    }

    message.textContent = "Loading weather...";
    weatherResult.hidden = true;
    searchBtn.disabled = true;

    try {
        const response = await fetch(
            `/api/weather?city=${encodeURIComponent(city)}`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to get weather.");
        }

        document.getElementById("cityName").textContent =
            `${data.city}, ${data.country}`;

        document.getElementById("condition").textContent =
            data.condition;

        document.getElementById("temperature").textContent =
            `${Math.round(data.temperature)}°C`;

        document.getElementById("feelsLike").textContent =
            `${Math.round(data.feels_like)}°C`;

        document.getElementById("humidity").textContent =
            `${data.humidity}%`;

        document.getElementById("windSpeed").textContent =
            `${data.wind_speed} m/s`;

        let suggestion = "Enjoy your day!";

        if (data.temperature >= 35) {
            suggestion = "☀️ Very hot! Wear light cotton clothes and drink water.";
        } else if (data.temperature >= 25) {
            suggestion = "👕 Warm weather! Light clothes are recommended.";
        } else if (data.temperature >= 15) {
            suggestion = "🧥 Pleasant weather! Carry a light jacket.";
        } else {
            suggestion = "🧣 Cold weather! Wear warm clothes.";
        }

        document.getElementById("suggestion").textContent = suggestion;

        weatherResult.hidden = false;
        message.textContent = "";

    } catch (error) {
        message.textContent = error.message;
    } finally {
        searchBtn.disabled = false;
    }
}

searchBtn.addEventListener("click", getWeather);

cityInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        getWeather();
    }
});

// Voice Search
const micBtn = document.getElementById("micBtn");

const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.lang = "en-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    micBtn.addEventListener("click", () => {
        message.textContent = "🎤 Listening... Speak your city name.";
        recognition.start();
    });

    recognition.onresult = (event) => {
        const city = event.results[0][0].transcript;
        cityInput.value = city;
        message.textContent = "You said: " + city;
        getWeather();
    };

    recognition.onerror = () => {
        message.textContent = "Microphone error. Please allow microphone permission.";
    };

    recognition.onend = () => {
        micBtn.disabled = false;
    };

    recognition.onerror = (event) => {
    message.textContent = "Voice error: " + event.error;
    micBtn.disabled = false;
};

} else {
    micBtn.disabled = true;
    micBtn.textContent = "Voice Not Supported";
}
