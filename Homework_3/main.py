import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests


class PostFetcher:
    """Handles fetching posts from an API and writing them to a JSON file."""

    def __init__(self, base_url: str, number_of_posts: int, filename: str):
        """
        Initializes the PostFetcher instance.

        :param base_url: The base URL of the API.
        :param number_of_posts: The total number of posts to fetch.
        :param filename: The path to the JSON file where posts will be saved.
        """
        self.base_url = base_url
        self.number_of_posts = number_of_posts
        self.filename = filename
        self.lock = threading.Lock()

    def get_single_post(self, post_id: int):
        """
        Fetches a single post from the API.

        :param post_id: The ID of the post to fetch.
        :return: The post data if the request is successful, otherwise None.
        """
        url = f'{self.base_url}{post_id}'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Error: Received status code {response.status_code} for post {post_id}.')
        except requests.RequestException as error:
            print(f'Error fetching post {post_id}: {error}')
            return None

    def write_post_to_file(self, post):
        """
        Writes a post to the JSON file in a thread-safe manner.
        :param post: The post data to write to the file.
        """
        with self.lock:
            # Open the file in append mode and add the post to the existing list
            with open(self.filename, 'r+') as file:
                data = json.load(file)
                data.append(post)
                # Move the file pointer to the beginning and overwrite the updated list
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

    def get_and_write(self, post_id: int):
        """
        Fetches a post and writes it to the file.
        :param post_id: The ID of the post to fetch and write.
        """
        post = self.get_single_post(post_id)
        if post:
            self.write_post_to_file(post)


class FileManager:
    """Handles initialization and verification of the JSON file."""

    def __init__(self, filename: str, number_of_posts: int):
        """
        Initializes the FileManager instance.

        :param filename: The path to the JSON file.
        :param number_of_posts: The total number of posts expected in the file.
        """
        self.filename = filename
        self.number_of_posts = number_of_posts

    def initialize_file(self):
        """Initializes the JSON file to an empty list."""
        with open(self.filename, 'w') as file:
            json.dump([], file)

    def verify_file_content(self):
        """Verifies the number of items in the JSON file."""
        with open(self.filename, 'r') as file:
            data = json.load(file)
            if len(data) == self.number_of_posts:
                print('\nVerification successful: The JSON file contains the correct number of items.')
            else:
                print(f'\nVerification failed: Expected {self.number_of_posts} items, but found {len(data)} items.')


def main():
    """Main function to initialize a JSON file, and fetch and write posts to it. """
    filename = 'posts.json'
    base_url = 'https://jsonplaceholder.typicode.com/posts/'
    number_of_posts = 77

    file_manager = FileManager(filename, number_of_posts)
    fetcher = PostFetcher(base_url, number_of_posts, filename)
    file_manager.initialize_file()

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=11) as executor:
        futures = [executor.submit(fetcher.get_and_write, post_id) for post_id in range(1, number_of_posts + 1)]
        for future in as_completed(futures):
            future.result()

    end_time = time.time()
    print(f'Finished in {round(end_time - start_time, 2)} second(s).')

    file_manager.verify_file_content()


if __name__ == '__main__':
    main()
