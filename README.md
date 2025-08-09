# Instagram Scraper - Setup Guide

Quick setup guide to get your Instagram scraper running.

## Prerequisites

- Python 3.7 or higher
- Internet connection
- Instagram account login (Mandatory) on terminal during script running

## Step-by-Step Setup

### 1. Create Virtual Environment

```bash
python3 -m venv myenv
source myenv/bin/activate  # Linux/Mac
# OR
myenv\Scripts\activate     # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Credentials and Settings (Mandatory)

We provide a `.env_example` file.  
Simply copy it to `.env` and edit the values.

```bash
cp .env_example .env
```

Open `.env` in a text editor and set:

```env
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
TARGET_USERNAMES=nasa,spacex,adidas
MAX_POSTS=5
DELAY_BETWEEN_POSTS=5
```

Variable details:

- **`INSTAGRAM_USERNAME`** → Your Instagram login username.
- **`INSTAGRAM_PASSWORD`** → Your Instagram login password. 
- **`TARGET_USERNAMES`** → Comma-separated string of Instagram accounts to scrape. (converted to list in code).
- **`MAX_POSTS`** → Number of posts to fetch per account. 
- **`DELAY_BETWEEN_POSTS`** → Delay in seconds between requests.  

> **Note:** You do not need to edit `instagram_scrap.py`.  
> All settings are read from `.env`.

### 4. Create Output Directory

```bash
mkdir -p generated_files
```

### 5. Run the Scraper

```bash
python instagram_scrap.py
```

## Quick Test

Run with default settings:
```bash
python instagram_scrap.py
```

Check `generated_files/` for the Excel report.

## Troubleshooting

- **Login issues**: Check credentials in `.env` file
- **Rate limiting**: Increase `delay_between_posts` to 10+ seconds
- **No data**: Ensure target accounts are public
- **Permission errors**: Check file permissions for output directory

## Files Created

- `.env` - Your credentials (don't commit this)
- `generated_files/instagram_report_*.xlsx` - Scraped data

### Function Reference — Arguments & Return Types

This section describes the key functions used in `instagram_scrap.py` along with their arguments and return types to help reviewers understand the code structure and flow.

1. **`login_to_instagram(username=None, password=None)`**

**Description:**  
Logs in to Instagram using a saved session or provided credentials (from environment variables or parameters).

**Arguments:**  
- `username` (str or None) → Instagram username (optional).  
  Defaults to environment variable `INSTAGRAM_USERNAME`.  
- `password` (str or None) → Instagram password (optional).  
  Defaults to environment variable `INSTAGRAM_PASSWORD`.

**Returns:**  
- bool → True if login/session load is successful; otherwise False.

---

2. **`scrape_account_data(username, max_posts=100, delay_between_posts=3)`**

**Description:**  
Fetches profile data and posts for a specified Instagram user, with rate limiting and error handling.

**Arguments:**  
- `username` (str) → Instagram username to scrape.  
- `max_posts` (int, optional) → Maximum posts to scrape (default is 100).  
- `delay_between_posts` (int, optional) → Delay in seconds between processing posts (default is 3).

**Returns:**  
- tuple → `(account_info, posts_list)`  
  - `account_info` (dict) → User profile details (ID, username, followers, bio, etc.)  
  - `posts_list` (list) → List of dictionaries representing individual posts with URL, caption, likes, comments, date, location, hashtags.  
- Returns `(None, [])` if scraping fails.

---

3. **`export_to_excel(all_accounts_data, all_posts_data_by_user, filename=None)`**

**Description:**  
Exports all collected profile and posts data into an Excel workbook. Creates one sheet for profile info and separate sheets for each user’s posts. Applies formatting for readability.

**Arguments:**  
- `all_accounts_data` (list) → List of account info dictionaries.  
- `all_posts_data_by_user` (dict) → Mapping of username to list of post dictionaries.  
- `filename` (str or None) → Optional output filename. If None, creates a timestamped file in `generated_files`.

**Returns:**  
- str → Filepath of saved Excel file on success.  
- None → On failure.

---

4. **`main()`**

**Description:**  
Entry point for the scraper script. Logs in, reads target usernames and settings from environment variables, scrapes data for each user, and exports to Excel.

**Arguments:**  
None

**Returns:**  
None


## Conclusion
That's it! Your scraper is ready to use.