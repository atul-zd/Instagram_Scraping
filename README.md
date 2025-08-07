# Instagram Scraper - Setup Guide

Quick setup guide to get your Instagram scraper running.

## Prerequisites

- Python 3.7 or higher
- Internet connection
- Instagram account login (Mandatory) on terminal during scrapt running

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

### 3. Set Up Credentials (Mandatory)

For better scraping access, create a `.env` file:

```bash
python setup_credentials.py
```

Or manually create `.env`:
```bash
echo "INSTAGRAM_USERNAME=your_username" > .env
echo "INSTAGRAM_PASSWORD=your_password" >> .env
```

### 4. Create Output Directory

```bash
mkdir -p generated_files
```

### 5. Run the Scraper

```bash
python instagram_scrap.py
```

## Configuration

### Change Target Accounts

Edit `instagram_scrap.py` line ~150:
```python
target_usernames = ["nasa", "spacex", "esa"]  # Add your target accounts
```

### Adjust Scraping Settings

Edit `instagram_scrap.py` lines ~151-152:
```python
max_posts = 5              # Posts per account 
delay_between_posts = 5    # Seconds between requests
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

That's it! Your scraper is ready to use.