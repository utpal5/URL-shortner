# URL Shortener Service

## Overview
This repository contains a complete implementation of a URL shortening service similar to bit.ly or tinyurl. The service provides endpoints to shorten URLs, redirect short codes to original URLs, and retrieve analytics on usage.

## Setup and Running

### Prerequisites
- Python 3.8+ installed

### Installation and Running
```bash
# Clone or download this repository
# Navigate to the assignment directory
cd url-shortener

# (Optional) Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
```

### Running Tests
```bash
# Run tests with pytest
pytest
```

## API Endpoints

### 1. Shorten URL Endpoint
- **POST** `/api/shorten`
- Request body: JSON with key `"url"` containing the long URL to shorten.
- Response: JSON with `"short_code"` and `"short_url"`.

Example:
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/very/long/url"}'
```

### 2. Redirect Endpoint
- **GET** `/<short_code>`
- Redirects to the original URL associated with the short code.
- Returns 404 if the short code does not exist.
- Tracks each redirect by incrementing click count.

Example:
```bash
curl -L http://localhost:5000/abc123
```

### 3. Analytics Endpoint
- **GET** `/api/stats/<short_code>`
- Returns JSON with:
  - `"url"`: original URL
  - `"clicks"`: number of redirects
  - `"created_at"`: timestamp of creation in ISO format

Example:
```bash
curl http://localhost:5000/api/stats/abc123
```

## Implementation Details

- URLs are validated before shortening.
- Short codes are 6-character alphanumeric strings.
- Thread-safe in-memory storage is used for URL mappings and click counts.
- Basic error handling is included for invalid input and missing short codes.
- Concurrency is handled using threading locks.
- Comprehensive tests cover core functionality, error cases, concurrency, and edge cases.


