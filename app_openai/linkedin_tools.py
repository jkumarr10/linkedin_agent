import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import logging

load_dotenv()


class Linkedin:
    
    def __init__(self, user: str = "jitthen"):
        
        if user.lower() == "jitthen".lower():
            # Get Linkedin Access Token from .env file
            access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
            linkedin_author = os.getenv("LINKEDIN_AUTHOR")
            
            self.access_token = access_token
            self.linkedin_author = linkedin_author
        
        else:
            logging.info(f"Enter User's Name")


    def get_user_info(self):
        
        
        # Linkedin API for getting USER INFO
        user_info_url = "https://api.linkedin.com/v2/userinfo"
        
        # Headers with authorization
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        response = requests.get(url = user_info_url, headers=headers)
        
        if response.status_code == 200:
            # Parse and return json response
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }

    def post_to_linkedin(self, generated_content: str):
        
        
        # Linkedin API to share content
        share_content_url = "https://api.linkedin.com/v2/ugcPosts"
        
        # Headers with authorization
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        post_data = {
        "author": f"urn:li:person:{self.linkedin_author}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": generated_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "CONNECTIONS"
            }
        }
        
        print(f"Attempting to post to LinkedIn with access token: {self.access_token[:5]}...")
        print(f"LinkedIn author ID: {self.linkedin_author}")
        print(f"Content to post: {generated_content[:50]}...")
        
        response = requests.post(url=share_content_url, headers=headers, json=post_data)

        print(f"LinkedIn API response status code: {response.status_code}")
        print(f"LinkedIn API response: {response.text}")
        
        if response.status_code in [200,201]:
            # Parse and return json response
            return response.json()
        else:
            return {
                "error": response.status_code,
                "message": response.text
            }
            

# Test Script
if __name__ == "__main__":
    # Add a timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    module = Linkedin()
    user_info = module.get_user_info()
    print(user_info)