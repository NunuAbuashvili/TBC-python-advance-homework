import asyncio
import json
import time

import aiohttp
import aiofiles


class PostFetcher:
    """
    A class to asynchronously fetch posts from an API and save them to a JSON file.

    This class handles the entire process of fetching posts, writing them to a file,
    and verifying the contents of the file.

    Attributes:
        filename (str): The name of the file to save the posts to.
        number_of_posts (int): The number of posts to fetch in total.
        semaphore (asyncio.Semaphore): A semaphore to limit concurrent requests.
        lock (asyncio.Lock): A lock to ensure thread-safe file operations.
    """

    def __init__(self, filename: str, number_of_posts: int, concurrent_requests: int):
        """
        Initializes the PostFetcher with the given parameters.

        :param filename: The name of the file to save the posts to.
        :param number_of_posts: The number of posts to fetch in total.
        :param concurrent_requests: The maximum number of concurrent requests allowed.
        """
        self.filename = filename
        self.number_of_posts = number_of_posts
        self.semaphore = asyncio.Semaphore(concurrent_requests)
        self.lock = asyncio.Lock()

    async def initialize_json_file(self):
        """Initialize the JSON file with an empty list."""
        async with aiofiles.open(self.filename, 'w') as file:
            await file.write(json.dumps([]))

    async def append_post_to_file(self, post: dict):
        """
        Append a post to the JSON file in a thread-safe manner.

        :param post: The post to append to the file.
        """
        async with self.lock:
            async with aiofiles.open(self.filename, 'r+') as file:
                file_contents = await file.read()
                posts = json.loads(file_contents) if file_contents else []
                posts.append(post)
                await file.seek(0)
                await file.write(json.dumps(posts, indent=4))
                await file.truncate()

    async def get_single_post(self, session: aiohttp.ClientSession, post_id: int):
        """
        Fetch a single post from the API and append it to the file.

        :param session: The aiohttp session to use for the request.
        :param post_id: The ID of the post to fetch.
        :return: The fetched post as a dictionary, or None if the fetch failed.
        """
        async with self.semaphore:
            url = f'https://jsonplaceholder.typicode.com/posts/{post_id}'
            async with session.get(url) as response:
                if response.status == 200:
                    post = await response.json()
                    await self.append_post_to_file(post)
                    return post
                else:
                    print(f'Failed to fetch post {post_id}. Status: {response.status}')
                    return None

    async def get_all_posts(self, session: aiohttp.ClientSession):
        """
        Fetch all posts asynchronously.

        :param session: The aiohttp session to use for the request.
        :return: A list of fetched posts, with None for any failed fetches.
        """
        tasks = []
        for post_id in range(1, self.number_of_posts + 1):
            task = asyncio.create_task(self.get_single_post(session, post_id))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def verify_contents_of_file(self):
        """Verify that the number of posts in the file matches the expected number."""
        async with aiofiles.open(self.filename, 'r') as file:
            file_contents = await file.read()
            posts = json.loads(file_contents)
            if len(posts) == self.number_of_posts:
                print('\nVerification successful: The JSON file contains the correct number of items.')
            else:
                print(f'\nVerification failed: Expected {self.number_of_posts} items, but found {len(posts)} items.')
    # noinspection PyTypeChecker
    async def run(self):
        """Run the entire process of fetching posts, saving them, and verifying the results."""
        start = time.time()

        await self.initialize_json_file()

        async with aiohttp.ClientSession() as session:
            results = await self.get_all_posts(session)

        end = time.time()
        execution_time = end - start

        self.process_results(results, execution_time)
        await self.verify_contents_of_file()

    def process_results(self, results: list[dict], execution_time: float):
        """
        Process and print the results of the post fetching operation.

        :param results: The list of fetched posts.
        :param execution_time: The time taken to fetch all posts.
        """
        valid_results = [result for result in results if result is not None]

        print(f'Finished executing in {round(execution_time, 2)} seconds.')
        print(f'Successfully fetched {len(valid_results)} out of {self.number_of_posts} posts.')


async def main():
    """The main function to create and run a PostFetcher instance."""
    filename = 'posts.json'
    number_of_posts = 77
    concurrent_requests = 16

    fetcher = PostFetcher(filename, number_of_posts, concurrent_requests)
    await fetcher.run()


if __name__ == '__main__':
    asyncio.run(main())
