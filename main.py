#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse                 # For parsing command line arguments;
import logging                  # For logging;
import os                       # For interacting with the operating system;
import re                       # For regular expressions;

# Logging configuration;
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import the OpenAI library and set the API key;
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Some basic configuration;
CONTENT_DIR = './content/'
TAG_PATTERN = re.compile(r'tags:\s*\[.*?\]', re.DOTALL)
SUMMARY_DELIMITER = '----'

# This function lists all the markdown files in a directory;
def listMarkdownFiles(directory):
    markdownFiles = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # Append the full path to the list;
                markdownFiles.append(os.path.join(root, file))
    return markdownFiles

# This function extracts tags from a markdown file;
def extractTags(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split('---')
            if len(parts) >= 2:
                # Extract the front matter;
                front_matter = parts[1]
                pattern = r'tags:\s*\[(.*?)\]'
                match = re.search(pattern, front_matter)
                if match:
                    try:
                        tags_str = match.group(1)
                        tags = [t.strip(' "\'') for t in tags_str.split(',') if t.strip()]
                        return tags
                    except Exception as e:
                        logging.warning(f"Error parsing tags in {file}: {e}")
                        return []
    except Exception as e:
        logging.error(f"Error reading file {file}: {e}")
    return []

# This function lists articles without tags;
def listArticlesWithoutTags():
    filesWithoutTags = []
    markdownFiles = listMarkdownFiles(CONTENT_DIR)
    # Check if the file has tags;
    for file in markdownFiles:
        tags = extractTags(file)
        if not tags:
            filesWithoutTags.append(file)
    return filesWithoutTags

# This function updates tags for articles;
def updateTags(force=False):
    markdownFiles = listMarkdownFiles(CONTENT_DIR)
    if not force:
        markdownFiles = [f for f in markdownFiles if not extractTags(f)]

    # Check if there are files to process;
    if not markdownFiles:
        logging.info("No files to process :)")
        return

    # Process each file;
    for file in markdownFiles:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            parts = content.split('---', 2)
            if len(parts) >= 2:
                front_matter_lines = parts[1].strip().split('\n')
                front_matter_lines = [line for line in front_matter_lines if not line.startswith('tags:')]
                front_matter = '\n'.join(front_matter_lines)
                # Extract the summary and body;
                body = parts[2] if len(parts) > 2 else ''
                summary = content.split(SUMMARY_DELIMITER)[0]
                # Generate tags using the modle;
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                            {"role": "system", "content": "You are a highly professional senior article classification expert capable of generating classification tags for blog articles. The tags can be detailed down to specific vocabulary, and should use words rather than phrases whenever possible. Each set of generated tags should be carefully selected, highly abstract, strongly representative, and distinctive, with a quantity control of around 6 to 8, depending on the length of the article. Depending on the language of the article, you should generate classification tags in different languages. Your generated tags should pay attention to grammar, such as capitalizing the first letter of phrases, and ensure there is a space between English letters and other languages. Only output the tags, one per line, without adding `-` or `*` symbols to the tags."},
                            {"role": "user", "content": f"Generate tags for the following article:\n\n{summary}"}
                    ],
                    n=1,
                    temperature=0.5
                )
                # Extract the tags;
                tags = response.choices[0].message.content.strip().split('\n')
                tags = [f'"{tag.strip()}"' for tag in tags]
                tags_str = f'tags: [{", ".join(tags)}]'
                new_content = f'---\n{front_matter}\n{tags_str}\n---{body}'
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                logging.info(f"Updated tags for {file}")

# This function parses command line arguments;
def parse_args():
    parser = argparse.ArgumentParser(description='Generate tags for blog posts')
    parser.add_argument('--list-no-tags', action='store_true', help="List articles without tags.")
    parser.add_argument('--generate-tags', action='store_true', help="Generate tags using GPT for articles without tags.")
    parser.add_argument('--force-update', action='store_true', help="Force update tags for all articles.")
    parser.add_argument('--specific-path', type=str, help="Specific path to generate tags for.", default='./content/')
    return parser.parse_args()

# Main function;
def main():
    args = parse_args()
    base_path = args.specific_path
    # Check if the path exists;
    if not os.path.exists(base_path):
        print(f"Error: Path '{base_path}' does not exist :(")
        return
    # Set the content directory;
    global CONTENT_DIR
    CONTENT_DIR = base_path

    # Check if the user wants to list articles without tags;
    if args.list_no_tags:
        noTagFiles = listArticlesWithoutTags()
        if noTagFiles:
            logging.info("Articles without tags:")
            for file in noTagFiles:
                logging.info(f"  - {file}")
        else:
            logging.info("All articles have tags.")
    # Check if the user wants to generate tags;
    if args.generate_tags:
        updateTags(args.force_update)

if __name__ == '__main__':
    main()
