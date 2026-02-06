-- ============================================
-- SUPABASE SCHEMA: Coding Problems Table
-- ============================================
-- This schema creates the coding_problems table in Supabase
-- This stores the active problems assigned to candidates
-- Run this SQL in your Supabase SQL Editor

-- Create coding_problems table
CREATE TABLE IF NOT EXISTS coding_problems (
    id BIGSERIAL PRIMARY KEY,
    problem_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    
    -- Starter code for different languages
    starter_code_python TEXT,
    starter_code_javascript TEXT,
    starter_code_java TEXT,
    starter_code_cpp TEXT,
    
    -- Test cases stored as JSONB array
    -- Format: [{"input": "...", "expected_output": "...", "is_hidden": false}]
    test_cases JSONB NOT NULL DEFAULT '[]'::jsonb,
    
    -- Execution limits
    time_limit_seconds INTEGER NOT NULL DEFAULT 5,
    memory_limit_mb INTEGER NOT NULL DEFAULT 256,
    
    -- Organization and categorization
    category TEXT DEFAULT 'general',
    tags TEXT[] DEFAULT '{}',
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_coding_problems_problem_id ON coding_problems(problem_id);
CREATE INDEX IF NOT EXISTS idx_coding_problems_difficulty ON coding_problems(difficulty);
CREATE INDEX IF NOT EXISTS idx_coding_problems_category ON coding_problems(category);
CREATE INDEX IF NOT EXISTS idx_coding_problems_created_at ON coding_problems(created_at DESC);

-- Create index for full-text search on title and description
CREATE INDEX IF NOT EXISTS idx_coding_problems_search ON coding_problems 
USING GIN (to_tsvector('english', title || ' ' || description));

-- Create GIN index on tags for array operations
CREATE INDEX IF NOT EXISTS idx_coding_problems_tags ON coding_problems USING GIN (tags);

-- Function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_coding_problems_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function before updates
CREATE TRIGGER trigger_update_coding_problems_updated_at
    BEFORE UPDATE ON coding_problems
    FOR EACH ROW
    EXECUTE FUNCTION update_coding_problems_updated_at();

-- Enable Row Level Security (RLS)
ALTER TABLE coding_problems ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth setup)
-- Allow everyone to read problems
CREATE POLICY "Enable read access for all users" ON coding_problems
    FOR SELECT USING (true);

-- Allow authenticated users to insert
CREATE POLICY "Enable insert for authenticated users" ON coding_problems
    FOR INSERT WITH CHECK (true);

-- Allow authenticated users to update
CREATE POLICY "Enable update for authenticated users" ON coding_problems
    FOR UPDATE USING (true);

-- Allow authenticated users to delete
CREATE POLICY "Enable delete for authenticated users" ON coding_problems
    FOR DELETE USING (true);

-- ============================================
-- SAMPLE QUERY EXAMPLES
-- ============================================

-- Get all problems
-- SELECT * FROM coding_problems ORDER BY problem_id;

-- Get problems by difficulty
-- SELECT * FROM coding_problems WHERE difficulty = 'medium';

-- Get problems by category
-- SELECT * FROM coding_problems WHERE category = 'Arrays';

-- Full-text search
-- SELECT * FROM coding_problems 
-- WHERE to_tsvector('english', title || ' ' || description) @@ to_tsquery('english', 'two & sum');

-- Count problems by difficulty
-- SELECT difficulty, COUNT(*) FROM coding_problems GROUP BY difficulty;

-- Get problems with specific tags
-- SELECT * FROM coding_problems WHERE tags @> ARRAY['sorting'];

-- Get recent problems
-- SELECT * FROM coding_problems ORDER BY created_at DESC LIMIT 10;
