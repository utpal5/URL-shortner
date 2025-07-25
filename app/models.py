import threading
import time

class URLStore:
    def __init__(self):
        self.lock = threading.Lock()
        self.url_map = {}  # short_code -> original_url
        self.clicks = {}   # short_code -> click count
        self.created_at = {}  # short_code -> creation timestamp

    def add_url(self, short_code, original_url):
        with self.lock:
            self.url_map[short_code] = original_url
            self.clicks[short_code] = 0
            self.created_at[short_code] = time.time()

    def get_url(self, short_code):
        with self.lock:
            return self.url_map.get(short_code)

    def increment_clicks(self, short_code):
        with self.lock:
            if short_code in self.clicks:
                self.clicks[short_code] += 1

    def get_clicks(self, short_code):
        with self.lock:
            return self.clicks.get(short_code, 0)

    def get_created_at(self, short_code):
        with self.lock:
            return self.created_at.get(short_code)
