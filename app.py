from flask import Flask, request, redirect, render_template_string
from pathlib import Path
import json
import random
import string
from urllib.parse import urlparse

app = Flask(__name__)

DATA_FILE = Path(__file__).parent / "urls.json"


def load_data():
    if not DATA_FILE.exists():
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def valid_url(url):
    try:
        parsed = urlparse(url)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.netloc)
            and "." in parsed.netloc
        )
    except Exception:
        return False


def generate_code(data):
    while True:
        code = "".join(
            random.choices(string.ascii_letters + string.digits, k=6)
        )

        if code not in data:
            return code


HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>url shortener</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 700px;
            margin: 60px auto;
            padding: 20px;
        }

        h1 {
            text-align: center;
        }

        form {
            margin: 30px 0;
        }

        input {
            width: 70%;
            padding: 12px;
            font-size: 16px;
        }

        button {
            padding: 12px 18px;
            font-size: 16px;
            cursor: pointer;
        }

        .result {
            padding: 15px;
            background: #f1f1f1;
            margin-top: 20px;
        }

        .error {
            color: red;
        }
    </style>
</head>

<body>

<h1>url shortener</h1>

<form method="POST">
    <input
        type="text"
        name="url"
        placeholder="enter your long url"
        required
    >

    <button type="submit">shorten</button>
</form>

{% if short_url %}
<div class="result">
    <strong>your shortened url:</strong>
    <br><br>
    <a href="{{ short_url }}" target="_blank">
        {{ short_url }}
    </a>
</div>
{% endif %}

{% if error %}
<p class="error">{{ error }}</p>
{% endif %}

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    short_url = None
    error = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not valid_url(url):
            error = "please enter a valid url."
        else:
            data = load_data()

            existing_code = None

            for code, info in data.items():
                if info.get("url") == url:
                    existing_code = code
                    break

            if existing_code:
                code = existing_code
            else:
                code = generate_code(data)

                data[code] = {
                    "url": url,
                    "clicks": 0
                }

                save_data(data)

            short_url = request.host_url.rstrip("/") + "/" + code

    return render_template_string(
        HTML,
        short_url=short_url,
        error=error
    )


@app.route("/<code>")
def redirect_url(code):
    data = load_data()

    if code not in data:
        return "short url not found", 404

    data[code]["clicks"] = data[code].get("clicks", 0) + 1
    save_data(data)

    return redirect(data[code]["url"])


if __name__ == "__main__":
    app.run(debug=True)