import { useState, useEffect, useRef, useCallback } from 'react';

interface PlaybackEvent {
  t: number; // timestamp relative to start
  c: string; // content (snapshot for MVP, delta in future)
}

export function useCodePlayback(sessionId: string | null, questionId: number | null) {
  const [isRecording, setIsRecording] = useState(false);
  const eventsBuffer = useRef<PlaybackEvent[]>([]);
  const startTime = useRef<number>(Date.now());
  const flushInterval = useRef<NodeJS.Timeout | null>(null);

  const startRecording = useCallback(() => {
    setIsRecording(true);
    startTime.current = Date.now();
    eventsBuffer.current = [];
    
    // Auto-flush every 5 seconds
    if (flushInterval.current) clearInterval(flushInterval.current);
    flushInterval.current = setInterval(flush, 5000);
  }, []);

  const stopRecording = useCallback(() => {
    setIsRecording(false);
    flush(); // Final flush
    if (flushInterval.current) {
      clearInterval(flushInterval.current);
      flushInterval.current = null;
    }
  }, []);

  const recordChange = useCallback((code: string) => {
    if (!isRecording) return;
    
    eventsBuffer.current.push({
      t: Date.now() - startTime.current,
      c: code
    });
  }, [isRecording]);

  const flush = async () => {
    if (eventsBuffer.current.length === 0 || !sessionId || !questionId) return;

    const eventsToSend = [...eventsBuffer.current];
    eventsBuffer.current = []; // Clear buffer immediately

    try {
        // Send to backend
        await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/playback/record`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('candidate_token')}`
            },
            body: JSON.stringify({
                session_id: sessionId,
                question_id: questionId,
                events: eventsToSend
            })
        });
    } catch (error) {
        console.error("Failed to flush playback logs", error);
        // On failure, maybe push back to buffer? For now, we drop to avoid memory leak or blocking.
    }
  };

  // Cleanup
  useEffect(() => {
    return () => {
      if (flushInterval.current) clearInterval(flushInterval.current);
    };
  }, []);

  return {
    startRecording,
    stopRecording,
    recordChange
  };
}
