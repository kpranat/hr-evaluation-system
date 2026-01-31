import { useState, useEffect } from 'react';
import { Video, Shield, AlertCircle, Maximize2, Minimize2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface WebcamMonitorProps {
  className?: string;
}

type MonitoringStatus = 'active' | 'warning' | 'error';

export function WebcamMonitor({ className }: WebcamMonitorProps) {
  const [isMinimized, setIsMinimized] = useState(false);
  const [status, setStatus] = useState<MonitoringStatus>('active');
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);

  // Simulate webcam permission check
  useEffect(() => {
    const checkPermission = async () => {
      try {
        // Check if mediaDevices is available
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
          // Just check permissions, don't actually stream
          const result = await navigator.permissions.query({ name: 'camera' as PermissionName });
          setHasPermission(result.state === 'granted');
          
          result.addEventListener('change', () => {
            setHasPermission(result.state === 'granted');
          });
        } else {
          setHasPermission(false);
        }
      } catch {
        // If permission API not available, assume we need to request
        setHasPermission(null);
      }
    };

    checkPermission();
  }, []);

  const statusConfig = {
    active: {
      label: 'Monitoring Active',
      color: 'text-success',
      bgColor: 'bg-success/10',
      borderColor: 'border-success/30',
      icon: Shield,
    },
    warning: {
      label: 'Attention Required',
      color: 'text-warning',
      bgColor: 'bg-warning/10',
      borderColor: 'border-warning/30',
      icon: AlertCircle,
    },
    error: {
      label: 'Connection Lost',
      color: 'text-destructive',
      bgColor: 'bg-destructive/10',
      borderColor: 'border-destructive/30',
      icon: AlertCircle,
    },
  };

  const currentStatus = statusConfig[status];
  const StatusIcon = currentStatus.icon;

  if (isMinimized) {
    return (
      <div
        className={cn(
          "fixed bottom-4 left-4 z-50",
          className
        )}
      >
        <Button
          variant="secondary"
          size="sm"
          className={cn(
            "gap-2 shadow-lg border",
            currentStatus.bgColor,
            currentStatus.borderColor
          )}
          onClick={() => setIsMinimized(false)}
        >
          <div className={cn("w-2 h-2 rounded-full animate-pulse", status === 'active' ? 'bg-success' : status === 'warning' ? 'bg-warning' : 'bg-destructive')} />
          <Video className="h-4 w-4" />
          <span className="text-xs">Webcam</span>
        </Button>
      </div>
    );
  }

  return (
    <div
      className={cn(
        "fixed bottom-4 left-4 z-50 w-64 rounded-lg overflow-hidden shadow-2xl border",
        "bg-card/95 backdrop-blur-xl",
        currentStatus.borderColor,
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-border/50">
        <div className="flex items-center gap-2">
          <Video className="h-4 w-4 text-muted-foreground" />
          <span className="text-xs font-medium">Webcam Preview</span>
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="h-6 w-6"
          onClick={() => setIsMinimized(true)}
        >
          <Minimize2 className="h-3 w-3" />
        </Button>
      </div>

      {/* Webcam Preview Area */}
      <div className="relative aspect-video bg-muted/50">
        {hasPermission === false ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center p-4 text-center">
            <AlertCircle className="h-8 w-8 text-muted-foreground mb-2" />
            <p className="text-xs text-muted-foreground">
              Camera access required
            </p>
          </div>
        ) : (
          <>
            {/* Mock webcam view with gradient */}
            <div className="absolute inset-0 bg-gradient-to-br from-muted/80 to-muted flex items-center justify-center">
              <div className="w-16 h-16 rounded-full bg-muted-foreground/20 flex items-center justify-center">
                <Video className="h-8 w-8 text-muted-foreground/50" />
              </div>
            </div>

            {/* Recording indicator */}
            <div className="absolute top-2 right-2 flex items-center gap-1.5 px-2 py-1 rounded bg-destructive/90 text-destructive-foreground">
              <div className="w-2 h-2 rounded-full bg-destructive-foreground animate-pulse" />
              <span className="text-[10px] font-medium uppercase tracking-wide">REC</span>
            </div>
          </>
        )}
      </div>

      {/* Status Bar */}
      <div className={cn(
        "flex items-center gap-2 px-3 py-2",
        currentStatus.bgColor
      )}>
        <StatusIcon className={cn("h-4 w-4", currentStatus.color)} />
        <span className={cn("text-xs font-medium", currentStatus.color)}>
          System Status: {currentStatus.label}
        </span>
      </div>
    </div>
  );
}
