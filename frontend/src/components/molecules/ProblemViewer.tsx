import { useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { FileText, Info, CheckCircle2 } from 'lucide-react';

interface ProblemViewerProps {
  problemTitle?: string;
  problemDescription?: string;
  instructions?: string[];
  examples?: Array<{ input: string; output: string; explanation?: string }>;
}

export function ProblemViewer({
  problemTitle = "Two Sum",
  problemDescription = "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.",
  instructions = [
    "Read the problem statement carefully before starting.",
    "You have 45 minutes to complete this assessment.",
    "Your code will be evaluated on correctness, efficiency, and code quality.",
    "You may use any standard library functions.",
    "Do not switch tabs or windows during the assessment.",
    "Your webcam and screen are being monitored.",
  ],
  examples = [
    {
      input: "nums = [2,7,11,15], target = 9",
      output: "[0,1]",
      explanation: "Because nums[0] + nums[1] == 9, we return [0, 1].",
    },
    {
      input: "nums = [3,2,4], target = 6",
      output: "[1,2]",
    },
    {
      input: "nums = [3,3], target = 6",
      output: "[0,1]",
    },
  ],
}: ProblemViewerProps) {
  const [activeTab, setActiveTab] = useState('problem');

  return (
    <div className="h-full flex flex-col bg-card border-r border-border">
      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
        <div className="border-b border-border px-4">
          <TabsList className="h-12 bg-transparent gap-4">
            <TabsTrigger
              value="problem"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 pb-3"
            >
              <FileText className="h-4 w-4 mr-2" />
              Problem Statement
            </TabsTrigger>
            <TabsTrigger
              value="instructions"
              className="data-[state=active]:bg-transparent data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-0 pb-3"
            >
              <Info className="h-4 w-4 mr-2" />
              Instructions
            </TabsTrigger>
          </TabsList>
        </div>

        <TabsContent value="problem" className="flex-1 overflow-auto p-6 m-0 space-y-6">
          {/* Problem Title */}
          <div>
            <span className="text-xs font-medium text-primary bg-primary/10 px-2 py-1 rounded">
              Medium
            </span>
            <h2 className="text-xl font-semibold mt-3">{problemTitle}</h2>
          </div>

          {/* Description */}
          <div className="prose prose-invert prose-sm max-w-none">
            <p className="text-muted-foreground whitespace-pre-line leading-relaxed">
              {problemDescription}
            </p>
          </div>

          {/* Examples */}
          <div className="space-y-4">
            <h3 className="font-medium">Examples</h3>
            {examples.map((example, index) => (
              <div
                key={index}
                className="bg-muted/50 rounded-lg p-4 space-y-2 font-mono text-sm"
              >
                <div>
                  <span className="text-muted-foreground">Input: </span>
                  <span className="text-foreground">{example.input}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Output: </span>
                  <span className="text-primary">{example.output}</span>
                </div>
                {example.explanation && (
                  <div className="text-muted-foreground text-xs pt-1 border-t border-border/50">
                    {example.explanation}
                  </div>
                )}
              </div>
            ))}
          </div>

          {/* Constraints */}
          <div className="space-y-2">
            <h3 className="font-medium">Constraints</h3>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• 2 ≤ nums.length ≤ 10⁴</li>
              <li>• -10⁹ ≤ nums[i] ≤ 10⁹</li>
              <li>• -10⁹ ≤ target ≤ 10⁹</li>
              <li>• Only one valid answer exists.</li>
            </ul>
          </div>
        </TabsContent>

        <TabsContent value="instructions" className="flex-1 overflow-auto p-6 m-0">
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold">Assessment Guidelines</h2>
              <p className="text-muted-foreground mt-2">
                Please read these instructions carefully before beginning.
              </p>
            </div>

            <div className="space-y-3">
              {instructions.map((instruction, index) => (
                <div
                  key={index}
                  className="flex items-start gap-3 p-3 rounded-lg bg-muted/30"
                >
                  <CheckCircle2 className="h-5 w-5 text-success flex-shrink-0 mt-0.5" />
                  <span className="text-sm">{instruction}</span>
                </div>
              ))}
            </div>

            <div className="p-4 rounded-lg border border-warning/30 bg-warning/5">
              <p className="text-sm text-warning font-medium">
                ⚠️ Important: Any attempt to cheat or use external resources will
                result in automatic disqualification.
              </p>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
