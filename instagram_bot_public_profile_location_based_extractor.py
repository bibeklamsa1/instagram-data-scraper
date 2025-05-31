from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from cred import username, password  # Assuming you have a credentials.py file with your login details
import requests as req
from bs4 import BeautifulSoup
import instaloader

#block the images and css files from loading
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
prefs = {
    "profile.managed_default_content_settings.images": 2,       # Block images
    "profile.managed_default_content_settings.stylesheets": 2,  # Block CSS
    "profile.managed_default_content_settings.fonts": 2,        # Block fonts
    "profile.managed_default_content_settings.plugins": 2       # Block Flash/plugins
}

# Set the preferences in Chrome options
chrome_options.add_experimental_option("prefs", prefs)



driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(5)

# Check if login was successful
#Let's login with instaloader to get all the information once the link extracted for each user post
#login to instaloader   
#check if instaloader session is already created
L = instaloader.Instaloader()
# If not, create a new session
if not L.context.is_logged_in:
    print("🔑 Logging in with instaloader...")
    try:
        L.login(username, password)  # Login to Instagram using instaloader
        L.save_session_to_file("instaloader_session") # Save the session to a file
        print("✅ Logged in with instaloader")
    except Exception as e:
        print("❌ Login failed. Please check your credentials.")
        #if login fails, exit the script
        driver.quit()
        exit()

else:
    print("🔑 Already logged in with instaloader")
    L.load_session_from_file("instaloader_session")  # Load the session from the file
    print("✅ Loaded instaloader session from file")
time.sleep(5)


# Input credentials
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys(username)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)

# Wait for login to complete
time.sleep(10)
print("✅ Logged in to Instagram via Selenium")



# now visit this page
data = driver.get("https://www.instagram.com/explore/search/keyword/?q=perth%20australia")

# Wait for the page to load
time.sleep(10)

#load more posts
# Scroll down multiple times
scroll_pause_time = 5  # Adjust based on your internet speed

for i in range(1):  # Scroll 10 times
    print(f"Scrolling {i + 1}/10...")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)



#now let's create a function that extracts 
#collect the username,folowers,following from the posts
users_info = []
# Collect post links (example)
posts = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
post_links = [post.get_attribute('href') for post in posts]
print(f"Found {len(post_links)} post links")
for link in post_links:
    driver.get(link)
      # Wait for the page to load
    time.sleep(0.5)
    bs = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Find the username link
    username_element = bs.find('a', href=lambda href: href and '/p/' not in href)
    
    if username_element:
        username = username_element.text.strip()
        profile_link = "https://www.instagram.com" + username_element['href']
        
        # Use instaloader to get user info
        try:
            profile = instaloader.Profile.from_username(L.context, username)
            followers = profile.followers
            following = profile.followees
            bio_graphy = profile.biography
            is_verified = profile.is_verified
            is_private = profile.is_private
            is_business_account = profile.is_business_account
            #check if user already exists in the list
            if any(user['username'] == username for user in users_info):
                print(f"User {username} already exists in the list. Skipping.")
                continue
            
            users_info.append({
                'UserName': username,
                'Followers': followers,
                'Following': following,
                'Profile Link': profile_link,
                'Bio': bio_graphy,
                'Is Verified': is_verified,
                'Is Private': is_private,
                'Is Business Account': is_business_account,
            })
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {username} does not exist.")
        except Exception as e:
            print(f"Error collecting info for {username}: {e}")
    else:
        print("No username link found.")
    
#now print offically the users info
print("\nCollected User Information:")
for user in users_info:
    print(f"UserName: {user['UserName']}, Followers: {user['Followers']}, Following: {user['Following']}, Profile Link: {user['Profile Link']} , Bio: {user['Bio']}, Verified: {user['Is Verified']}, Private: {user['Is Private']}, Business Account: {user['Is Business Account']}")
#write it in a csv file
import pandas as pd
df = pd.DataFrame(users_info)
df.to_csv('instagram_users_info.csv', index=False)
print("✅ User information saved to instagram_users_info.csv")
# Close the driver
driver.quit()