#!/usr/bin/env python3
"""
Script to push all changes to Git
"""

import subprocess
import sys

def run_command(command):
    """Run a shell command and return the output"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def push_to_git():
    """Push all changes to Git"""
    print("Pushing changes to Git...")
    
    # Add all files
    print("Adding files...")
    run_command("git add .")
    
    # Commit changes
    commit_message = "Update documentation, remove credentials, and improve security"
    print(f"Committing with message: {commit_message}")
    run_command(f'git commit -m "{commit_message}"')
    
    # Push to remote
    print("Pushing to remote...")
    result = run_command("git push")
    
    if result is not None:
        print("Successfully pushed changes to Git!")
    else:
        print("Failed to push changes to Git.")

if __name__ == "__main__":
    print("GenAI Pipeline - Push to Git")
    print("===========================")
    
    confirm = input("Push all changes to Git? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)
    
    push_to_git()