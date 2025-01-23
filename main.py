import aiohttp
import asyncio
import logging
import json
import os
from typing import List, Dict, Any

# Configure logging
logging.basicConfig(
    filename='request_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# User-Agent strings for different browsers and operating systems
USER_AGENTS = {
    'chrome_windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'firefox_windows': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'safari_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15',
    'chrome_mac': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'chrome_android': 'Mozilla/5.0 (Linux; Android 10; Pixel 3 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36',
    'firefox_android': 'Mozilla/5.0 (Android 10; Mobile; rv:89.0) Gecko/89.0 Firefox/89.0',
}

class RequestSimulator:
    def __init__(self, total_requests: int, user_agent: str):
        self.total_requests = total_requests
        self.user_agent = user_agent
        self.urls = self.load_urls()
        self.results: List[Dict[str, Any]] = []

    def load_urls(self) -> List[str]:
        """Load URLs from list.txt file."""
        try:
            if os.path.exists('list.txt'):
                with open('list.txt', 'r') as file:
                    return [line.strip() for line in file if line.strip()]
            else:
                logging.warning("list.txt not found. No URLs loaded.")
                return []
        except Exception as e:
            logging.error(f"Error loading URLs: {e}")
            return []

    async def send_single_request(self, session: aiohttp.ClientSession, url: str) -> None:
        headers = {'User-Agent': self.user_agent}
        try:
            async with session.get(url, headers=headers) as response:
                status = response.status
                if status == 200:
                    logging.info(f"Success: {status} from {self.user_agent} to {url}")
                    self.results.append({"url": url, "status": status, "success": True})
                else:
                    logging.warning(f"Failed: {status} from {self.user_agent} to {url}")
                    self.results.append({"url": url, "status": status, "success": False})
        except Exception as e:
            logging.error(f"Exception: {e} from {self.user_agent} to {url}")
            self.results.append({"url": url, "status": "error", "success": False})

    async def send_requests_to_url(self, url: str) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [self.send_single_request(session, url) for _ in range(self.total_requests)]
            await asyncio.gather(*tasks)

    async def run(self) -> None:
        """Run the simulator in an infinite loop."""
        try:
            while True:
                self.urls = self.load_urls()  # Reload URLs from the file
                for url in self.urls:
                    await self.send_requests_to_url(url)
                self.save_results()
                await asyncio.sleep(1)  # Optional: sleep for a second between URL batches
        except asyncio.CancelledError:
            logging.info("Request simulator stopped gracefully.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            self.save_results()

    def save_results(self) -> None:
        """Save results to login.json file."""
        try:
            with open('login.json', 'w') as json_file:
                json.dump(self.results, json_file, indent=4)
            logging.info("Results saved to login.json")
        except Exception as e:
            logging.error(f"Error saving results: {e}")

async def shutdown(signal, loop, simulator: RequestSimulator):
    """Graceful shutdown."""
    logging.info(f"Received exit signal {signal.name}...")
    tasks = [task for task in asyncio.all_tasks() if task is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def main():
    # Configuration
    total_requests = int(os.getenv('TOTAL_REQUESTS', 100))  # Number of simultaneous requests
    user_agent = os.getenv('USER_AGENT', USER_AGENTS['chrome_windows'])  # Default user agent

    simulator = RequestSimulator(total_requests, user_agent)
    loop = asyncio.get_event_loop()

    # Handle graceful shutdown
    signals = (asyncio.tasks.Task.all_tasks(), asyncio.tasks.Task.all_tasks())
    for s in signals:
        loop.add_signal_handler(
            s, lambda s=s: asyncio.create_task(shutdown(s, loop, simulator))
        )

    try:
        loop.run_until_complete(simulator.run())
    finally:
        loop.close()

if __name__ == "__main__":
    main()
