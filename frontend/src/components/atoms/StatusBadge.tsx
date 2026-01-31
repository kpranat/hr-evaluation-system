import { cn } from '@/lib/utils';

type Status = 'pending' | 'in-progress' | 'completed' | 'failed';

interface StatusBadgeProps {
  status: Status;
  className?: string;
}

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const variants: Record<Status, string> = {
    pending: 'bg-muted text-muted-foreground',
    'in-progress': 'bg-warning/10 text-warning border-warning/20',
    completed: 'bg-success/10 text-success border-success/20',
    failed: 'bg-destructive/10 text-destructive border-destructive/20',
  };

  const labels: Record<Status, string> = {
    pending: 'Pending',
    'in-progress': 'In Progress',
    completed: 'Completed',
    failed: 'Failed',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border',
        variants[status],
        className
      )}
    >
      <span
        className={cn(
          'w-1.5 h-1.5 rounded-full mr-1.5',
          status === 'pending' && 'bg-muted-foreground',
          status === 'in-progress' && 'bg-warning animate-pulse-subtle',
          status === 'completed' && 'bg-success',
          status === 'failed' && 'bg-destructive'
        )}
      />
      {labels[status]}
    </span>
  );
}
