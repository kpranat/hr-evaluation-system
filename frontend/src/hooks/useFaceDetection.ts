import { useEffect, useRef, useState } from 'react';

export interface ViolationEvent {
  type: 'NO_FACE' | 'MULTIPLE_FACES' | 'FACE_TOO_FAR' | 'FACE_TURNED' | 'PHONE_DETECTED' | 'LOOKING_AWAY';
  details: string;
}

interface UseFaceDetectionOptions {
  enabled: boolean;
  detectionInterval?: number;
  onViolation: (event: ViolationEvent) => void;
  sessionId?: string;
}

interface UseFaceDetectionReturn {
  stream: MediaStream | null;
  videoRef: React.RefObject<HTMLVideoElement>;
  isModelLoaded: boolean;
}

export function useFaceDetection({
  enabled,
  detectionInterval = 2000,
  onViolation,
  sessionId
}: UseFaceDetectionOptions): UseFaceDetectionReturn {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isModelLoaded, setIsModelLoaded] = useState(true); // Always true for backend-based
  const onViolationRef = useRef(onViolation);

  // Update ref when callback changes
  useEffect(() => {
    onViolationRef.current = onViolation;
  }, [onViolation]);

  // Initialize Camera
  useEffect(() => {
    let mediaStream: MediaStream | null = null;
    let isMounted = true;

    const startCamera = async () => {
      if (!enabled) return;

      try {
        const newStream = await navigator.mediaDevices.getUserMedia({
          video: {
            width: { ideal: 640 },
            height: { ideal: 480 },
            facingMode: 'user'
          }
        });

        if (!isMounted) {
          newStream.getTracks().forEach(track => track.stop());
          return;
        }

        mediaStream = newStream;
        setStream(newStream);

        if (videoRef.current) {
          videoRef.current.srcObject = newStream;
        }
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };

    if (enabled) {
      startCamera();
    } else {
      setStream(null);
    }

    return () => {
      isMounted = false;
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
      }
    };
  }, [enabled]);

  // Run Backend Analysis Loop
  useEffect(() => {
    if (!enabled || !stream) return;

    const analyzeFrame = async () => {
      if (!videoRef.current || videoRef.current.paused || videoRef.current.ended) return;

      try {
        const video = videoRef.current;
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        // Use default quality (0.92) or specify lower to save bandwidth
        const imageData = canvas.toDataURL('image/jpeg', 0.8);

        const token = localStorage.getItem('candidate_token');
        if (!token) {
            console.warn("No candidate token found for proctoring");
            return;
        }

        const response = await fetch('/api/proctor/analyze-frame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                session_id: sessionId,
                image: imageData
            })
        });

        if (!response.ok) return;

        const data = await response.json();
        const analysis = data.analysis;

        if (analysis) {
            if (!analysis.face_detected) {
                onViolationRef.current({ type: 'NO_FACE', details: 'No face detected in frame' });
            } else if (analysis.multiple_faces) {
                onViolationRef.current({ type: 'MULTIPLE_FACES', details: 'Multiple people detected' });
            } else if (analysis.looking_away) {
                onViolationRef.current({ type: 'LOOKING_AWAY', details: 'Candidate looking away' });
            } else if (analysis.phone_detected) {
                onViolationRef.current({ type: 'PHONE_DETECTED', details: 'Suspicious object/hand detected' });
            }
        }

      } catch (error) {
        console.warn('Face detection loop error:', error);
      }
    };

    const intervalId = setInterval(analyzeFrame, detectionInterval);

    return () => {
      clearInterval(intervalId);
    };
  }, [enabled, stream, detectionInterval, sessionId]);

  return { stream, videoRef, isModelLoaded };
}
