import { useState, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import { Clock, AlertCircle, ChevronLeft, ChevronRight } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { ProblemViewer } from '@/components/molecules/ProblemViewer';
import { CodeEditorMock } from '@/components/molecules/CodeEditorMock';
import { ConsoleOutput } from '@/components/molecules/ConsoleOutput';
import { WebcamMonitor } from '@/components/molecules/WebcamMonitor';
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable';

interface ConsoleLog {
  type: 'log' | 'error' | 'info' | 'success';
  message: string;
  timestamp: Date;
}

export default function Assessment() {
  const { id } = useParams<{ id: string }>();
  const [currentQuestion, setCurrentQuestion] = useState(1);
  const [isRunning, setIsRunning] = useState(false);
  const [consoleLogs, setConsoleLogs] = useState<ConsoleLog[]>([]);
  const [consoleExpanded, setConsoleExpanded] = useState(false);
  const totalQuestions = 5;

  const addLog = useCallback((type: ConsoleLog['type'], message: string) => {
    setConsoleLogs((prev) => [...prev, { type, message, timestamp: new Date() }]);
  }, []);

  const clearLogs = useCallback(() => {
    setConsoleLogs([]);
  }, []);

  const handleRunCode = useCallback(async (code: string) => {
    setIsRunning(true);
    
    // Log the code execution attempt
    addLog('info', 'Submitting code to server...');
    addLog('log', `POST /submit-test`);
    addLog('log', `Assessment ID: ${id}`);
    addLog('log', `Code length: ${code.length} characters`);

    // Simulate API call to Flask backend
    try {
      // Mock API request
      await new Promise((resolve) => setTimeout(resolve, 1500));
      
      // Log mock request details
      console.log('Mock Flask API Request:', {
        endpoint: 'POST /submit-test',
        payload: {
          assessmentId: id,
          questionNumber: currentQuestion,
          code: code,
          timestamp: new Date().toISOString(),
        },
      });

      addLog('info', 'Server received code submission');
      addLog('log', 'Running test cases...');
      
      await new Promise((resolve) => setTimeout(resolve, 800));
      
      // Mock output
      addLog('log', '');
      addLog('log', '=== Test Results ===');
      addLog('success', '✓ Test Case 1: Passed (nums=[2,7,11,15], target=9)');
      addLog('success', '✓ Test Case 2: Passed (nums=[3,2,4], target=6)');
      addLog('success', '✓ Test Case 3: Passed (nums=[3,3], target=6)');
      addLog('log', '');
      addLog('success', 'All test cases passed! (3/3)');
      addLog('log', 'Execution time: 45ms');
      addLog('log', 'Memory usage: 14.2 MB');
      
    } catch (error) {
      addLog('error', 'Failed to connect to server');
      addLog('error', 'Please check your network connection');
    } finally {
      setIsRunning(false);
    }
  }, [id, currentQuestion, addLog]);

  const handlePrevious = () => {
    if (currentQuestion > 1) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < totalQuestions) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-[calc(100vh-7rem)] animate-fade-in">
      {/* Assessment Header */}
      <div className="h-12 border-b border-border/50 bg-muted/20 flex items-center justify-between px-4 flex-shrink-0">
        <div className="flex items-center gap-4">
          <h1 className="text-sm font-medium">Technical Assessment</h1>
          <span className="text-xs text-muted-foreground px-2 py-1 bg-muted rounded">
            {id}
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
              Question {currentQuestion} of {totalQuestions}
            </span>
            <Progress 
              value={(currentQuestion / totalQuestions) * 100} 
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
              disabled={currentQuestion === 1}
            >
              <ChevronLeft className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={handleNext}
              disabled={currentQuestion === totalQuestions}
            >
              <ChevronRight className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </div>

      {/* Main Split View */}
      <div className="flex-1 min-h-0">
        <ResizablePanelGroup direction="horizontal">
          {/* Left Panel - Problem Viewer */}
          <ResizablePanel defaultSize={40} minSize={30}>
            <ProblemViewer />
          </ResizablePanel>

          <ResizableHandle withHandle />

          {/* Right Panel - Code Editor + Console */}
          <ResizablePanel defaultSize={60} minSize={40}>
            <div className="h-full flex flex-col">
              {/* Code Editor */}
              <div className="flex-1 min-h-0">
                <CodeEditorMock 
                  onRunCode={handleRunCode}
                  isRunning={isRunning}
                />
              </div>

              {/* Console */}
              <ConsoleOutput
                logs={consoleLogs}
                onClear={clearLogs}
                isExpanded={consoleExpanded}
                onToggleExpand={() => setConsoleExpanded(!consoleExpanded)}
              />
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
