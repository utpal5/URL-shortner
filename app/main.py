from flask import Flask, jsonify, request, redirect, abort
from app.models import URLStore
from app.utils import generate_short_code, is_valid_url
import time

app = Flask(__name__)

url_store = URLStore()

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Generate unique short code
    for _ in range(5):  # try 5 times to avoid collision
        short_code = generate_short_code()
        if url_store.get_url(short_code) is None:
            break
    else:
        return jsonify({"error": "Could not generate unique short code"}), 500

    url_store.add_url(short_code, original_url)

    short_url = request.host_url + short_code
    return jsonify({"short_code": short_code, "short_url": short_url})

@app.route('/<short_code>')
def redirect_short_url(short_code):
    original_url = url_store.get_url(short_code)
    if original_url is None:
        abort(404, description="Short code not found")

    url_store.increment_clicks(short_code)
    return redirect(original_url)

@app.route('/api/stats/<short_code>')
def get_stats(short_code):
    original_url = url_store.get_url(short_code)
    if original_url is None:
        abort(404, description="Short code not found")

    clicks = url_store.get_clicks(short_code)
    created_at_timestamp = url_store.get_created_at(short_code)
    created_at_iso = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(created_at_timestamp)) if created_at_timestamp else None

    return jsonify({
        "url": original_url,
        "clicks": clicks,
        "created_at": created_at_iso
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
