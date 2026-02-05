import { useEffect, useRef, useState } from 'react';

export interface ViolationEvent {
  type: 'NO_FACE' | 'MULTIPLE_FACES' | 'FACE_TOO_FAR' | 'FACE_TURNED';
  details: string;
}

interface UseFaceDetectionOptions {
  enabled: boolean;
  detectionInterval?: number;
  onViolation: (event: ViolationEvent) => void;
}

interface UseFaceDetectionReturn {
  stream: MediaStream | null;
  videoRef: React.RefObject<HTMLVideoElement>;
}

export function useFaceDetection({
  enabled,
  detectionInterval = 1000,
  onViolation
}: UseFaceDetectionOptions): UseFaceDetectionReturn {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const onViolationRef = useRef(onViolation);

  // Update ref when callback changes (doesn't trigger effect re-run)
  useEffect(() => {
    onViolationRef.current = onViolation;
  }, [onViolation]);

  useEffect(() => {
    let mediaStream: MediaStream | null = null;
    let detectionIntervalId: NodeJS.Timeout | null = null;
    let isMounted = true;

    const startCamera = async () => {
      try {
        const newStream = await navigator.mediaDevices.getUserMedia({
          video: { width: 640, height: 480 }
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

        // Start face detection
        if (enabled) {
          detectionIntervalId = setInterval(() => {
            // Placeholder for actual face detection logic
            // In production, you would use face-api.js or similar library here
          }, detectionInterval);
        }
      } catch (error) {
        console.error('Error accessing camera:', error);
      }
    };

    if (enabled) {
      startCamera();
    }

    return () => {
      isMounted = false;
      
      if (detectionIntervalId) {
        clearInterval(detectionIntervalId);
      }
      
      if (mediaStream) {
        mediaStream.getTracks().forEach(track => track.stop());
      }
      
      setStream(null);
    };
  }, [enabled, detectionInterval]);

  return { stream, videoRef };
}
