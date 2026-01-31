import { AssessmentQuestion } from '@/types/assessment';

export interface Candidate {
    id: string;
    name: string;
    role: string;
    technical_score: number;
    soft_skill_score: number;
    status: 'High Match' | 'Potential' | 'Reject';
}

export interface IntegrityLog {
    timestamp: string;
    event: string;
    severity: 'low' | 'medium' | 'high';
}

export interface CandidateDetail extends Candidate {
    verdict: 'Hire' | 'No-Hire';
    ai_rationale: string;
    integrity_logs: IntegrityLog[];
    applied_date: string;
    email: string;
}

export const mockCandidates: Candidate[] = [
    {
        id: "1",
        name: "Sarah Chen",
        role: "Senior Frontend Engineer",
        technical_score: 92,
        soft_skill_score: 88,
        status: "High Match"
    },
    {
        id: "2",
        name: "Michael Ross",
        role: "Backend Developer",
        technical_score: 75,
        soft_skill_score: 60,
        status: "Potential"
    },
    {
        id: "3",
        name: "David Kim",
        role: "Full Stack Engineer",
        technical_score: 45,
        soft_skill_score: 50,
        status: "Reject"
    },
    {
        id: "4",
        name: "Emily Watson",
        role: "Product Designer",
        technical_score: 85,
        soft_skill_score: 95,
        status: "High Match"
    },
    {
        id: "5",
        name: "James Liu",
        role: "DevOps Engineer",
        technical_score: 68,
        soft_skill_score: 72,
        status: "Potential"
    }
];

export const mockCandidateDetails: Record<string, CandidateDetail> = {
    "1": {
        ...mockCandidates[0],
        verdict: "Hire",
        email: "sarah.chen@example.com",
        applied_date: "2024-02-01",
        ai_rationale: "Candidate demonstrated exceptional problem-solving skills in the system design interview. Her code was clean, well-documented, and efficient. Psychometric profiling indicates strong leadership potential and high emotional intelligence, making her a great culture fit for the senior role.",
        integrity_logs: [
            { timestamp: "10:02 AM", event: "Assessment Started", severity: "low" },
            { timestamp: "10:15 AM", event: "Browser Focus Lost (2s)", severity: "low" },
            { timestamp: "10:45 AM", event: "Assessment Submitted", severity: "low" }
        ]
    },
    "2": {
        ...mockCandidates[1],
        verdict: "No-Hire",
        email: "michael.ross@example.com",
        applied_date: "2024-02-02",
        ai_rationale: "While technical skills are adequate, the candidate struggled with basic data structures. More importantly, multiple integrity violations were detected during the coding session.",
        integrity_logs: [
            { timestamp: "11:05 AM", event: "Tab Switch Detected", severity: "medium" },
            { timestamp: "11:06 AM", event: "Copy/Paste Event", severity: "medium" },
            { timestamp: "11:20 AM", event: "Multiple Faces Detected", severity: "high" }
        ]
    }
};

export const mockQuestions: AssessmentQuestion[] = [
    {
        id: 1,
        type: 'mcq',
        title: 'Workplace Conflict Resolution',
        description: 'You notice a significant error in a colleague\'s code that has already been merged to the main branch. This colleague is senior to you. How do you handle this?',
        options: [
            { id: 'a', text: 'Immediately revert the commit to prevent production issues.' },
            { id: 'b', text: 'Privately reach out to the colleague to discuss the error and potential fixes.' },
            { id: 'c', text: 'Post about the error in the public team channel to warn everyone.' },
            { id: 'd', text: 'Wait for the QA team to catch it to avoid stepping on toes.' }
        ]
    },
    {
        id: 2,
        type: 'coding',
        title: 'Two Sum',
        description: 'Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.',
        language: 'python',
        template: 'def twoSum(nums: List[int], target: int) -> List[int]:\n    ',
        examples: [
            { input: "nums = [2,7,11,15], target = 9", output: "[0,1]", explanation: "Because nums[0] + nums[1] == 9, we return [0, 1]." },
            { input: "nums = [3,2,4], target = 6", output: "[1,2]" }
        ],
        constraints: [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ]
    },
    {
        id: 3,
        type: 'text',
        title: 'System Design Thought Process',
        description: 'Describe how you would design a rate limiter for a high-traffic API. What algorithms would you consider, and what trade-offs would you make regarding precision vs. performance?',
        maxLength: 1000,
        placeholder: 'Type your answer here...'
    },
    {
        id: 4,
        type: 'rating',
        title: 'Self-Assessment: Leadership',
        description: 'Rate your comfort level in leading technical decisions within a team setting.',
        min: 1,
        max: 10,
        minLabel: 'Prefer following instructions',
        maxLabel: 'Comfortable driving technical strategy'
    },
    {
        id: 5,
        type: 'coding',
        title: 'Valid Palindrome',
        description: 'A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.',
        language: 'python',
        template: 'def isPalindrome(s: str) -> bool:\n    ',
        examples: [
            { input: 's = "A man, a plan, a canal: Panama"', output: 'true', explanation: '"amanaplanacanalpanama" is a palindrome.' },
            { input: 's = "race a car"', output: 'false', explanation: '"raceacar" is not a palindrome.' }
        ]
    }
];
