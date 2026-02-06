-- ============================================
-- COPY DATA: coding_problems → coding_question_bank
-- ============================================
-- Run this in Supabase SQL Editor if your data is in the wrong table
-- This copies all data from coding_problems to coding_question_bank

-- First, make sure coding_question_bank table exists with correct schema
-- (If it doesn't, run the supabase_question_bank_schema.sql first)

-- Copy data from coding_problems to coding_question_bank
-- Mapping fields appropriately
INSERT INTO coding_question_bank (
    bank_id,
    title,
    description,
    difficulty,
    starter_code_python,
    starter_code_javascript,
    starter_code_java,
    starter_code_cpp,
    test_cases,
    time_limit,
    memory_limit,
    category,
    tags,
    source_file,
    created_at,
    updated_at
)
SELECT 
    problem_id as bank_id,                    -- Use problem_id as bank_id
    title,
    description,
    difficulty,
    starter_code_python,
    starter_code_javascript,
    starter_code_java,
    starter_code_cpp,
    test_cases_json as test_cases,            -- Field name mapping
    time_limit / 1000 as time_limit,          -- Convert milliseconds to seconds
    memory_limit,
    'general' as category,                     -- Default category
    '{}' as tags,                              -- Default empty tags
    NULL as source_file,                       -- No source file info
    created_at,
    NOW() as updated_at
FROM coding_problems
WHERE problem_id NOT IN (
    SELECT bank_id FROM coding_question_bank
)
ORDER BY problem_id;

-- Verify the copy
SELECT COUNT(*) as total_copied FROM coding_question_bank;

-- Show sample data
SELECT bank_id, title, difficulty, test_cases 
FROM coding_question_bank 
ORDER BY bank_id 
LIMIT 5;
