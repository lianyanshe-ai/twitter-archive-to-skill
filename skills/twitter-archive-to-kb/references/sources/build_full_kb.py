#!/usr/bin/env python3
"""
Twitter Archive to Markdown Knowledge Base
Reference implementation
"""
import json
import re
import os
from datetime import datetime

def slugify(title):
    """Convert title to filename-safe slug"""
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s-]+', '-', slug.strip())
    return slug[:50]

def extract_tags(text):
    """Extract hashtags from text"""
    tags = re.findall(r'#(\w+)', text)
    return list(set(tags))

def parse_js_file(file_path):
    """Parse Twitter export .js file that starts with window.YTD.*"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find where the JSON array starts after the variable declaration
    match = re.search(r'window\.YTD\.[^=]+=\s*(.*)', content, re.DOTALL)
    if match:
        json_str = match.group(1)
    else:
        json_str = content

    data = json.loads(json_str)
    return data

def is_retweet_or_reply(text):
    """Check if this is a retweet or reply"""
    # Reply starts with @username
    if text.strip().startswith('@'):
        return True
    # Retweet starts with RT @
    if text.strip().startswith('RT '):
        return True
    return False

def write_markdown_file(output_dir, item_id, title, date_obj, content, url, tags, source_type):
    """Write a single markdown file with frontmatter"""
    if not title or title.strip() == '':
        # Use first few words as title
        words = content.strip().split()[:8]
        title = ' '.join(words)
        if not title:
            title = f"untitled-{item_id}"

    date_str = date_obj.strftime('%Y-%m-%d')
    year = date_obj.strftime('%Y')
    month = date_obj.strftime('%m')

    # Create directory
    dir_path = os.path.join(output_dir, year, month)
    os.makedirs(dir_path, exist_ok=True)

    # Create filename
    slug = slugify(title)
    filename = f"{date_str}-{slug}-{item_id}.md"
    filepath = os.path.join(dir_path, filename)

    # Build frontmatter
    frontmatter = [
        '---',
        f'title: "{title.replace('"', '\\"')}"',
        f'date: {date_str}',
        f'tweet_id: {item_id}',
        f'url: {url}',
        f'source: {source_type}',
    ]
    if tags:
        frontmatter.append(f'tags: [{", ".join(f"`{tag}`" for tag in tags)}]')
    frontmatter.append('---\n')

    # Combine everything
    full_content = '\n'.join(frontmatter) + '\n' + content.strip() + '\n'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(full_content)

    return filepath

def process_tweets(tweets_js_path, output_dir):
    """Process tweets.js, filter out replies and retweets"""
    data = parse_js_file(tweets_js_path)

    count = 0
    kept = 0

    for item in data:
        tweet = item.get('tweet', {})
        tweet_id = tweet.get('id_str', '')
        full_text = tweet.get('full_text', '')
        created_at = tweet.get('created_at', '')

        if is_retweet_or_reply(full_text):
            continue

        # Parse date: "Mon Apr 07 12:34:56 +0000 2025"
        try:
            date_obj = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        except:
            date_obj = datetime.now()

        # Extract title from first line
        lines = [line.strip() for line in full_text.split('\n') if line.strip()]
        if lines:
            title = lines[0]
        else:
            title = full_text[:60]

        tags = extract_tags(full_text)
        url = f"https://twitter.com/i/web/status/{tweet_id}"

        write_markdown_file(output_dir, tweet_id, title, date_obj, full_text, url, tags, 'tweet')
        kept += 1
        count += 1

    print(f"Processed tweets: {count} total, kept {kept} (filtered out {count - kept} replies/retweets)")
    return kept

def process_notes(notes_js_path, output_dir):
    """Process note-tweet.js (Twitter Notes long form)"""
    data = parse_js_file(notes_js_path)

    count = 0
    for item in data:
        note = item.get('noteTweet', {})
        note_id = note.get('noteTweetId', '') or note.get('noteId', '') or note.get('id', '')
        if not note_id:
            continue

        # Get the full content from core.text (newer Twitter export format)
        content = ''
        if 'core' in note and 'text' in note['core']:
            content = note['core']['text']
        elif 'entityData' in note and 'blocks' in note['entityData']:
            # Older format
            for block in note['entityData']['blocks']:
                if 'text' in block:
                    content += block['text'] + '\n\n'
        elif 'content' in note:
            content = note['content']

        if not content.strip():
            continue

        # Get date from updatedAt (could be ISO string or timestamp)
        updated_at = note.get('updatedAt', '') or note.get('createdAt', '')
        date_obj = datetime.now()
        if updated_at:
            # Try ISO string format first (e.g. "2023-08-12T15:31:27.000Z")
            try:
                date_obj = datetime.strptime(updated_at, '%Y-%m-%dT%H:%M:%S.%fZ')
            except ValueError:
                # Try unix timestamp
                try:
                    date_obj = datetime.fromtimestamp(int(updated_at) / 1000)
                except:
                    pass

        # Extract title from first line
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if lines:
            title = lines[0]
        else:
            title = content[:60]

        tags = extract_tags(content)
        url = f"https://twitter.com/i/web/status/{note_id}"

        write_markdown_file(output_dir, note_id, title, date_obj, content, url, tags, 'note')
        count += 1

    print(f"Processed notes: {count} total")
    return count

def process_articles(articles_js_path, output_dir):
    """Process article.js (Twitter Articles)"""
    data = parse_js_file(articles_js_path)

    count = 0
    for item in data:
        article = item.get('article', {})
        article_id = article.get('id', '')
        if not article_id:
            continue

        # Reconstruct content from blocks
        content = ''
        if 'content' in article and 'blocks' in article['content']:
            blocks = article['content']['blocks']
            for block in blocks:
                if 'text' in block:
                    content += block['text'] + '\n\n'

        if not content.strip():
            continue

        # Get created_at if available
        created_at = article.get('createdAt', '')
        if created_at:
            try:
                date_obj = datetime.fromtimestamp(int(created_at) / 1000)
            except:
                date_obj = datetime.now()
        else:
            date_obj = datetime.now()

        # Extract title from first block
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        if lines:
            title = lines[0]
        else:
            title = content[:60]

        tags = extract_tags(content)
        url = f"https://twitter.com/i/web/status/{article_id}"

        # Add cover image if exists
        if 'coverMedia' in article and article['coverMedia']:
            content += f'\n\n![Cover]({article["coverMedia"]})\n'

        write_markdown_file(output_dir, article_id, title, date_obj, content, url, tags, 'article')
        count += 1

    print(f"Processed articles: {count} total")
    return count

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # If running from skill directory, adjust data path
    # User should run this from their archive root directory
    data_dir = './data'
    output_dir = './twitter-notes-kb'

    print(f"Starting full knowledge base build...")
    print(f"Output directory: {output_dir}")

    total = 0

    # Process tweets.js (filter replies/retweets)
    tweets_path = os.path.join(data_dir, 'tweets.js')
    if os.path.exists(tweets_path):
        kept = process_tweets(tweets_path, output_dir)
        total += kept
    else:
        print(f"Warning: {tweets_path} not found")

    # Process note-tweet.js
    notes_path = os.path.join(data_dir, 'note-tweet.js')
    if os.path.exists(notes_path):
        note_count = process_notes(notes_path, output_dir)
        total += note_count
    else:
        print(f"Warning: {notes_path} not found")

    # Process article.js
    articles_path = os.path.join(data_dir, 'article.js')
    if os.path.exists(articles_path):
        article_count = process_articles(articles_path, output_dir)
        total += article_count
    else:
        print(f"Warning: {articles_path} not found")

    print(f"\n✅ Complete! Total files written: {total}")
    print(f"All files saved to: {output_dir}")

if __name__ == '__main__':
    main()
