# 📸 Instagram User Profile Scraper

This project contains two Python scripts that automate the extraction of Instagram user profiles using Selenium, BeautifulSoup, and Instaloader. These scripts help collect public user information (username, follower count, etc.) based on:

1. **Name and Location Keywords**
2. **Instagram Location Tags**

> ⚠️ This project is for educational and research purposes only. Be mindful of Instagram's Terms of Use.

---

## 🚀 Features

- Automated login via Selenium and Instaloader
- Search posts by name and location keyword or by location tag
- Extract user profiles and details:  
  - Username  
  - Followers  
  - Following  
  - Bio  
  - Verified Status  
  - Privacy and Business Account Status  
- Save all data to CSV

---

## 🧠 Scripts Overview

### 1. `instagram_perth_user_profile_scapper.py`

Searches for posts using a **name + location keyword** (e.g., `"ben perth"`), extracts user profiles, and saves usernames.

### 2. `instagram_bot_public_profile_location_based_extractor.py.py`

Searches for posts from a specific **Instagram location tag** (e.g., `"perth australia"`), scrapes detailed profile data using Instaloader.

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/instagram-user-scraper.git
cd instagram-user-scraper
