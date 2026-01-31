import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Download, Mail, Calendar, CheckCircle, XCircle, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { ScrollArea } from '@/components/ui/scroll-area';
import { mockCandidateDetails } from '@/lib/mock-data';

export default function CandidateDetail() {
  const { id } = useParams<{ id: string }>();
  // Fallback to the first mock candidate if ID not found or mocks limited
  const candidate = mockCandidateDetails[id || "1"] || mockCandidateDetails["1"];

  const getVerdictBadge = (verdict: string) => {
    if (verdict === 'Hire') {
      return (
        <Badge className="bg-green-600 hover:bg-green-700 text-white text-lg px-4 py-1.5 h-auto">
          <CheckCircle className="mr-2 h-5 w-5" />
          HIRE
        </Badge>
      );
    }
    return (
      <Badge variant="destructive" className="text-lg px-4 py-1.5 h-auto">
        <XCircle className="mr-2 h-5 w-5" />
        NO-HIRE
      </Badge>
    );
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high': return 'text-destructive';
      case 'medium': return 'text-orange-500';
      default: return 'text-muted-foreground';
    }
  };

  return (
    <div className="space-y-6 animate-fade-in max-w-7xl mx-auto p-6">
      {/* Back Link */}
      <Link
        to="/admin/dashboard"
        className="inline-flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-smooth"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to Dashboard
      </Link>

      {/* Candidate Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-6 border-b border-border pb-6">
        <div className="flex items-center gap-6">
          <div className="h-20 w-20 rounded-full bg-primary/10 flex items-center justify-center text-primary text-2xl font-bold">
            {candidate.name.split(' ').map(n => n[0]).join('')}
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              {candidate.name}
            </h1>
            <p className="text-lg text-muted-foreground">{candidate.role}</p>
            <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <Mail className="h-4 w-4" />
                {candidate.email}
              </span>
              <span className="flex items-center gap-1">
                <Calendar className="h-4 w-4" />
                Applied {candidate.applied_date}
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="flex flex-col items-end gap-2">
            <span className="text-sm font-medium text-muted-foreground uppercase tracking-wider">Verdict</span>
            {getVerdictBadge(candidate.verdict)}
          </div>
          <div className="h-12 w-px bg-border mx-2 hidden md:block" />
          <Button variant="outline">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
        </div>
      </div>

      {/* Grid Layout */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

        {/* Card 1: AI Rationale (Spans 2 columns on large screens) */}
        <Card className="md:col-span-2 lg:col-span-2 h-full flex flex-col">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span className="bg-primary/10 p-2 rounded-lg">🤖</span>
              AI Decision Rationale
            </CardTitle>
            <CardDescription>
              Analysis generated regarding the hiring decision.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex-1">
            <div className="bg-muted/30 p-6 rounded-xl border border-border/50 text-base leading-relaxed">
              {candidate.ai_rationale}
            </div>
          </CardContent>
        </Card>

        {/* Card 2: Scores */}
        <Card className="h-full flex flex-col">
          <CardHeader>
            <CardTitle>Performance Scores</CardTitle>
            <CardDescription>Technical vs. Soft Skills</CardDescription>
          </CardHeader>
          <CardContent className="space-y-8 flex-1 flex flex-col justify-center">
            {/* Technical Score */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium">Technical Skills</span>
                <span className="font-bold">{candidate.technical_score}/100</span>
              </div>
              <Progress value={candidate.technical_score} className="h-3" />
            </div>

            {/* Soft Skills Score */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-medium">Soft Skills / Culture</span>
                <span className="font-bold">{candidate.soft_skill_score}/100</span>
              </div>
              <Progress value={candidate.soft_skill_score} className="h-3" />
            </div>

            <div className="pt-4 border-t border-border">
              <div className="flex justify-between items-center text-sm">
                <span className="text-muted-foreground">Overall Weighted Score</span>
                <span className="text-xl font-bold text-primary">
                  {Math.round((candidate.technical_score * 0.7) + (candidate.soft_skill_score * 0.3))}%
                </span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Card 3: Integrity Log (Spans full width on small, 1 col on large) */}
        <Card className="md:col-span-2 lg:col-span-1 h-full flex flex-col lg:order-last">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-orange-500" />
              Integrity Monitor
            </CardTitle>
            <CardDescription>
              Proctoring event log
            </CardDescription>
          </CardHeader>
          <CardContent className="flex-1 min-h-[300px] p-0 relative">
            <ScrollArea className="h-[350px] w-full p-6 pt-0">
              <div className="space-y-4">
                {candidate.integrity_logs.map((log, index) => (
                  <div key={index} className="flex items-start gap-4 pb-4 border-b last:border-0 border-border/50 last:pb-0">
                    <span className="text-xs font-mono text-muted-foreground whitespace-nowrap pt-1">
                      {log.timestamp}
                    </span>
                    <div>
                      <p className={`text-sm font-medium ${getSeverityColor(log.severity)}`}>
                        {log.event}
                      </p>
                    </div>
                  </div>
                ))}
                {candidate.integrity_logs.length === 0 && (
                  <div className="text-center text-muted-foreground py-8">
                    No integrity violations detected.
                  </div>
                )}
              </div>
            </ScrollArea>
            <div className="absolute bottom-0 left-0 right-0 h-12 bg-gradient-to-t from-card to-transparent pointer-events-none" />
          </CardContent>
        </Card>

        {/* Placeholder for Details (optional, can be removed if not needed by user scope) */}
        <Card className="md:col-span-2 hidden lg:block">
          <CardHeader>
            <CardTitle>Detailed Assessment Breakdown</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-32 border-2 border-dashed border-border rounded-lg flex items-center justify-center text-muted-foreground">
              Detailed code analysis and question breakdown visualization
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
