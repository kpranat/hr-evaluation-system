import { useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { Clock, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ProblemViewer } from '@/components/molecules/ProblemViewer';
import { AssessmentInput } from '@/components/molecules/AssessmentInput';
import { ConsoleOutput } from '@/components/molecules/ConsoleOutput';
import { WebcamMonitor } from '@/components/molecules/WebcamMonitor';
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable';
import { mockQuestions } from '@/lib/mock-data';
import { AssessmentQuestion } from '@/types/assessment';

interface ConsoleLog {
  type: 'log' | 'error' | 'info' | 'success';
  message: string;
  timestamp: Date;
}

export default function Assessment() {
  const { id } = useParams<{ id: string }>();

  // State
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<number, any>>({});
  const [isRunning, setIsRunning] = useState(false);
  const [consoleLogs, setConsoleLogs] = useState<ConsoleLog[]>([]);
  const [consoleExpanded, setConsoleExpanded] = useState(false);

  // Derived State
  const currentQuestion: AssessmentQuestion = mockQuestions[currentQuestionIndex];
  const totalQuestions = mockQuestions.length;
  const currentAnswer = answers[currentQuestion.id];

  // Logic
  const addLog = useCallback((type: ConsoleLog['type'], message: string) => {
    setConsoleLogs((prev) => [...prev, { type, message, timestamp: new Date() }]);
  }, []);

  const clearLogs = useCallback(() => {
    setConsoleLogs([]);
  }, []);

  const handleAnswerChange = (value: any) => {
    setAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: value
    }));
  };

  const handleRunCode = async () => {
    if (currentQuestion.type !== 'coding') return;

    setIsRunning(true);
    addLog('info', 'Compiling and running code...');

    // Simulate execution
    await new Promise(resolve => setTimeout(resolve, 1500));

    addLog('success', 'All test cases passed!');
    setIsRunning(false);
  };

  const handleSubmitQuestion = () => {
    if (currentQuestion.type === 'coding') {
      handleRunCode();
    } else {
      // For non-coding questions, just move to next if available
      if (currentQuestionIndex < totalQuestions - 1) {
        handleNext();
      } else {
        addLog('success', 'Assessment completed! Answers saved.');
      }
    }
  };

  const handlePrevious = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(currentQuestionIndex - 1);
    }
  };

  const handleNext = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
    }
  };

  // Helper to map current question props to ProblemViewer
  const getProblemViewerProps = () => {
    const props: any = {
      problemTitle: currentQuestion.title,
      problemDescription: currentQuestion.description,
    };

    if (currentQuestion.type === 'coding') {
      props.examples = currentQuestion.examples;
      props.constraints = currentQuestion.constraints;
    } else if (currentQuestion.type === 'mcq') {
      props.instructions = [
        "Select the best option from the available choices.",
        "Read the scenario carefully."
      ];
    } else if (currentQuestion.type === 'text') {
      props.instructions = [
        "Be concise and clear in your response.",
        `Maximum ${currentQuestion.maxLength} characters allowed.`
      ];
    }

    return props;
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-7rem)] animate-fade-in">
      {/* Assessment Header */}
      <div className="h-12 border-b border-border/50 bg-muted/20 flex items-center justify-between px-4 flex-shrink-0">
        <div className="flex items-center gap-4">
          <h1 className="text-sm font-medium">Assessment Framework</h1>
          <span className="text-xs text-muted-foreground px-2 py-1 bg-muted rounded">
            {currentQuestion.type.toUpperCase()}
          </span>
        </div>

        <div className="flex items-center gap-6">
          {/* Timer */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-background border border-border">
            <Clock className="h-4 w-4 text-muted-foreground" />
            <span className="font-mono text-sm font-medium tabular-nums">45:00</span>
          </div>

          {/* Progress */}
          <div className="flex items-center gap-3">
            <span className="text-sm text-muted-foreground">
              Question {currentQuestionIndex + 1} of {totalQuestions}
            </span>
            <Progress
              value={((currentQuestionIndex + 1) / totalQuestions) * 100}
              className="w-24 h-2"
            />
          </div>

          {/* Navigation */}
          <div className="flex items-center gap-1">
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handlePrevious}
              disabled={currentQuestionIndex === 0}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleNext}
              disabled={currentQuestionIndex === totalQuestions - 1}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Main Split View */}
      <div className="flex-1 min-h-0">
        <ResizablePanelGroup direction="horizontal">
          {/* Left Panel - Context Area */}
          <ResizablePanel defaultSize={40} minSize={30}>
            <ProblemViewer {...getProblemViewerProps()} />
          </ResizablePanel>

          <ResizableHandle withHandle />

          {/* Right Panel - Input Area */}
          <ResizablePanel defaultSize={60} minSize={40}>
            <div className="h-full flex flex-col">
              {/* Input Component Switcher */}
              <div className="flex-1 min-h-0 relative">
                <AssessmentInput
                  question={currentQuestion}
                  answer={currentAnswer}
                  onAnswerChange={handleAnswerChange}
                  onSubmit={handleSubmitQuestion}
                  isRunning={isRunning}
                />
              </div>

              {/* Console - Only for Coding Questions */}
              {currentQuestion.type === 'coding' && (
                <ConsoleOutput
                  logs={consoleLogs}
                  onClear={clearLogs}
                  isExpanded={consoleExpanded}
                  onToggleExpand={() => setConsoleExpanded(!consoleExpanded)}
                />
              )}
            </div>
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>

      {/* Proctoring Notice */}
      <div className="h-8 flex items-center justify-center gap-2 text-xs text-muted-foreground border-t border-border/50 bg-muted/20 flex-shrink-0">
        <AlertCircle className="h-3.5 w-3.5" />
        <span>
          This assessment is monitored. Please do not switch tabs or windows.
        </span>
      </div>

      {/* Webcam Monitor */}
      <WebcamMonitor />
    </div>
  );
}
