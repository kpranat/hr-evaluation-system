import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';
import { Progress } from '@/components/ui/progress';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Brain, CheckCircle2, AlertCircle, Loader2, ChevronRight } from 'lucide-react';
import { psychometricApi } from '@/lib/api';

interface Question {
  id: number;
  question_id: number;
  question: string;
  trait_type: number;
  scoring_direction: string;
}

interface AnswerOption {
  value: number;
  label: string;
}

export default function PsychometricTest() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showInstructions, setShowInstructions] = useState(true);
  
  const [instructions, setInstructions] = useState('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [answerOptions, setAnswerOptions] = useState<AnswerOption[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, number>>({});
  
  const [error, setError] = useState('');
  const [testComplete, setTestComplete] = useState(false);
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    startTest();
  }, []);

  const startTest = async () => {
    setLoading(true);
    setError('');
    
    const candidateToken = localStorage.getItem('candidate_token');
    const candidateData = candidateToken ? JSON.parse(atob(candidateToken.split('.')[1])) : null;
    
    if (!candidateData?.id) {
      setError('Please login first');
      setTimeout(() => navigate('/candidate/login'), 2000);
      return;
    }

    const response = await psychometricApi.startTest(candidateData.id);
    
    if (response.data?.success) {
      setInstructions(response.data.instructions);
      setQuestions(response.data.questions);
      setAnswerOptions(response.data.answer_options);
    } else {
      setError(response.data?.error || response.error || 'Failed to load test');
    }
    
    setLoading(false);
  };

  const handleAnswerSelect = (answer: number) => {
    const currentQuestion = questions[currentQuestionIndex];
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.question_id]: answer
    }));
  };

  const handleNext = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  const handleSubmit = async () => {
    setSubmitting(true);
    setError('');
    
    const candidateToken = localStorage.getItem('candidate_token');
    const candidateData = candidateToken ? JSON.parse(atob(candidateToken.split('.')[1])) : null;
    
    if (!candidateData?.id) {
      setError('Session expired. Please login again.');
      return;
    }

    // Convert answers to API format
    const formattedAnswers = Object.entries(answers).map(([question_id, answer]) => ({
      question_id: parseInt(question_id),
      answer: answer
    }));

    const response = await psychometricApi.submitTest(candidateData.id, formattedAnswers);
    
    if (response.data?.success) {
      setTestComplete(true);
      setResults(response.data.results);
    } else {
      setError(response.data?.error || response.error || 'Failed to submit test');
    }
    
    setSubmitting(false);
  };

  const progress = questions.length > 0 
    ? ((Object.keys(answers).length / questions.length) * 100) 
    : 0;

  const currentQuestion = questions[currentQuestionIndex];
  const currentAnswer = currentQuestion ? answers[currentQuestion.question_id] : undefined;
  const allAnswered = Object.keys(answers).length === questions.length;

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <Loader2 className="h-8 w-8 animate-spin mx-auto" />
          <p className="text-muted-foreground">Loading psychometric assessment...</p>
        </div>
      </div>
    );
  }

  if (error && !questions.length) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Alert variant="destructive" className="max-w-md">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  if (showInstructions) {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="max-w-2xl w-full">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Brain className="h-6 w-6 text-primary" />
              <CardTitle>Psychometric Assessment</CardTitle>
            </div>
            <CardDescription>IPIP Big Five Personality Test</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="prose prose-sm">
              <p className="whitespace-pre-line">{instructions}</p>
            </div>
            
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                You have <strong>{questions.length} questions</strong> to answer. 
                Take your time and answer honestly.
              </AlertDescription>
            </Alert>

            <Button onClick={() => setShowInstructions(false)} className="w-full">
              Start Assessment
              <ChevronRight className="ml-2 h-4 w-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (testComplete && results) {
    const traitNames: Record<string, string> = {
      extraversion: 'Extraversion',
      agreeableness: 'Agreeableness',
      conscientiousness: 'Conscientiousness',
      emotional_stability: 'Emotional Stability',
      intellect_imagination: 'Intellect/Imagination'
    };

    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <Card className="max-w-2xl w-full">
          <CardHeader>
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-6 w-6 text-green-500" />
              <CardTitle>Test Complete!</CardTitle>
            </div>
            <CardDescription>Your personality assessment results</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <Alert>
              <CheckCircle2 className="h-4 w-4" />
              <AlertDescription>
                Thank you for completing the psychometric assessment. 
                Your results have been recorded.
              </AlertDescription>
            </Alert>

            <div className="space-y-4">
              <h3 className="font-semibold">Big Five Personality Traits</h3>
              {Object.entries(results).map(([key, value]) => {
                if (typeof value === 'number') {
                  const percentage = (value / 50) * 100;
                  return (
                    <div key={key} className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="font-medium">{traitNames[key]}</span>
                        <span className="text-muted-foreground">{value}/50</span>
                      </div>
                      <Progress value={percentage} className="h-2" />
                    </div>
                  );
                }
                return null;
              })}
            </div>

            <Button onClick={() => navigate('/candidate/home')} className="w-full">
              Return to Dashboard
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted/20 p-4">
      <div className="max-w-4xl mx-auto space-y-6 py-8">
        {/* Progress Header */}
        <Card>
          <CardContent className="pt-6 space-y-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center gap-2">
                <Brain className="h-5 w-5 text-primary" />
                <span className="font-semibold">Psychometric Test</span>
              </div>
              <span className="text-sm text-muted-foreground">
                Question {currentQuestionIndex + 1} of {questions.length}
              </span>
            </div>
            <Progress value={progress} className="h-2" />
            <p className="text-sm text-muted-foreground">
              {Object.keys(answers).length} answered • {questions.length - Object.keys(answers).length} remaining
            </p>
          </CardContent>
        </Card>

        {/* Question Card */}
        <Card>
          <CardHeader>
            <CardTitle className="text-xl">{currentQuestion?.question}</CardTitle>
            <CardDescription>
              Select the option that best describes you
            </CardDescription>
          </CardHeader>
          <CardContent>
            <RadioGroup value={String(currentAnswer)} onValueChange={(val) => handleAnswerSelect(parseInt(val))}>
              <div className="space-y-3">
                {answerOptions.map((option) => (
                  <div key={option.value} className="flex items-center space-x-2">
                    <RadioGroupItem value={String(option.value)} id={`option-${option.value}`} />
                    <Label htmlFor={`option-${option.value}`} className="flex-1 cursor-pointer p-3 rounded border hover:bg-accent">
                      {option.label}
                    </Label>
                  </div>
                ))}
              </div>
            </RadioGroup>
          </CardContent>
        </Card>

        {/* Navigation */}
        <div className="flex justify-between items-center gap-4">
          <Button
            variant="outline"
            onClick={handlePrevious}
            disabled={currentQuestionIndex === 0}
          >
            Previous
          </Button>

          <div className="flex gap-2">
            {currentQuestionIndex < questions.length - 1 ? (
              <Button
                onClick={handleNext}
                disabled={!currentAnswer}
              >
                Next
                <ChevronRight className="ml-2 h-4 w-4" />
              </Button>
            ) : (
              <Button
                onClick={handleSubmit}
                disabled={!allAnswered || submitting}
                className="bg-green-600 hover:bg-green-700"
              >
                {submitting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="mr-2 h-4 w-4" />
                    Submit Test
                  </>
                )}
              </Button>
            )}
          </div>
        </div>

        {!allAnswered && currentQuestionIndex === questions.length - 1 && (
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Please answer all questions before submitting. 
              You have {questions.length - Object.keys(answers).length} unanswered question(s).
            </AlertDescription>
          </Alert>
        )}

        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </div>
    </div>
  );
}
