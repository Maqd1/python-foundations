# URL Parser with Pattern Matching

## Hard Level — Question 5

Write a function `parse_url(url)` that uses Python's **`match` statement** to parse URLs.

### Requirements

The `parse_url(url)` function should:

1. Take a URL string as input.
2. Use `match` (pattern matching) to handle the supported URL patterns.
3. Return a dictionary containing the parsed URL information.
4. Return `"Invalid URL"` for unsupported URL formats.

### Supported URL Patterns

#### HTTPS URL

```text
https://example.com/page
```

Should return:

```python
{
    "protocol": "https",
    "domain": "example.com",
    "path": "/page"
}
```

#### HTTP URL

```text
http://example.com
```

Should return:

```python
{
    "protocol": "http",
    "domain": "example.com",
    "path": "/"
}
```

#### FTP URL

```text
ftp://files.example.com/data.zip
```

Should return:

```python
{
    "protocol": "ftp",
    "domain": "files.example.com",
    "path": "/data.zip"
}
```

#### Invalid URL

Any other URL format should return:

```text
Invalid URL
```

### Pattern Matching with Guards

The harder part is using `match` with **guards (conditions)** to identify special URL types.

#### Image URLs

URLs ending in:

* `.jpg`
* `.png`

should have:

```python
{"type": "image"}
```

added to the returned information.

#### API URLs

URLs containing `api` should have:

```python
{"type": "api"}
```

added to the returned information.

### Required Functions

#### `parse_url(url)`

Parses the URL and returns the appropriate dictionary or `"Invalid URL"`.

#### `display_url_info(url_info)`

Takes the parsed URL information and displays it neatly.

### Example

```python
url = "https://api.example.com/users/123"
info = parse_url(url)
display_url_info(info)
```

### Expected Output

```text
Protocol: https
Domain: api.example.com
Path: /users/123
Type: api
```

### Concepts

* `match` statement
* Pattern matching
* Guards
* Functions
* Dictionaries
* String methods
