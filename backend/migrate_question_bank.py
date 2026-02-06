"""
Migration Script: Populate Coding Question Bank from Local Files

This script scans the local coding problems folder, parses all questions,
and stores them in the Supabase question bank table.

Usage:
    python migrate_question_bank.py
    python migrate_question_bank.py --dry-run
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.services.coding_question_bank import CodingQuestionBankService
from app.config import Config
from app.CodeExecution.problem_parser import scan_sample_problems, parse_python_problem_file, format_problem_for_db


def validate_supabase_config():
    """Validate that Supabase configuration exists"""
    if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
        print("❌ ERROR: Supabase configuration not found!")
        print("   Please set SUPABASE_URL and SUPABASE_KEY in your .env file")
        return False
    
    print(f"✅ Supabase URL: {Config.SUPABASE_URL[:30]}...")
    print(f"✅ Supabase Key: {Config.SUPABASE_KEY[:20]}...")
    return True


def get_sample_problems_directory():
    """Get the path to the sample problems directory"""
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(
        backend_dir,
        '..',
        'CODING SAMPLE QUESTIONS',
        'coding-problems'
    )
    
    base_dir = os.path.normpath(base_dir)
    
    if not os.path.exists(base_dir):
        print(f"❌ ERROR: Sample problems directory not found: {base_dir}")
        return None
    
    print(f"✅ Sample problems directory: {base_dir}")
    return base_dir


def migrate_question(question_data, bank_id, dry_run=False):
    """
    Migrate a single question to the bank
    
    Args:
        question_data: Parsed question data dictionary
        bank_id: ID to assign to the question
        dry_run: If True, don't actually save
        
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        title = question_data.get('title')
        
        # Check if question already exists
        if not dry_run:
            exists = CodingQuestionBankService.question_exists(title)
            if exists:
                return False, f"Question '{title}' already exists in bank"
        
        # Format for database
        db_data = format_problem_for_db(question_data)
        
        # Add bank_id and source file
        db_data['bank_id'] = bank_id
        db_data['source_file'] = question_data.get('file_path', '')
        
        # Ensure time_limit is in seconds (not milliseconds)
        if 'time_limit' in db_data and db_data['time_limit'] > 1000:
            db_data['time_limit'] = db_data['time_limit'] // 1000
        
        if dry_run:
            return True, f"Would migrate: {title}"
        
        # Create in Supabase
        created = CodingQuestionBankService.create_question(db_data)
        
        if created:
            return True, f"Successfully migrated: {title}"
        else:
            return False, f"Failed to create in Supabase: {title}"
            
    except Exception as e:
        return False, f"Error migrating {question_data.get('title', 'unknown')}: {str(e)}"


def migrate_all_questions(dry_run=False):
    """
    Migrate all questions from local files to question bank
    
    Args:
        dry_run: If True, only shows what would be migrated without actually doing it
    """
    print("\n" + "="*70)
    print("🚀 QUESTION BANK MIGRATION: Local Files → Supabase")
    print("="*70 + "\n")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No changes will be made\n")
    
    # Validate configuration
    if not validate_supabase_config():
        return
    
    # Get sample problems directory
    base_dir = get_sample_problems_directory()
    if not base_dir:
        return
    
    # Create Flask app context
    app = create_app()
    
    with app.app_context():
        try:
            # Scan all problems
            print("\n📂 Scanning local problem files...\n")
            problems = scan_sample_problems(base_dir)
            total_problems = len(problems)
            
            print(f"📊 Found {total_problems} problems in local files\n")
            
            if total_problems == 0:
                print("ℹ️  No problems to migrate")
                return
            
            # Get existing questions from bank (if not dry run)
            existing_titles = set()
            if not dry_run:
                existing_questions = CodingQuestionBankService.get_all_questions()
                existing_titles = {q.get('title') for q in existing_questions}
                print(f"ℹ️  Found {len(existing_titles)} existing questions in bank\n")
            
            # Migrate each problem
            migrated = 0
            skipped = 0
            failed = 0
            
            print("\n📝 Migration Progress:\n")
            print("-" * 70)
            
            for idx, problem in enumerate(problems, 1):
                status_prefix = f"[{idx}/{total_problems}]"
                bank_id = idx  # Use sequential bank IDs
                
                if dry_run:
                    # In dry run mode, just check if it would be migrated
                    if problem['title'] in existing_titles:
                        print(f"{status_prefix} ⏭️  SKIP: {problem['title']} (already exists)")
                        skipped += 1
                    else:
                        print(f"{status_prefix} ✅ WOULD MIGRATE: {problem['title']} ({problem['category']})")
                        migrated += 1
                else:
                    # Actually migrate
                    success, message = migrate_question(problem, bank_id, dry_run=False)
                    
                    if success:
                        print(f"{status_prefix} ✅ {message} ({problem['category']})")
                        migrated += 1
                        existing_titles.add(problem['title'])
                    elif "already exists" in message:
                        print(f"{status_prefix} ⏭️  {message}")
                        skipped += 1
                    else:
                        print(f"{status_prefix} ❌ {message}")
                        failed += 1
            
            # Summary
            print("\n" + "="*70)
            print("📈 MIGRATION SUMMARY")
            print("="*70)
            print(f"Total questions scanned: {total_problems}")
            print(f"✅ Successfully migrated: {migrated}")
            print(f"⏭️  Skipped (already exist): {skipped}")
            print(f"❌ Failed: {failed}")
            print("="*70 + "\n")
            
            if dry_run:
                print("⚠️  This was a DRY RUN - no changes were made")
                print("   Run without --dry-run flag to actually migrate\n")
            elif failed > 0:
                print("⚠️  Some questions failed to migrate. Check the errors above.\n")
            elif migrated > 0:
                print("🎉 Migration completed successfully!")
                print("   Your question bank is now populated in Supabase!\n")
                print("📋 Next steps:")
                print("   1. Go to recruiter dashboard")
                print("   2. Click 'Import from Bank'")
                print("   3. Questions will now load from Supabase!\n")
            else:
                print("ℹ️  All questions already exist in the bank\n")
                
        except Exception as e:
            print(f"\n❌ MIGRATION ERROR: {str(e)}")
            import traceback
            traceback.print_exc()


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Migrate coding question bank from local files to Supabase'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry run without actually migrating data'
    )
    
    args = parser.parse_args()
    
    try:
        migrate_all_questions(dry_run=args.dry_run)
    except KeyboardInterrupt:
        print("\n\n⚠️  Migration cancelled by user")
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
