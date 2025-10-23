# automated-vulnerable-site-scanner-from-google-search
It is a Python script designed to automatically discover potentially vulnerable WordPress websites using Google Dorks through the Google Custom Search JSON API. The script collects unique URLs matching specific WordPress vulnerability patterns, normalizes them, filters for relevant domains, and stores them in a database via API calls.
🎯 Key Features:
Google Dork Integration: Uses 13 pre-defined WordPress-specific Google Dorks

URL Normalization: Standardizes URLs to https://www format

Domain Filtering: Focuses on .com domains while excluding development/community sites

Duplicate Prevention: Maintains unique URL collection using sets

Database Integration: Automatically inserts valid URLs via REST API

Results Export: Saves collected sites to vulnerable_sites.txt

Rate Limiting: Implements delays to respect API limits

🔍 Vulnerable WordPress Site Searcher
📖 Overview
This Python script automates the discovery of potentially vulnerable WordPress sites using Google's Custom Search API with specialized search queries (Google Dorks). It's designed for security researchers and penetration testers to identify WordPress installations with common security misconfigurations.

🛠️ Prerequisites
Python 3.6+

Required Python packages:

bash
pip install requests
⚙️ Configuration
API Setup
Google Custom Search API:

Obtain API key from Google Cloud Console

Create Custom Search Engine at Google CSE

Update the following variables in the script:

python
API_KEY = "your_google_api_key_here"
CSE_ID = "your_custom_search_engine_id"
Database API:

Ensure your database endpoint is accessible

Update the API key in the insert_into_db() function:

python
"api_key": "your_database_api_key_here"
🚀 Usage
Run the script:

bash
python vulnerableSiteSearcher.py
Enter target count when prompted:

text
Enter the number of URLs you want to collect: 100
Monitor progress - the script will:

Display search progress for each dork

Show insertion status for each URL

Save results to vulnerable_sites.txt

🔧 Function Details
Core Functions
search_google(query, start_index): Fetches search results from Google API

normalize_url(url): Standardizes URL format and enforces HTTPS

is_valid_domain(url): Filters for relevant .com domains

insert_into_db(urls): Sends valid URLs to database via API

main(): Orchestrates the entire collection process

Google Dorks Used
The script searches for 13 WordPress-specific patterns including:

Login pages (wp-login.php, wp-admin)

Configuration files (wp-config.php)

Backup files (SQL, ZIP, GZ)

Debug logs and error files

Specific vulnerable components (timthumb.php, revslider.php)

📊 Output
Console: Real-time progress and status updates

Database: URLs inserted via API calls

File: vulnerable_sites.txt with all collected URLs

⚠️ Important Notes
Legal Use Only: Ensure you have permission to scan target sites

API Limits: Google Custom Search API has daily quotas

Rate Limiting: Built-in delays prevent API throttling

Ethical Considerations: Use responsibly for authorized security testing only

🐛 Troubleshooting
Common Issues
API Errors: Check Google API key and CSE ID configuration

Database Connection: Verify endpoint URL and API key

No Results: Some dorks may return limited results

Duplicate URLs: Script automatically handles duplicates

Error Messages
Error during API call: Google API connection issue

Failed to insert: Database API failure

Duplicate URL found: URL already processed

📝 License & Ethics
This tool is intended for:

Security research

Authorized penetration testing

Educational purposes

⚠️ Warning: Unauthorized use against websites without permission may be illegal in your jurisdiction. Always obtain proper authorization before conducting security assessments.

🔒 Security Disclaimer
This tool is designed for legitimate security research and authorized testing only. Users are responsible for ensuring they have proper authorization before scanning any websites. The developers are not liable for misuse of this software.

