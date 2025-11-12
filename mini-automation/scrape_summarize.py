import pandas as pd
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import time
import sys
from urllib.parse import urlparse

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyBww79MzcA9o9_hJkkoG3q3vAyWJpHI3MU"  # Replace with your API key
genai.configure(api_key=GEMINI_API_KEY)

def read_urls(file_path):
    """Read URLs from various file formats"""
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
            # Assume first column contains URLs
            urls = df.iloc[:, 0].tolist()
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
            urls = df.iloc[:, 0].tolist()
        elif file_path.endswith('.txt'):
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        else:
            raise ValueError("Unsupported file format. Use .csv, .xlsx, or .txt")
        
        return urls
    except Exception as e:
        print(f"Error reading URLs file: {e}")
        sys.exit(1)

def fetch_webpage_info(url, timeout=10):
    """Fetch webpage and extract key information"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title = soup.find('title')
        title = title.get_text().strip() if title else "No title found"
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'property': 'og:description'})
        description = meta_desc.get('content', 'No description found') if meta_desc else "No description found"
        
        # Extract main text content (first 1000 characters)
        paragraphs = soup.find_all('p')
        text_content = ' '.join([p.get_text().strip() for p in paragraphs[:5]])
        text_content = text_content[:1000] if text_content else "No content found"
        
        return {
            'status': 'success',
            'title': title,
            'description': description,
            'content': text_content
        }
        
    except requests.exceptions.Timeout:
        return {'status': 'error', 'error': 'Request timeout'}
    except requests.exceptions.RequestException as e:
        return {'status': 'error', 'error': str(e)}
    except Exception as e:
        return {'status': 'error', 'error': f'Parsing error: {str(e)}'}

def generate_ai_summary(content, model_name='gemini-1.5-flash'):
    """Generate AI summary using Gemini API"""
    try:
        model = genai.GenerativeModel(model_name)
        
        prompt = f"""Summarize the following webpage content in 2-3 sentences. 
        Focus on the main purpose and key information:
        
        {content}"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"Summary generation failed: {str(e)}"

def scrape_and_summarize(urls_file='urls.txt', output_file='scrape_results.csv'):
    """Main function to scrape and summarize webpages"""
    
    print("=" * 70)
    print("WEB SCRAPING & SUMMARIZATION AUTOMATION")
    print("=" * 70)
    
    # Read URLs
    print(f"\\nReading URLs from: {urls_file}")
    urls = read_urls(urls_file)
    print(f"✓ Found {len(urls)} URLs to process\\n")
    
    results = []
    
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Processing: {url}")
        
        # Extract domain
        domain = urlparse(url).netloc
        
        # Fetch webpage info
        print(f"  → Fetching webpage...")
        page_info = fetch_webpage_info(url)
        
        if page_info['status'] == 'error':
            print(f"  ✗ Error: {page_info['error']}")
            results.append({
                'url': url,
                'domain': domain,
                'title': 'N/A',
                'description': 'N/A',
                'ai_summary': f"Error: {page_info['error']}",
                'status': 'failed'
            })
            continue
        
        print(f"  → Generating AI summary...")
        
        # Generate AI summary
        summary_input = f"Title: {page_info['title']}\\n\\nDescription: {page_info['description']}\\n\\nContent: {page_info['content']}"
        ai_summary = generate_ai_summary(summary_input)
        
        results.append({
            'url': url,
            'domain': domain,
            'title': page_info['title'][:100],  # Limit length
            'description': page_info['description'][:200],
            'ai_summary': ai_summary,
            'status': 'success'
        })
        
        print(f"  ✓ Completed\\n")
        
        # Rate limiting - be respectful to servers
        time.sleep(2)
    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total URLs processed: {len(urls)}")
    print(f"Successful: {len([r for r in results if r['status'] == 'success'])}")
    print(f"Failed: {len([r for r in results if r['status'] == 'failed'])}")
    print(f"\\n✓ Results saved to: {output_file}")
    print("=" * 70)
    
    return df

if __name__ == "__main__":
    # You can change the input/output files here
    scrape_and_summarize('url.csv', 'scrape_results.csv')
