import instaloader
import time
import pandas as pd
import os
from datetime import datetime
import logging
from dotenv import load_dotenv

# Adjust column width and wrap text using openpyxl
import openpyxl
from openpyxl.styles import Alignment


load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Instaloader
L = instaloader.Instaloader(
    download_comments=False, download_video_thumbnails=False, download_geotags=False
)


def login_to_instagram(username=None, password=None):
    username = username or os.getenv("INSTAGRAM_USERNAME")

    try:
        L.load_session_from_file(username)
        logger.info("Loaded session file")
        return True
    except Exception as e:
        logger.warning(f"Session load failed: {e}")
        password = password or os.getenv("INSTAGRAM_PASSWORD")
        if username and password:
            try:
                L.login(username, password)
                L.save_session_to_file()
                logger.info("Logged in and session saved")
                return True
            except Exception as e:
                logger.error(f"Failed to login: {e}")
                return False
        else:
            logger.warning("No credentials. Running in anonymous mode.")
            return False


def scrape_account_data(username, max_posts=100, delay_between_posts=3):
    """Scrape Instagram account data with improved error handling and rate limiting"""
    try:
        profile = instaloader.Profile.from_username(L.context, username)
        logger.info(f"Successfully fetched profile for {username}")
    except Exception as e:
        logger.error(f"Failed to fetch profile for {username}: {e}")
        return None, []

    # Account information
    data = {
        "Instagram ID": profile.userid,
        "Username": profile.username,
        "Full Name": profile.full_name,
        "Followers": profile.followers,
        "Following": profile.followees,
        "Posts Count": profile.mediacount,
        "Bio": profile.biography,
        "External URL": profile.external_url,
        "Private": profile.is_private,
        "Verified": profile.is_verified,
    }

    logger.info(f"Fetching posts for {username} (max: {max_posts})...")

    posts_data = []
    count = 0

    try:
        for post in profile.get_posts():
            if count >= max_posts:
                break

            try:
                # Safely get location data
                location_name = ""
                try:
                    if post.location:
                        location_name = post.location.name
                except Exception as e:
                    logger.debug(
                        f"Could not fetch location for post {post.shortcode}: {e}"
                    )
                    location_name = ""

                # Extract hashtags safely
                hashtags = []
                if post.caption:
                    try:
                        hashtags = [
                            tag for tag in post.caption.split() if tag.startswith("#")
                        ]
                    except Exception as e:
                        logger.debug(
                            f"Could not extract hashtags for post {post.shortcode}: {e}"
                        )

                post_info = {
                    "Instagram username": profile.username,
                    "Post URL": f"https://www.instagram.com/p/{post.shortcode}/",
                    "Caption": post.caption or "",
                    "Likes": post.likes,
                    "Comments Count": post.comments,
                    "Date": post.date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                    "Is Video": post.is_video,
                    "Location": location_name,
                    "Hashtags": hashtags,
                }

                posts_data.append(post_info)
                count += 1

                if count % 10 == 0:
                    logger.info(f"Processed {count} posts...")

                time.sleep(delay_between_posts)  # Rate limiting

            except Exception as e:
                logger.error(f"Unexpected error: {e}")

    except Exception as e:
        logger.error(f"Error fetching posts: {e}")

    logger.info(f"Successfully processed {len(posts_data)} posts")
    return data, posts_data


def export_to_excel(all_accounts_data, all_posts_data_by_user, filename=None):
    """Export data like the second script: one Profile Info sheet + one Posts sheet per user."""

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_files/instagram_report_{timestamp}.xlsx"

    try:
        # Debug log: show how many posts per user
        logger.info(f"Posts data collected: { {u: len(p) for u, p in all_posts_data_by_user.items()} }")

        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            # Combine all account info into one sheet
            account_df = pd.DataFrame(all_accounts_data)
            account_df.to_excel(writer, sheet_name="Profile Info", index=False)

            # Always create a posts sheet for each user
            for account in all_accounts_data:
                username = account["Username"]
                sheet_name = f"{username}_Posts"[:31]  # Excel limit is 31 chars
                posts_data = all_posts_data_by_user.get(username, [])
                posts_df = pd.DataFrame(posts_data)
                posts_df.to_excel(writer, sheet_name=sheet_name, index=False)

        # Format column width and wrap text
        wb = openpyxl.load_workbook(filename)
        for ws in wb.worksheets:
            for col in ws.columns:
                col_letter = col[0].column_letter
                ws.column_dimensions[col_letter].width = 50
                for cell in col:
                    cell.alignment = Alignment(wrap_text=True)
        wb.save(filename)

        logger.info(f"Successfully exported data to {filename}")
        return filename

    except Exception as e:
        logger.error(f"Failed to export data: {e}")
        return None




def main():
    """Main function to run the scraper for multiple users"""

    # Login
    login_success = login_to_instagram()

    # Get environment variables
    target_usernames_raw = os.getenv("TARGET_USERNAMES")
    if not target_usernames_raw:
        logger.error("TARGET_USERNAMES is not set in .env")
        return

    target_usernames = [u.strip() for u in target_usernames_raw.split(",")]

    try:
        max_posts = int(os.getenv("MAX_POSTS", "10"))
        delay_between_posts = int(os.getenv("DELAY_BETWEEN_POSTS", "3"))
    except ValueError:
        logger.error("MAX_POSTS and DELAY_BETWEEN_POSTS must be integers")
        return

    all_accounts_data = []
    all_posts_data_by_user = {}

    for username in target_usernames:
        logger.info(f"Starting scrape for {username}")
        account_data, posts_data = scrape_account_data(
            username, max_posts=max_posts, delay_between_posts=delay_between_posts
        )

        if account_data:
            all_accounts_data.append(account_data)
            all_posts_data_by_user[username] = posts_data
        else:
            logger.warning(f"Skipping {username} due to scrape failure")

    if all_accounts_data:
        filename = export_to_excel(all_accounts_data, all_posts_data_by_user)
        if filename:
            logger.info(f"Scraping completed. Data saved to {filename}")
        else:
            logger.error("Failed to export data")
    else:
        logger.error("No data collected to export")


if __name__ == "__main__":
    main()
