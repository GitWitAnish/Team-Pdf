import { useState, useEffect, useRef } from "react";

export const useTextToSpeech = () => {
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [voices, setVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState(null);
  const synthRef = useRef(window.speechSynthesis);

  useEffect(() => {
    const loadVoices = () => {
      const availableVoices = synthRef.current.getVoices();
      setVoices(availableVoices);

      // Set default voice (prefer English voices)
      const englishVoice = availableVoices.find((voice) =>
        voice.lang.startsWith("en"),
      );
      setSelectedVoice(englishVoice || availableVoices[0]);
    };

    loadVoices();
    synthRef.current.addEventListener("voiceschanged", loadVoices);

    return () => {
      synthRef.current.removeEventListener("voiceschanged", loadVoices);
      synthRef.current.cancel();
    };
  }, []);

  const speak = (text, options = {}) => {
    // Cancel any ongoing speech
    synthRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = selectedVoice;
    utterance.rate = options.rate || 1;
    utterance.pitch = options.pitch || 1;
    utterance.volume = options.volume || 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    synthRef.current.speak(utterance);
  };

  const stop = () => {
    synthRef.current.cancel();
    setIsSpeaking(false);
  };

  const pause = () => {
    synthRef.current.pause();
  };

  const resume = () => {
    synthRef.current.resume();
  };

  return {
    speak,
    stop,
    pause,
    resume,
    isSpeaking,
    voices,
    selectedVoice,
    setSelectedVoice,
    isSupported: "speechSynthesis" in window,
  };
};
