import React, { useState } from 'react';

const VoiceChatbot = () => {
  const [listening, setListening] = useState(false);
  const [query, setQuery] = useState('');
  const [recommendations, setRecommendations] = useState([]);

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.continuous = false;
  recognition.lang = 'en-US';

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    setQuery(transcript);
    fetchRecommendations(transcript);
    setListening(false);
  };

  recognition.onerror = () => setListening(false);

  const startListening = () => {
    setListening(true);
    recognition.start();
  };

  const speak = (text) => {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  };

  const fetchRecommendations = async (input) => {
    const response = await fetch('http://127.0.0.1:5000/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: input }),
    });
    const data = await response.json();
    setRecommendations(data.recommendations);

    const spokenText = "Here are some movies I recommend: " + data.recommendations.join(", ");
    speak(spokenText);
  };

  return (
    <div className="chat-container">
      <h1>🎙️ Voice Movie Recommender</h1>
      <button onClick={startListening} disabled={listening}>
        {listening ? 'Listening...' : 'Speak'}
      </button>
      <p><strong>You said:</strong> {query}</p>
      <h2>Recommendations:</h2>
      <ul>
        {recommendations.map((movie, idx) => <li key={idx}>{movie}</li>)}
      </ul>
    </div>
  );
  
};

export default VoiceChatbot;
