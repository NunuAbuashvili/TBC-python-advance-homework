import json
import threading
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = 'https://jsonplaceholder.typicode.com/posts/'
NUMBER_OF_POSTS = 77
lock = threading.Lock()

def fetch_and_write_to_file(post_id: int, filename: str):
    """Fetches a post from the API and writes it to the JSON file in a thread-safe manner."""
    url = f'{BASE_URL}{post_id}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            post = response.json()
            with lock:
                # Open the file in append mode and add the post to the existing list
                with open(filename, 'r+') as file:
                    data = json.load(file)
                    data.append(post)
                    # Move the file pointer to the beginning and overwrite the updated list
                    file.seek(0)
                    json.dump(data, file, indent=4)
                    file.truncate()
            print(f'Fetched and wrote post {post_id}')
        else:
            print(f'Error: Received status code {response.status_code} for post {post_id}')
    except requests.RequestException as error:
        print(f'Error fetching post {post_id}: {error}')

def initialize_file(filename: str):
    """Initializes the JSON file to an empty list."""
    with open(filename, 'w') as file:
        json.dump([], file)

def verify_file(filename: str):
    """Verifies the number of items in the JSON file."""
    with open(filename, 'r') as file:
        data = json.load(file)
        print(f'Number of items in the JSON file: {len(data)}')
        if len(data) == NUMBER_OF_POSTS:
            print('Verification successful: The JSON file contains the correct number of items.')
        else:
            print(f'Verification failed: Expected {77} items, but found {len(data)} items.')

def main():
    filename = 'posts.json'
    start_time = time.time()

    # Initialize the JSON file
    initialize_file(filename)

    # Use ThreadPoolExecutor to fetch and write posts concurrently
    with ThreadPoolExecutor(max_workers=11) as executor:
        futures = [executor.submit(fetch_and_write_to_file, post_id, filename) for post_id in range(1, 78)]
        for future in as_completed(futures):
            future.result()

    end_time = time.time()
    print(f'Finished in {round(end_time - start_time, 2)} second(s)')

    # Verify the contents of the JSON file
    verify_file(filename)

if __name__ == '__main__':
    main()
