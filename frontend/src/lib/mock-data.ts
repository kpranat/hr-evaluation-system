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
