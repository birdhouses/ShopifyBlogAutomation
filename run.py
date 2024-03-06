import argparse
from src.uploader import BlogPostUploader

def main():
    parser = argparse.ArgumentParser(description='Upload blog posts from a directory (.txt files).')
    parser.add_argument('--blog_id', type=str, required=True, help='ID of the Shopify blog to upload to.')
    parser.add_argument('--blog_dir', type=str, required=True, help='Directory to containing blog posts')
    parser.add_argument('--image_dir', type=str, required=False, help='Directory to containing the images for the blog posts')

    args = parser.parse_args()

    uploader = BlogPostUploader(args.blog_id, args.blog_dir, args.image_dir)
    uploader.run()

if __name__ == '__main__':
    main()