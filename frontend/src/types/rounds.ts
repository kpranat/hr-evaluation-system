export type AssessmentRound = 'mcq' | 'psychometric' | 'technical' | 'text-based';

export interface RoundConfig {
  id: AssessmentRound;
  name: string;
  description: string;
  icon: string;
  estimatedTime: number; // in minutes
  order: number;
}

export interface RoundProgress {
  round: AssessmentRound;
  status: 'not-started' | 'in-progress' | 'completed';
  startedAt?: Date;
  completedAt?: Date;
  currentQuestionIndex?: number;
  totalQuestions?: number;
  answers: Record<number, any>;
}

export interface AssessmentState {
  currentRound: AssessmentRound;
  rounds: Record<AssessmentRound, RoundProgress>;
  overallProgress: number; // 0-100
}

export const ROUND_CONFIGS: Record<AssessmentRound, RoundConfig> = {
  mcq: {
    id: 'mcq',
    name: 'Multiple Choice Questions',
    description: 'Test your fundamental knowledge with carefully curated MCQ questions',
    icon: 'CheckSquare',
    estimatedTime: 15,
    order: 1
  },
  psychometric: {
    id: 'psychometric',
    name: 'Psychometric Assessment',
    description: 'Evaluate your personality traits, work style, and soft skills',
    icon: 'Brain',
    estimatedTime: 20,
    order: 2
  },
  technical: {
    id: 'technical',
    name: 'Technical Assessment',
    description: 'Demonstrate your coding skills with real-world programming challenges',
    icon: 'Code',
    estimatedTime: 45,
    order: 3
  },
  'text-based': {
    id: 'text-based',
    name: 'Text-Based Questions',
    description: 'Answer open-ended questions to evaluate your communication and thought process',
    icon: 'FileText',
    estimatedTime: 30,
    order: 4
  }
};

export const ROUND_ORDER: AssessmentRound[] = ['mcq', 'psychometric', 'technical', 'text-based'];
