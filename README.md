# ShopifyBlogAutomation
Create Shopify Blog posts in Bulk with Python!

## Setup
- Run pip install requirements.txt
- Copy `env.example` and rename to `.env`
  - Fill in your details
    - To find your Shopify store name for API interaction, go to Admin > Apps > Manage private apps. Your store name is in the Example URL. More details in Private apps.
  - You need to enable custom app development for your Shopify Store
    - https://help.shopify.com/en/manual/apps/app-types/custom-apps

## Usage
- Run `python3 run.py --blog_id your_blog_id --blog_dir your_blog_dir`
  - To find your blog ID, navigate to Online Store > Blog Posts. Click on the blog name. The number at the end of the URL in your browser's address bar is the blog ID.
  - The blog dir should be a folder with .txt files for the blog posts.The title of the blog post is determined by the first line of the .txt file, prefixed with a singular #

# Important
You can specify an `images_dir` when running the script. Every time a blog post is created, it will pick a random image from the directory.
