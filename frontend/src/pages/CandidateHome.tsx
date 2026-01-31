import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, ArrowRight, FileText, Brain, Shield } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { cn } from '@/lib/utils';

export default function CandidateHome() {
  const navigate = useNavigate();
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile?.type === 'application/pdf') {
      setFile(droppedFile);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
    }
  };

  const handleStartAssessment = () => {
    // TODO: Upload file and get assessment ID from backend
    navigate('/assessment/demo-123');
  };

  return (
    <div className="flex-1 flex flex-col items-center justify-center p-6 animate-fade-in">
      <div className="max-w-2xl w-full space-y-8 text-center">
        {/* Hero */}
        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
            <Brain className="h-4 w-4" />
            AI-Powered Evaluation
          </div>
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight">
            Your skills,{' '}
            <span className="gradient-text">fairly evaluated</span>
          </h1>
          <p className="text-lg text-muted-foreground max-w-md mx-auto">
            Upload your resume and complete a personalized assessment tailored to
            your experience and the role you're applying for.
          </p>
        </div>

        {/* Upload Area */}
        <Card
          className={cn(
            'p-8 border-2 border-dashed transition-smooth cursor-pointer',
            isDragging
              ? 'border-primary bg-primary/5'
              : 'border-border hover:border-primary/50'
          )}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input')?.click()}
        >
          <input
            id="file-input"
            type="file"
            accept=".pdf"
            className="hidden"
            onChange={handleFileSelect}
          />

          {file ? (
            <div className="flex items-center justify-center gap-3">
              <FileText className="h-8 w-8 text-primary" />
              <div className="text-left">
                <p className="font-medium">{file.name}</p>
                <p className="text-sm text-muted-foreground">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              <div className="mx-auto w-12 h-12 rounded-full bg-muted flex items-center justify-center">
                <Upload className="h-6 w-6 text-muted-foreground" />
              </div>
              <div>
                <p className="font-medium">Drop your resume here</p>
                <p className="text-sm text-muted-foreground">
                  or click to browse (PDF only)
                </p>
              </div>
            </div>
          )}
        </Card>

        {/* CTA */}
        <Button
          size="lg"
          className="gap-2"
          disabled={!file}
          onClick={handleStartAssessment}
        >
          Start Assessment
          <ArrowRight className="h-4 w-4" />
        </Button>

        {/* Trust Badges */}
        <div className="flex items-center justify-center gap-6 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Shield className="h-4 w-4" />
            Secure & Private
          </div>
          <div className="flex items-center gap-2">
            <Brain className="h-4 w-4" />
            AI-Powered
          </div>
        </div>
      </div>
    </div>
  );
}
