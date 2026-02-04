import { AssessmentQuestion } from '@/types/assessment';
import { AssessmentRound } from '@/types/rounds';

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

// Organize questions by round
export const questionsByRound: Record<AssessmentRound, AssessmentQuestion[]> = {
    mcq: [
        {
            id: 101,
            type: 'mcq',
            title: 'Team Collaboration',
            description: 'Your team is working on a tight deadline. A team member asks for help, but you are also behind on your own tasks. What do you do?',
            options: [
                { id: 'a', text: 'Help them immediately, as teamwork is priority' },
                { id: 'b', text: 'Schedule time after completing your critical tasks' },
                { id: 'c', text: 'Direct them to documentation or other resources' },
                { id: 'd', text: 'Decline politely and focus on your work' }
            ]
        },
        {
            id: 102,
            type: 'mcq',
            title: 'Code Review Ethics',
            description: 'You notice a colleague\'s code that could be significantly improved. How do you approach code review feedback?',
            options: [
                { id: 'a', text: 'Provide direct criticism to ensure quality' },
                { id: 'b', text: 'Offer constructive suggestions with examples' },
                { id: 'c', text: 'Approve it to maintain good relationships' },
                { id: 'd', text: 'Rewrite it yourself and submit a new PR' }
            ]
        },
        {
            id: 103,
            type: 'mcq',
            title: 'Technical Disagreement',
            description: 'You disagree with the technical approach proposed by your team lead. What is your best course of action?',
            options: [
                { id: 'a', text: 'Follow the lead\'s decision without question' },
                { id: 'b', text: 'Present your concerns with supporting evidence privately' },
                { id: 'c', text: 'Challenge it publicly in the team meeting' },
                { id: 'd', text: 'Implement your approach and show results later' }
            ]
        },
        {
            id: 104,
            type: 'mcq',
            title: 'Agile Methodology',
            description: 'In Scrum, what is the primary purpose of a Sprint Retrospective?',
            options: [
                { id: 'a', text: 'To review and demo completed work to stakeholders' },
                { id: 'b', text: 'To plan the next sprint\'s work items' },
                { id: 'c', text: 'To reflect on the process and identify improvements' },
                { id: 'd', text: 'To assign tasks to team members' }
            ],
            correctOptionId: 'c'
        },
        {
            id: 105,
            type: 'mcq',
            title: 'Version Control',
            description: 'What is the primary advantage of using feature branches in Git?',
            options: [
                { id: 'a', text: 'Faster code execution' },
                { id: 'b', text: 'Isolated development without affecting main branch' },
                { id: 'c', text: 'Automatic bug detection' },
                { id: 'd', text: 'Reduced storage requirements' }
            ],
            correctOptionId: 'b'
        }
    ],
    psychometric: [
        {
            id: 201,
            type: 'rating',
            title: 'Self-Assessment: Adaptability',
            description: 'How comfortable are you with sudden changes in project requirements or priorities?',
            min: 1,
            max: 10,
            minLabel: 'Prefer stable, predictable work',
            maxLabel: 'Thrive in dynamic environments'
        },
        {
            id: 202,
            type: 'rating',
            title: 'Self-Assessment: Communication',
            description: 'Rate your ability to explain complex technical concepts to non-technical stakeholders.',
            min: 1,
            max: 10,
            minLabel: 'Prefer technical-only discussions',
            maxLabel: 'Excellent at simplifying complexity'
        },
        {
            id: 203,
            type: 'rating',
            title: 'Self-Assessment: Continuous Learning',
            description: 'How actively do you pursue learning new technologies and skills?',
            min: 1,
            max: 10,
            minLabel: 'Learn only when required',
            maxLabel: 'Constantly exploring new tech'
        },
        {
            id: 204,
            type: 'text',
            title: 'Conflict Resolution',
            description: 'Describe a time when you had a significant disagreement with a team member about a technical decision. How did you handle it, and what was the outcome?',
            maxLength: 500,
            placeholder: 'Share your experience...'
        },
        {
            id: 205,
            type: 'text',
            title: 'Work Style',
            description: 'What type of work environment helps you perform at your best? Consider factors like collaboration vs. individual work, structure vs. flexibility, etc.',
            maxLength: 400,
            placeholder: 'Describe your ideal work environment...'
        },
        {
            id: 206,
            type: 'rating',
            title: 'Self-Assessment: Problem Solving',
            description: 'When faced with a complex problem, how would you rate your systematic approach to breaking it down?',
            min: 1,
            max: 10,
            minLabel: 'Tend to get overwhelmed',
            maxLabel: 'Excellent at decomposition'
        }
    ],
    technical: [
        {
            id: 301,
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
            id: 302,
            type: 'coding',
            title: 'Valid Palindrome',
            description: 'A phrase is a **palindrome** if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.\n\nGiven a string `s`, return `true` if it is a palindrome, or `false` otherwise.',
            language: 'python',
            template: 'def isPalindrome(s: str) -> bool:\n    ',
            examples: [
                { input: 's = "A man, a plan, a canal: Panama"', output: 'true', explanation: '"amanaplanacanalpanama" is a palindrome.' },
                { input: 's = "race a car"', output: 'false', explanation: '"raceacar" is not a palindrome.' }
            ],
            constraints: [
                '1 <= s.length <= 2 * 10^5',
                's consists only of printable ASCII characters.'
            ]
        },
        {
            id: 303,
            type: 'text',
            title: 'System Design: Rate Limiter',
            description: 'Describe how you would design a rate limiter for a high-traffic API. What algorithms would you consider (token bucket, leaky bucket, fixed window, sliding window)? What trade-offs would you make regarding precision vs. performance?',
            maxLength: 1000,
            placeholder: 'Explain your design approach...'
        },
        {
            id: 304,
            type: 'coding',
            title: 'Reverse Linked List',
            description: 'Given the head of a singly linked list, reverse the list, and return the reversed list.',
            language: 'python',
            template: 'def reverseList(head: Optional[ListNode]) -> Optional[ListNode]:\n    ',
            examples: [
                { input: 'head = [1,2,3,4,5]', output: '[5,4,3,2,1]' },
                { input: 'head = [1,2]', output: '[2,1]' },
                { input: 'head = []', output: '[]' }
            ],
            constraints: [
                'The number of nodes in the list is the range [0, 5000].',
                '-5000 <= Node.val <= 5000'
            ]
        }
    ]
};
