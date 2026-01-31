import { Outlet } from 'react-router-dom';
import { Logo } from '@/components/atoms/Logo';

/**
 * Candidate Layout - Minimalist, distraction-free
 * No sidebar to prevent cheating during assessments
 */
export function CandidateLayout() {
  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Minimal Header */}
      <header className="h-14 border-b border-border/50 flex items-center px-6">
        <Logo size="sm" />
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col">
        <Outlet />
      </main>

      {/* Minimal Footer */}
      <footer className="h-12 border-t border-border/50 flex items-center justify-center">
        <p className="text-xs text-muted-foreground">
          Powered by EvalynAI • Secure Assessment Environment
        </p>
      </footer>
    </div>
  );
}
