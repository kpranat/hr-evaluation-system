import { useNavigate } from 'react-router-dom';
import { Users, Code, ArrowRight, Shield } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import DarkVeil from '@/components/animations/DarkVeil';

export default function Landing() {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-[calc(100vh-4rem)] flex flex-col items-center justify-center p-6 animate-fade-in overflow-hidden">

      {/* 3D Background Animation */}
      <div className="absolute inset-0 z-0 opacity-40">
        <DarkVeil
          hueShift={11}
          noiseIntensity={0}
          scanlineIntensity={0.22}
          speed={0.5}
          scanlineFrequency={1.6}
          warpAmount={2}
        />
      </div>

      <div className="max-w-5xl w-full space-y-12 text-center relative z-10">
        {/* Hero Section */}
        <div className="space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium backdrop-blur-sm border border-primary/20">
            <Shield className="h-4 w-4" />
            AI-Enabled Evaluation Platform
          </div>
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
            Welcome to <span className="gradient-text">Cygnusa</span>
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto backdrop-blur-sm bg-background/30 p-4 rounded-lg">
            A zero-cost, automated hiring platform that combines technical assessment with AI-driven integrity monitoring.
          </p>
        </div>

        {/* Selection Cards */}
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {/* Candidate Card */}
          <Card
            className="group relative overflow-hidden p-8 hover:border-primary/50 transition-all duration-300 hover:shadow-lg cursor-pointer text-left bg-card/80 backdrop-blur-md"
            onClick={() => navigate('/candidate/login')}
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Code className="h-24 w-24" />
            </div>
            <div className="relative z-10 space-y-4">
              <div className="h-12 w-12 rounded-lg bg-blue-500/10 flex items-center justify-center text-blue-500">
                <Code className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold">I'm a Candidate</h3>
                <p className="text-muted-foreground mt-2">
                  Sign in to access your assessment dashboard and prove your skills.
                </p>
              </div>
              <Button className="w-full gap-2 group-hover:bg-primary/90">
                Sign In
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </Card>

          {/* Recruiter Card */}
          <Card
            className="group relative overflow-hidden p-8 hover:border-purple-500/50 transition-all duration-300 hover:shadow-lg cursor-pointer text-left bg-card/80 backdrop-blur-md"
            onClick={() => navigate('/recruiter/login')}
          >
            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
              <Users className="h-24 w-24" />
            </div>
            <div className="relative z-10 space-y-4">
              <div className="h-12 w-12 rounded-lg bg-purple-500/10 flex items-center justify-center text-purple-500">
                <Users className="h-6 w-6" />
              </div>
              <div>
                <h3 className="text-2xl font-semibold">I'm a Recruiter</h3>
                <p className="text-muted-foreground mt-2">
                  Manage candidates, review AI reports, and analyze hiring data.
                </p>
              </div>
              <Button variant="outline" className="w-full gap-2 border-purple-500/20 hover:bg-purple-500/10 hover:text-purple-500">
                Sign In
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
            </div>
          </Card>
        </div>

        {/* Footer info */}
        <p className="text-sm text-muted-foreground">
          Select your role to continue with secure authentication.
        </p>
      </div>
    </div>
  );
}
