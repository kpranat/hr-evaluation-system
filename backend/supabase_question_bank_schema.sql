-- ============================================
-- SUPABASE SCHEMA: Coding Question Bank Table
-- ============================================
-- This schema creates the coding_question_bank table in Supabase
-- This stores the repository of available questions for import
-- Run this SQL in your Supabase SQL Editor

-- Create coding_question_bank table
CREATE TABLE IF NOT EXISTS coding_question_bank (
    id BIGSERIAL PRIMARY KEY,
    bank_id INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    difficulty TEXT NOT NULL DEFAULT 'medium' CHECK (difficulty IN ('easy', 'medium', 'hard')),
    
    -- Starter code for different languages
    starter_code_python TEXT,
    starter_code_javascript TEXT,
    starter_code_java TEXT,
    starter_code_cpp TEXT,
    
    -- Test cases stored as JSONB array
    test_cases JSONB NOT NULL DEFAULT '[]'::jsonb,
    
    -- Execution limits
    time_limit INTEGER NOT NULL DEFAULT 5, -- seconds
    memory_limit INTEGER NOT NULL DEFAULT 256, -- MB
    
    -- Organization and categorization
    category TEXT DEFAULT 'general',
    tags TEXT[] DEFAULT '{}',
    
    -- Source information
    source_file TEXT, -- Original file path if imported from files
    
    -- Metadata
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_question_bank_bank_id ON coding_question_bank(bank_id);
CREATE INDEX IF NOT EXISTS idx_question_bank_difficulty ON coding_question_bank(difficulty);
CREATE INDEX IF NOT EXISTS idx_question_bank_category ON coding_question_bank(category);
CREATE INDEX IF NOT EXISTS idx_question_bank_created_at ON coding_question_bank(created_at DESC);

-- Create index for full-text search on title and description
CREATE INDEX IF NOT EXISTS idx_question_bank_search ON coding_question_bank 
USING GIN (to_tsvector('english', title || ' ' || description));

-- Create GIN index on tags for array operations
CREATE INDEX IF NOT EXISTS idx_question_bank_tags ON coding_question_bank USING GIN (tags);

-- Function to auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_question_bank_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to call the function before updates
CREATE TRIGGER trigger_update_question_bank_updated_at
    BEFORE UPDATE ON coding_question_bank
    FOR EACH ROW
    EXECUTE FUNCTION update_question_bank_updated_at();

-- Enable Row Level Security (RLS)
ALTER TABLE coding_question_bank ENABLE ROW LEVEL SECURITY;

-- RLS Policies (adjust based on your auth setup)
-- Allow everyone to read questions
CREATE POLICY "Enable read access for all users" ON coding_question_bank
    FOR SELECT USING (true);

-- Allow authenticated users to insert (for migration scripts)
CREATE POLICY "Enable insert for authenticated users" ON coding_question_bank
    FOR INSERT WITH CHECK (true);

-- Allow authenticated users to update
CREATE POLICY "Enable update for authenticated users" ON coding_question_bank
    FOR UPDATE USING (true);

-- Allow authenticated users to delete
CREATE POLICY "Enable delete for authenticated users" ON coding_question_bank
    FOR DELETE USING (true);

-- ============================================
-- SAMPLE QUERY EXAMPLES
-- ============================================

-- Get all questions
-- SELECT * FROM coding_question_bank ORDER BY bank_id;

-- Get questions by category
-- SELECT * FROM coding_question_bank WHERE category = 'Arrays';

-- Get questions by difficulty
-- SELECT * FROM coding_question_bank WHERE difficulty = 'easy';

-- Full-text search
-- SELECT * FROM coding_question_bank 
-- WHERE to_tsvector('english', title || ' ' || description) @@ to_tsquery('english', 'array & sum');

-- Count questions by category
-- SELECT category, COUNT(*) FROM coding_question_bank GROUP BY category;

-- Get questions with specific tags
-- SELECT * FROM coding_question_bank WHERE tags @> ARRAY['dynamic-programming'];
