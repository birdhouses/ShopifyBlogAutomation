import os
import requests
import markdown
import json
import time
import base64
from pathlib import Path
import random
from dotenv import load_dotenv

class BlogPostUploader:
    def __init__(self, blog_id, blog_dir, image_dir):
        self.blog_id = blog_id
        self.blog_dir = blog_dir
        self.image_dir = image_dir

        load_dotenv()

        self.password = os.getenv('PASSWORD')
        self.api_key = os.getenv('API_KEY')
        self.shop_name = os.getenv('SHOP_NAME')
        self.store_url = f'https://{self.api_key}:{self.password}@{self.shop_name}.myshopify.com/admin'
        self.articles_endpoint = f'{self.store_url}/api/2024-01/blogs/{self.blog_id}/articles.json'

    def sanitize_title(self, title):
        # Remove leading '#' and strip leading/trailing whitespace
        clean_title = title.lstrip('#').strip()

        # Capitalize the first letter of each word
        capitalized_title = ' '.join(word.capitalize() for word in clean_title.split())

        return capitalized_title

    def convert_md_to_html(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            title = lines[0].strip()  # Extract title from the first line
            content_md = ''.join(lines[1:])  # Join the rest of the lines to form the content
            content_html = markdown.markdown(content_md)
            title = self.sanitize_title(title)
            return title, content_html

    def check_existing_posts(self, title, articles):
        for article in articles:
            if article['title'].strip().lower() == title.strip().lower():
                return True
        return False

    def image_to_base64(self, image_path):
        with open(image_path, 'rb') as image_file:
            # Read the file
            encoded_image = base64.b64encode(image_file.read())
            # Convert bytes to string
            return encoded_image.decode('utf-8')

    def get_image(self):
        image_files = list(Path(self.image_dir).glob('*.*'))

        if not image_files:
            print(f"No images found in {self.image_dir}")
            return None

        random_image_file = image_files[random.randint(0, len(image_files) - 1)]

        # Convert the first image to base64
        return self.image_to_base64(random_image_file)

    def run(self):
        response = requests.get(f'{self.articles_endpoint}?limit=250', headers={'Content-Type': 'application/json'})
        articles = response.json().get('articles', [])

        try:
            for filename in os.listdir(self.blog_dir):
                if filename.endswith('.txt'):
                    time.sleep(5)
                    # Constructing file path
                    file_path = os.path.join(self.blog_dir, filename)

                    # Style the blog post with HTML
                    title, content = self.convert_md_to_html(file_path)
                    image = None

                    if self.image_dir is not None:
                        print('pl')
                        image = self.get_image()

                    # Check if the post already exists
                    if self.check_existing_posts(title, articles):
                        print(f'Blog post already exists: {title}')
                        continue

                    if image is not None:
                        # Data for the new blog post
                        new_post = {
                            "article": {
                                "title": title,
                                "author": "Author",
                                "body_html": content,
                                "image": {
                                    "attachment": image
                                }
                            }
                        }
                    else:
                        # Data for the new blog post
                        new_post = {
                            "article": {
                                "title": title,
                                "author": "Author",
                                "body_html": content
                            }
                        }

                    # POST request to create a new blog post
                    response = requests.post(
                        self.articles_endpoint,
                        headers={'Content-Type': 'application/json'},
                        data=json.dumps(new_post),
                    )

                    # Checking the response
                    if response.status_code == 201:
                        print(f'Successfully created a new blog post: {title}')
                    else:
                        print(f'Failed to create a new blog post: {title}')
                        print(response.content)

                    # Respect the API rate limit
                    time.sleep(1)  # Adjust the sleep time if needed

        except Exception as e:
            ## Retry, probably due to rate limiting
            ## Need to implement better retry mechanism
            print(e)
            self.run()

        print('All blog posts processed.')