import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Mail, ArrowRight, Shield, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { candidateApi } from '@/lib/api';
import DarkVeil from '@/components/animations/DarkVeil';

export default function CandidateLogin() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const result = await candidateApi.login(email, password);

      if (result.data && (result.data as any).success) {
        // Store token and user data
        localStorage.setItem('candidate_token', (result.data as any).token);
        localStorage.setItem('candidate_user', JSON.stringify((result.data as any).user));

        // Navigate to candidate home
        navigate('/candidate');
      } else {
        setError((result.data as any)?.message || result.error || 'Login failed');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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

      <div className="max-w-md w-full space-y-8 relative z-10">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium backdrop-blur-sm border border-primary/20">
            <Shield className="h-4 w-4" />
            Secure Login
          </div>
          <h1 className="text-3xl font-bold tracking-tight">
            Welcome Back, <span className="gradient-text">Candidate</span>
          </h1>
          <p className="text-muted-foreground backdrop-blur-sm bg-background/30 p-2 rounded-lg inline-block">
            Sign in to access your assessment dashboard
          </p>
        </div>

        {/* Login Form */}
        <Card className="p-6 bg-card/80 backdrop-blur-md">
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Error Alert */}
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Email Field */}
            <div className="space-y-2">
              <Label htmlFor="email">Email Address</Label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="email"
                  type="email"
                  placeholder="candidate@example.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="pl-9 bg-background/50"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password Field */}
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-9 bg-background/50"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              className="w-full gap-2"
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign In'}
              <ArrowRight className="h-4 w-4" />
            </Button>
          </form>
        </Card>

        {/* Footer */}
        <p className="text-center text-sm text-muted-foreground">
          Don't have an account? Contact your recruiter for credentials.
        </p>
      </div>
    </div>
  );
}
