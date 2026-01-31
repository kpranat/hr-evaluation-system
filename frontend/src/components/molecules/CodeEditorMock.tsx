import { useState, useCallback, useEffect } from 'react';
import { Play, RotateCcw, ChevronDown } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { cn } from '@/lib/utils';

interface CodeEditorMockProps {
  onRunCode: (code: string) => void;
  isRunning?: boolean;
  initialCode?: string;
}

const defaultCodeStr = `def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Find two indices whose values sum to target.
    
    Args:
        nums: List of integers
        target: Target sum
    
    Returns:
        List of two indices
    """
    # Your solution here
    seen = {}
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []


# Test your solution
if __name__ == "__main__":
    result = two_sum([2, 7, 11, 15], 9)
    print(f"Result: {result}")
`;

const languages = [
  { id: 'python', name: 'Python 3', extension: '.py' },
  { id: 'javascript', name: 'JavaScript', extension: '.js' },
  { id: 'typescript', name: 'TypeScript', extension: '.ts' },
  { id: 'java', name: 'Java', extension: '.java' },
];

export function CodeEditorMock({
  onRunCode,
  isRunning = false,
  initialCode = defaultCodeStr
}: CodeEditorMockProps) {
  const [code, setCode] = useState(initialCode);
  const [selectedLanguage, setSelectedLanguage] = useState(languages[0]);

  useEffect(() => {
    setCode(initialCode);
  }, [initialCode]);

  const lines = code.split('\n');

  const handleReset = useCallback(() => {
    setCode(initialCode); // Reset to the specific problem's template, not defaultCodeStr
  }, [initialCode]);

  const handleRunCode = useCallback(() => {
    onRunCode(code);
  }, [code, onRunCode]);

  // Simple syntax highlighting for Python
  const highlightLine = (line: string) => {
    // Keywords
    const keywords = ['def', 'return', 'for', 'in', 'if', 'else', 'elif', 'class', 'import', 'from', 'as', 'try', 'except', 'with', 'lambda', 'and', 'or', 'not', 'True', 'False', 'None'];
    const builtins = ['print', 'len', 'range', 'enumerate', 'list', 'dict', 'str', 'int', 'float', 'bool', 'set', 'tuple'];

    let result = line;

    // Escape HTML
    result = result.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // Strings (handle both single and double quotes)
    result = result.replace(/(["'])((?:\\.|(?!\1)[^\\])*?)\1/g, '<span class="text-success">$1$2$1</span>');

    // Triple-quoted strings/docstrings
    result = result.replace(/("""|''')([\s\S]*?)\1/g, '<span class="text-success">$1$2$1</span>');

    // Comments
    result = result.replace(/(#.*)$/g, '<span class="text-green-400 italic">$1</span>');

    // Keywords
    keywords.forEach(keyword => {
      const regex = new RegExp(`\\b(${keyword})\\b`, 'g');
      result = result.replace(regex, '<span class="text-primary font-medium">$1</span>');
    });

    // Built-in functions
    builtins.forEach(builtin => {
      const regex = new RegExp(`\\b(${builtin})\\b`, 'g');
      result = result.replace(regex, '<span class="text-warning">$1</span>');
    });

    // Function definitions
    result = result.replace(/\b(def\s+)(\w+)/g, '$1<span class="text-accent-foreground">$2</span>');

    // Numbers
    result = result.replace(/\b(\d+)\b/g, '<span class="text-orange-400">$1</span>');

    return result;
  };

  return (
    <div className="h-full flex flex-col bg-[hsl(222,47%,6%)] text-gray-300">
      {/* Editor Toolbar */}
      <div className="h-12 border-b border-border flex items-center justify-between px-4 bg-card/50">
        <div className="flex items-center gap-3">
          {/* Language Selector */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="sm" className="h-8 gap-2">
                {selectedLanguage.name}
                <ChevronDown className="h-3 w-3" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="start">
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.id}
                  onClick={() => setSelectedLanguage(lang)}
                >
                  {lang.name}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* File Tab */}
          <div className="flex items-center gap-2 px-3 py-1.5 bg-muted/50 rounded text-sm">
            <span className="text-muted-foreground">solution</span>
            <span className="text-foreground">{selectedLanguage.extension}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={handleReset}
            className="h-8 gap-2"
          >
            <RotateCcw className="h-4 w-4" />
            Reset
          </Button>
          <Button
            size="sm"
            onClick={handleRunCode}
            disabled={isRunning}
            className="h-8 gap-2 bg-success hover:bg-success/90 text-success-foreground"
          >
            <Play className={cn("h-4 w-4", isRunning && "animate-pulse")} />
            {isRunning ? 'Running...' : 'Run Code'}
          </Button>
        </div>
      </div>

      {/* Code Editor */}
      <div className="flex-1 overflow-auto">
        <div className="flex min-h-full">
          {/* Line Numbers */}
          <div className="py-4 px-2 text-right select-none bg-[hsl(222,47%,5%)] border-r border-border/50 min-w-[3rem]">
            {lines.map((_, index) => (
              <div
                key={index}
                className="text-xs leading-6 text-muted-foreground/80 font-mono"
              >
                {index + 1}
              </div>
            ))}
          </div>

          {/* Code Content */}
          <div className="flex-1 relative">
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="absolute inset-0 w-full h-full resize-none bg-transparent text-transparent caret-foreground font-mono text-sm leading-6 p-4 focus:outline-none"
              spellCheck={false}
              style={{
                fontFamily: 'ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace',
              }}
            />
            <div className="p-4 font-mono text-sm leading-6 pointer-events-none">
              {lines.map((line, index) => (
                <div
                  key={index}
                  className="whitespace-pre"
                  dangerouslySetInnerHTML={{ __html: highlightLine(line) || '&nbsp;' }}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
