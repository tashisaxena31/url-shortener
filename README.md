# Mini URL Shortener

A simple command-line URL Shortener made using **Python** in **Visual Studio Code**.

It converts a long URL into a short code. The short code can later be used to find the original URL.

## Features

### Required Features

* Shorten a URL
* Generate a short code
* Find the original URL using the code
* Store URLs permanently
* Show all saved URLs
* Check if a URL is valid
* Handle invalid or missing codes
* No external APIs used

### Extra Features

* Custom aliases
* Click counter
* Open the URL in a browser
* Delete a saved URL
* Interactive menu
* Creation date and time

---

## Requirements

You need:

* Latest version of **Python**
* **Visual Studio Code**

No extra Python packages are required.

---

## Project Files

```text
Mini-URL-Shortener/
│
├── main.py
├── README.md
├── .gitignore
└── urls.json
```

**Note:** `urls.json` is created automatically by the program when you save your first URL.

---

# How to Run

1. Open the project folder in **Visual Studio Code**.
2. Open **Terminal → New Terminal**.
3. Type:

```bash
python main.py
```

4. Press **Enter**.

The program will start.

---

# Main Commands

## 1. Shorten a URL

```bash
python main.py shorten https://www.google.com
```

Example:

```text
URL shortened successfully!
Original URL: https://www.google.com
Short code:   aB72xK
Short URL:    aB72xK
```

The short code will be different each time.

---

## 2. Find the Original URL

Use the short code:

```bash
python main.py resolve aB72xK
```

Example:

```text
Original URL: https://www.google.com
Resolution count: 1
```

The resolution count increases every time the code is used.

---

## 3. Open the URL

You can also open the original URL in your browser:

```bash
python main.py resolve aB72xK --open
```

---

## 4. Show All URLs

```bash
python main.py list
```

Example:

```text
================================================================================
                        STORED URLS
================================================================================

[1]
Short code : aB72xK
Original   : https://www.google.com
Created    : 2026-10-01T20:15:32
Clicks     : 2

===============================================================================
Total URLs: 1
=============================================================================
```

---

## 5. Create Your Own Short Code

You can choose your own alias.

Example:

```bash
python main.py shorten https://www.wikipedia.org --alias wiki
```

Output:

```text
URL shortened successfully!
Original URL: https://www.wikipedia.org
Short code:   wiki
Short URL:    wiki
```

You can use:

* Letters
* Numbers
* `-`
* `_`

---

## 6. Delete a URL

To delete a saved URL:

```bash
python main.py delete wiki
```

Example:

```text
URL deleted successfully.
Short code: wiki
Original URL: https://www.wikipedia.org
```

---

# Saving Data

The program saves all URL information in a file called:

```text
urls.json
```

For example:

```json
{
    "aB72xK": {
        "url": "https://www.google.com",
        "created_at": "2026-10-01T20:15:32",
        "clicks": 2
    }
}
```

This means the URLs are **not lost when the program is closed**.

---

# URL Checking

The program accepts `http` and `https` URLs.

### Valid examples

```text
https://www.google.com
https://github.com
https://example.com/page
```

### Invalid examples

```text
google.com
hello
www.google.com
ftp://example.com
```

Invalid URLs will show an error message.

---

# Error Handling

The program can handle:

* Invalid URLs
* Short codes that do not exist
* Aliases that are already being used
* Invalid aliases
* Problems with the saved data file

For example:

```bash
python main.py resolve unknown123
```

Output:

```text
Error: Short code 'unknown123' was not found.
```

---

# Technologies Used

This project was made using:

* **Python**
* **Visual Studio Code**
* Python standard library

No external packages or URL-shortening websites are used.

---

# Testing

The program was tested for:

* Shortening URLs
* Finding original URLs
* Saving data
* Listing URLs
* Custom aliases
* Click counting
* Invalid URLs
* Missing codes
* Deleting URLs
* Opening URLs in the browser

---

# Future Improvements

In the future, this project could be improved by adding:

* A website interface
* A database
* QR code generation
* URL expiration
* More detailed statistics

---

# Author

**Tashi Saxena**

**Mini URL Shortener — Track A**

Made using **Python in Visual Studio Code**.
