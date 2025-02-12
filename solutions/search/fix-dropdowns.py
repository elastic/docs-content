#!/usr/bin/env python3
import os
import re

def clean_dropdown_line(line):
    """Clean formatting from dropdown lines."""
    # Match dropdown syntax with any number of colons and potential formatting
    dropdown_pattern = r'(:{2,})\s*{dropdown}\s*(.+?)\s*$'
    
    if match := re.match(dropdown_pattern, line):
        colons = match.group(1)
        content = match.group(2)
        
        # Remove markdown formatting
        cleaned_content = (
            content
            .replace('**', '')  # Remove bold
            .replace('*', '')   # Remove italic
            .replace('__', '')  # Remove alternate bold
            .replace('_', '')   # Remove alternate italic
            .replace('`', '')   # Remove code formatting
            .strip()            # Remove extra whitespace
        )
        
        # Reconstruct the dropdown line
        return f'{colons}{{dropdown}} {cleaned_content}\n'
    
    return line

def process_file(filepath):
    """Process a single file to clean dropdown formatting."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        modified = False
        new_lines = []
        
        for line in lines:
            if '{dropdown}' in line:
                cleaned_line = clean_dropdown_line(line)
                if cleaned_line != line:
                    modified = True
                new_lines.append(cleaned_line)
            else:
                new_lines.append(line)
        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            return True
        
        return False
    
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

def process_markdown_files(directory):
    """Recursively process all markdown files in directory."""
    modified_count = 0
    skipped_count = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                if process_file(filepath):
                    print(f"Modified: {filepath}")
                    modified_count += 1
                else:
                    print(f"Skipped: {filepath}")
                    skipped_count += 1
    
    return modified_count, skipped_count

if __name__ == "__main__":
    current_dir = os.getcwd()
    print(f"Processing markdown files in: {current_dir}")
    
    modified, skipped = process_markdown_files(current_dir)
    
    print(f"\nSummary:")
    print(f"Files modified: {modified}")
    print(f"Files skipped: {skipped}")