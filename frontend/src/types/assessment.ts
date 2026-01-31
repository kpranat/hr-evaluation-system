export type QuestionType = 'coding' | 'mcq' | 'text' | 'rating';

export interface BaseQuestion {
    id: number;
    type: QuestionType;
    title: string;
    description: string;
}

export interface CodingQuestion extends BaseQuestion {
    type: 'coding';
    language: string;
    template: string;
    testCases?: { input: string; output: string }[];
    constraints?: string[];
    examples?: { input: string; output: string; explanation?: string }[];
}

export interface MCQQuestion extends BaseQuestion {
    type: 'mcq';
    options: { id: string; text: string }[];
    correctOptionId?: string; // Hidden from frontend in real app, but useful for mock
}

export interface TextQuestion extends BaseQuestion {
    type: 'text';
    maxLength?: number;
    placeholder?: string;
}

export interface RatingQuestion extends BaseQuestion {
    type: 'rating';
    minLabel: string;
    maxLabel: string;
    min: number;
    max: number;
    step?: number;
}

export type AssessmentQuestion = CodingQuestion | MCQQuestion | TextQuestion | RatingQuestion;
