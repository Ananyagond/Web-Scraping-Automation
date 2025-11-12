# Web Scraping Automation Project

## Overview
This project is a complete web scraping automation solution that extracts data from websites, generates AI summaries using Claude API, and presents the results in an interactive dashboard.

## Project Structure
```
project/
├── scraper.py                 # Main web scraping script
├── scrape_results.csv         # Output CSV file with scraped data
├── dashboard/                 # React dashboard (optional)
│   ├── src/
│   │   └── App.jsx           # Main dashboard component
│   ├── package.json
│   └── README.md
├── README.md                  # This file
├── reflection.txt             # Project reflection
└── ai_assist_log.txt         # AI assistance documentation
```

## Dependencies

### Python Dependencies
```bash
pip install requests beautifulsoup4 anthropic python-dotenv pandas
```

Or install from requirements.txt:
```bash
pip install -r requirements.txt
```

### Required Python Packages:
- `requests` (2.31.0+) - HTTP requests for web scraping
- `beautifulsoup4` (4.12.0+) - HTML parsing
- `anthropic` (0.18.0+) - Claude API integration
- `python-dotenv` (1.0.0+) - Environment variable management
- `pandas` (2.0.0+) - CSV data handling

### React Dashboard Dependencies (Optional)
```bash
cd dashboard
npm install
# or
yarn install
```

Required packages:
- `react` (18.0+)
- `lucide-react` - Icons
- `tailwindcss` - Styling

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd web-scraping-automation
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

## Running the Scraper

### Basic Usage
```bash
python scraper.py
```

### Output
The script generates `scrape_results.csv` with the following columns:
- `url` - Original URL
- `domain` - Extracted domain name
- `title` - Page title
- `description` - Meta description
- `ai_summary` - AI-generated summary
- `status` - Scraping status (success/failed)

### Example Output
```csv
url,domain,title,description,ai_summary,status
https://www.python.org,www.python.org,Welcome to Python.org,Official Python website,Python.org is the official website...,success
```

## Running the Dashboard (Optional)

### Setup React Dashboard
```bash
cd dashboard
npm install
npm start
```

The dashboard will open at `http://localhost:3000` (or another port if 3000 is busy).

### Features
- Search and filter scraped data
- View AI-generated summaries
- Interactive statistics
- Success/failure tracking
- Click-to-expand rows for full summaries

## How It Works

### 1. Web Scraping Process
```
Read URLs → Send HTTP Request → Parse HTML → Extract Data → Handle Errors
```

- Uses `requests` to fetch web pages
- `BeautifulSoup` parses HTML content
- Extracts title, meta description, and main content
- Error handling for failed requests

### 2. AI Summary Generation
```
Scraped Content → Clean Text → Claude API → AI Summary → Store Result
```

- Sends cleaned content to Claude API
- Generates concise summaries (2-3 sentences)
- Handles API rate limits and errors
- Falls back gracefully on failures

### 3. Data Storage
- Results saved to CSV for easy analysis
- Includes status tracking for each URL
- Can be imported into Excel, databases, or dashboards

## Configuration Options

### Modify Scraper Settings
Edit `scraper.py` to adjust:

```python
# Request timeout (seconds)
timeout = 10

# Claude model
model = "claude-sonnet-4-20250514"

# Max tokens for summaries
max_tokens = 150
```

### Add Custom Headers
```python
headers = {
    'User-Agent': 'Your Custom User Agent',
    'Accept-Language': 'en-US,en;q=0.9'
}
```

## Assumptions & Limitations

### Assumptions
1. Input URLs are publicly accessible (no authentication required)
2. Websites allow scraping (check robots.txt)
3. Valid Anthropic API key is provided
4. Stable internet connection
5. CSV input file is properly formatted

### Limitations
1. **Rate Limiting:** Respects website rate limits, may be slow for many URLs
2. **JavaScript Content:** Cannot scrape dynamically loaded content (requires Selenium/Playwright)
3. **Authentication:** Does not handle login-required pages
4. **CAPTCHAs:** Cannot bypass CAPTCHA protection
5. **API Costs:** Claude API usage incurs costs based on tokens processed

### Known Issues
- Some websites block automated requests (403/429 errors)
- Very large pages may exceed API token limits
- Special characters in CSV may require encoding handling

## Error Handling

### Common Errors & Solutions

**1. ModuleNotFoundError: No module named 'anthropic'**
```bash
pip install anthropic
```

**2. API Key Error**
- Check `.env` file exists and contains valid key
- Verify key format: `ANTHROPIC_API_KEY=sk-ant-...`

**3. CSV File Not Found**
- Ensure `urls.csv` exists in the same directory
- Check file encoding (use UTF-8)

**4. Connection Timeout**
- Check internet connection
- Increase timeout value in code
- Some websites may be temporarily down

**5. 403 Forbidden Errors**
- Website blocks automated requests
- Try adding custom User-Agent header
- Respect robots.txt directives

## Best Practices

### 1. Ethical Scraping
- Always check `robots.txt` before scraping
- Respect rate limits and add delays between requests
- Use appropriate User-Agent strings
- Cache responses to avoid repeated requests

### 2. API Usage
- Monitor API usage to control costs
- Implement retry logic with exponential backoff
- Cache AI summaries when possible
- Use appropriate model based on needs

### 3. Data Quality
- Validate URLs before scraping
- Clean and normalize extracted data
- Handle encoding issues properly
- Implement data validation rules

## Troubleshooting

### Debug Mode
Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Test Single URL
```python
# Test with one URL first
test_urls = ['https://www.python.org']
```

### Check API Connection
```python
# Test API separately
from anthropic import Anthropic
client = Anthropic(api_key="your_key")
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.content)
```

## Extending the Project

### Possible Enhancements
1. **Add Database Storage** - Store results in PostgreSQL/MongoDB
2. **Scheduling** - Use cron jobs or Task Scheduler for automated runs
3. **Email Notifications** - Send results via email
4. **Advanced Scraping** - Use Selenium for JavaScript-heavy sites
5. **API Endpoint** - Create REST API to serve data
6. **Authentication** - Handle login-required websites
7. **Multi-threading** - Parallel scraping for faster processing
8. **Data Validation** - Add schema validation for scraped data

## License
MIT License - Feel free to use and modify


## Contributors
[Ananya]

## Acknowledgments
- Anthropic Claude API for AI summaries
- BeautifulSoup for HTML parsing
- React and Tailwind CSS for dashboard UI