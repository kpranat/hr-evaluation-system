/**
 * API Client for Flask Backend
 * Backend runs on port 5000
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return { data, error: null };
  } catch (error) {
    return {
      data: null,
      error: error instanceof Error ? error.message : 'An error occurred',
    };
  }
}

// ============ Candidate Endpoints ============

export const candidateApi = {
  /** Upload resume for evaluation */
  uploadResume: async (file: File) => {
    const formData = new FormData();
    formData.append('resume', file);
    // TODO: Implement actual upload
    return request('/api/candidates/upload', {
      method: 'POST',
      body: formData,
    });
  },

  /** Get assessment questions */
  getAssessment: async (assessmentId: string) => {
    return request(`/api/assessments/${assessmentId}`);
  },

  /** Submit assessment answers */
  submitAssessment: async (assessmentId: string, answers: Record<string, unknown>) => {
    return request(`/api/assessments/${assessmentId}/submit`, {
      method: 'POST',
      body: JSON.stringify(answers),
    });
  },
};

// ============ Admin/Recruiter Endpoints ============

export const adminApi = {
  /** Get all candidates */
  getCandidates: async () => {
    return request('/api/admin/candidates');
  },

  /** Get single candidate details */
  getCandidate: async (candidateId: string) => {
    return request(`/api/admin/candidates/${candidateId}`);
  },

  /** Get analytics dashboard data */
  getAnalytics: async () => {
    return request('/api/admin/analytics');
  },

  /** Update settings */
  updateSettings: async (settings: Record<string, unknown>) => {
    return request('/api/admin/settings', {
      method: 'PUT',
      body: JSON.stringify(settings),
    });
  },
};

export default {
  candidate: candidateApi,
  admin: adminApi,
};
