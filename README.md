# AI Tags Generator

[![ai-tags-generator](https://img.shields.io/badge/LICENSE-AGPL3%20Liscense-blue?style=flat-square)](./LICENSE)
[![ai-tags-generator](https://img.shields.io/badge/GitHub-AI%20Tags%20Genrator-blueviolet?style=flat-square&logo=github)](https://github.com/fernvenue/ai-tags-generator)
[![ai-tags-generator](https://img.shields.io/badge/GitLab-AI%20Tags%20Genrator-orange?style=flat-square&logo=gitlab)](https://gitlab.com/fernvenue/ai-tags-generator)

Use AI to automatically generate tags for your articles.

## Features

If you think it's troublesome to write tags for each article, I feel the same way! So I created this tool, which performs well on my Hugo blog and can also work well with any markdown format article based on other framework!

- [x] Automatically identify unlabeled articles and generate tags;
- [x] Support for customizing API key via CLI and environment variables;
- [x] Support for specifying directories;
- [x] Support for listing only without modifications;
- [x] Support for forced updates;
- [x] Comprehensive logging output system;
- [x] Support for automatic recognition of multilingual articles;
- [x] Support for specifying models;
- [ ] Support for accessing API using a proxy;

## Usage

### Command Line Arguments

- `--list-only`: Only list articles without tags, don't generate new ones;
- `--force-update`: Force update tags for all articles, regardless of existing tags;
- `--specific-path PATH`: Specify custom path to generate tags for (default: './content/');
- `--api-key KEY`: Provide OpenAI API key (alternatively, set OPENAI_API_KEY environment variable);
