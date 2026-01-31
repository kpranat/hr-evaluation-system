import { Brain } from 'lucide-react';

interface LogoProps {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
}

export function Logo({ size = 'md', showText = true }: LogoProps) {
  const sizes = {
    sm: 'h-6 w-6',
    md: 'h-8 w-8',
    lg: 'h-10 w-10',
  };

  const textSizes = {
    sm: 'text-lg',
    md: 'text-xl',
    lg: 'text-2xl',
  };

  return (
    <div className="flex items-center gap-2">
      <div className="relative">
        <Brain className={`${sizes[size]} text-primary`} />
        <div className="absolute inset-0 blur-lg bg-primary/30 -z-10" />
      </div>
      {showText && (
        <span className={`font-semibold ${textSizes[size]} tracking-tight`}>
          Evalyn<span className="text-primary">AI</span>
        </span>
      )}
    </div>
  );
}
