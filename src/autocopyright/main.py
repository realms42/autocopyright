#!/usr/bin/env python3
"""
Copyright (c) 2024. All rights reserved.
"""
import subprocess
import re
from datetime import datetime
import argparse
import os
from difflib import unified_diff

def get_changed_files(repo_path, include_pattern, exclude_pattern):
    """Retrieve a list of changed files including modified, new (untracked), and staged files, filtered by filename and exclusion patterns."""
    modified_cmd = ['git', '-C', repo_path, 'diff', '--name-only', 'HEAD', '--']
    modified_result = subprocess.run(modified_cmd, stdout=subprocess.PIPE, text=True)
    new_cmd = ['git', '-C', repo_path, 'ls-files', '--others', '--exclude-standard', '--cached']
    new_result = subprocess.run(new_cmd, stdout=subprocess.PIPE, text=True)
    if modified_result.returncode == 0 and new_result.returncode == 0:
        modified_files = modified_result.stdout.splitlines()
        new_files = new_result.stdout.splitlines()
        all_files = set(modified_files + new_files)
        if include_pattern:
            all_files = [f for f in all_files if re.search(include_pattern, f)]
        if exclude_pattern:
            exclude_compiled = re.compile(exclude_pattern)
            all_files = [f for f in all_files if not exclude_compiled.search(f)]
        return list(all_files)
    else:
        print("Error retrieving changed files.")
        return []

def calculate_diff(file_path, content, new_content):
    """Calculate and print the diff for the given file."""
    diff = unified_diff(
        content.splitlines(keepends=True),
        new_content.splitlines(keepends=True),
        fromfile=file_path,
        tofile=file_path + " (new)",
        lineterm=''
    )
    diff_output = ''.join(diff)
    if diff_output:
        print(f"Diff for {file_path}:\n{diff_output}")

def copyright_header_update(file_path, copyright_regex, replacement_year, dry_run=False):
    """Update the copyright header in the specified file, with an option for a dry run."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            regex_compiled = re.compile(copyright_regex)
            def replace_year(match):
                return f"{match.group(1)}{replacement_year}{match.group(3)}"
            new_content, n = regex_compiled.subn(replace_year, content)
            if n > 0:
                if dry_run:
                    calculate_diff(file_path, content, new_content)
                else:
                    with open(file_path, 'w', encoding='utf-8') as writable_file:
                        writable_file.write(new_content)
                        print(f"Updated copyright in: {file_path}")
    except IOError as e:
        print(f"Error processing file {file_path}: {e}")

def main(repo_path, copyright_regex, replacement_year, include_pattern, exclude_pattern, dry_run):
    changed_files = get_changed_files(repo_path, include_pattern, exclude_pattern)
    for file_path in changed_files:
        full_path = os.path.join(repo_path, file_path)
        copyright_header_update(full_path, copyright_regex, replacement_year, dry_run=dry_run)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update copyright headers in your project files.")
    parser.add_argument("path", nargs='?', default=os.getcwd(), help="The path to work with. Defaults to current working directory.")
    parser.add_argument("--dry-run", action='store_true', help="Run the script in dry-run mode without applying changes.")
    parser.add_argument("--regex", default=r'(Copyright \(c\) )(\d{4})(.*)', help="Regular expression to match the copyright header. Defaults to a common format.")
    parser.add_argument("--include-pattern", help="Regex pattern to include files by their names.")
    parser.add_argument("--exclude-pattern", help="Regex pattern to exclude files or directories from processing.")
    parser.add_argument("--year", help="The replacement year for the copyright notice. Defaults to the current year.", default=str(datetime.now().year))
    args = parser.parse_args()
    main(args.path, args.regex, args.year, args.include_pattern, args.exclude_pattern, args.dry_run)