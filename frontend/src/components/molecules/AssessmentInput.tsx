import { AssessmentQuestion } from '@/types/assessment';
import { CodeEditorMock } from './CodeEditorMock';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Slider } from '@/components/ui/slider';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { Label } from '@/components/ui/label';

interface AssessmentInputProps {
    question: AssessmentQuestion;
    answer: any;
    onAnswerChange: (answer: any) => void;
    onSubmit: () => void;
    isRunning?: boolean;
}

export function AssessmentInput({
    question,
    answer,
    onAnswerChange,
    onSubmit,
    isRunning = false
}: AssessmentInputProps) {

    // Render Coding Interface
    if (question.type === 'coding') {
        return (
            <CodeEditorMock
                initialCode={question.template}
                onRunCode={onSubmit}
                isRunning={isRunning}
            />
        );
    }

    // Render MCQ Interface (handles both API format and mock format)
    if (question.type === 'mcq' || question.options) {
        return (
            <div className="h-full flex flex-col p-6 max-w-2xl mx-auto w-full">
                <h3 className="text-lg font-medium mb-6">Select the best answer:</h3>
                <RadioGroup
                    value={answer?.toString()}
                    onValueChange={(val) => onAnswerChange(question.options[0]?.id ? val : parseInt(val))}
                    className="space-y-4"
                >
                    {question.options.map((option) => {
                        const optionId = option.id.toString();
                        const isSelected = answer?.toString() === optionId;
                        
                        return (
                            <div key={optionId} className="flex items-center space-x-2">
                                <RadioGroupItem value={optionId} id={optionId} className="peer sr-only" />
                                <Label
                                    htmlFor={optionId}
                                    className="flex items-center w-full p-4 rounded-lg border-2 border-muted bg-card hover:bg-accent hover:text-accent-foreground peer-data-[state=checked]:border-primary peer-data-[state=checked]:bg-primary/5 cursor-pointer transition-all"
                                >
                                    <div className="w-5 h-5 rounded-full border border-primary mr-3 flex items-center justify-center">
                                        {isSelected && <div className="w-2.5 h-2.5 rounded-full bg-primary" />}
                                    </div>
                                    <span className="text-base">{option.text}</span>
                                </Label>
                            </div>
                        );
                    })}
                </RadioGroup>
                <div className="mt-8 flex justify-end">
                    <Button onClick={onSubmit} size="lg" disabled={!answer}>
                        Submit Answer
                    </Button>
                </div>
            </div>
        );
    }

    // Render Text Interface
    if (question.type === 'text') {
        const charCount = (answer as string)?.length || 0;

        return (
            <div className="h-full flex flex-col p-6 max-w-3xl mx-auto w-full">
                <h3 className="text-lg font-medium mb-4">Your Answer:</h3>
                <Card className="flex-1 p-2 flex flex-col">
                    <Textarea
                        value={answer as string || ''}
                        onChange={(e) => onAnswerChange(e.target.value)}
                        placeholder={question.placeholder}
                        className="flex-1 resize-none border-0 focus-visible:ring-0 text-base leading-relaxed p-4"
                        maxLength={question.maxLength}
                    />
                    <div className="p-2 text-right text-xs text-muted-foreground border-t">
                        {charCount} / {question.maxLength} characters
                    </div>
                </Card>
                <div className="mt-6 flex justify-end">
                    <Button onClick={onSubmit} size="lg" disabled={charCount === 0}>
                        Submit Response
                    </Button>
                </div>
            </div>
        );
    }

    // Render Rating/Slider Interface
    if (question.type === 'rating') {
        return (
            <div className="h-full flex flex-col items-center justify-center p-6 max-w-2xl mx-auto w-full">
                <Card className="w-full p-8 space-y-8">
                    <div className="text-center space-y-2">
                        <h3 className="text-2xl font-bold text-primary">{answer || question.min}</h3>
                        <p className="text-muted-foreground">Your Rating</p>
                    </div>

                    <Slider
                        value={[answer || question.min]}
                        min={question.min}
                        max={question.max}
                        step={question.step || 1}
                        onValueChange={(value) => onAnswerChange(value[0])}
                        className="py-4"
                    />

                    <div className="flex justify-between text-sm text-muted-foreground w-full px-1">
                        <span>{question.minLabel}</span>
                        <span>{question.maxLabel}</span>
                    </div>

                    <div className="pt-6 flex justify-center w-full">
                        <Button onClick={onSubmit} size="lg" className="w-full sm:w-auto min-w-[200px]">
                            Confirm Rating
                        </Button>
                    </div>
                </Card>
            </div>
        );
    }

    return <div>Unknown question type</div>;
}
