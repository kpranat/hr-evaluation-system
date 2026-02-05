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
          detectionIntervalId = setInterval(async () => {
            if (!videoRef.current || !isMounted) return;
            
            try {
              // Capture frame from video
              const canvas = document.createElement('canvas');
              canvas.width = videoRef.current.videoWidth;
              canvas.height = videoRef.current.videoHeight;
              const ctx = canvas.getContext('2d');
              
              if (!ctx) return;
              
              ctx.drawImage(videoRef.current, 0, 0);
              const base64Image = canvas.toDataURL('image/jpeg', 0.6);
              
              // Send to backend for analysis
              const response = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:5000'}/api/proctor/analyze-frame`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${localStorage.getItem('candidate_token')}`
                },
                body: JSON.stringify({
                  image: base64Image
                })
              });
              
              const data = await response.json();
              
              if (data.success && data.analysis) {
                const analysis = data.analysis;
                
                // Check for violations and call onViolation callback
                if (!analysis.face_detected) {
                  console.log('🚨 No face detected');
                  onViolationRef.current({
                    type: 'NO_FACE',
                    details: 'No face detected in frame'
                  });
                } else if (analysis.multiple_faces) {
                  console.log('🚨 Multiple faces detected');
                  onViolationRef.current({
                    type: 'MULTIPLE_FACES',
                    details: 'Multiple people detected'
                  });
                } else if (analysis.looking_away) {
                  console.log('🚨 Looking away detected');
                  onViolationRef.current({
                    type: 'FACE_TURNED',
                    details: 'Candidate looking away from screen'
                  });
                }
              }
            } catch (error) {
              console.error('Face detection error:', error);
            }
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
