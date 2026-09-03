def parse_url(url):
    match url.split("://", 1):
        case [protocol, rest] if protocol in ("https", "http", "ftp"):
            if "/" in rest:
                domain, path = rest.split("/", 1)
                path = "/" + path
            else:
                domain, path = rest, "/"
            
            info = {"protocol": protocol, "domain": domain, "path": path}

            if path.lower().endswith((".jpg", ".png")):
                info["type"] = "image"
            elif "api" in rest:
                info["type"] = "api"
            
            return info
        
        case _:
            return "Invalid URL"
        
def display_url_info(url_info):
    if isinstance( url_info, str):
        print(url_info)
        return
    print(f"Protocol: {url_info['protocol']}")
    print(f"Domain: {url_info['domain']}")
    print(f"Path: {url_info['path']}")
    if "type" in url_info:
        print(f"Type: {url_info['type']}")

if __name__ == "__main__":
    urls = [
        "https://example.com/page",
        "http://example.com",
        "ftp://files.example.com/data.zip",
        "https://api.example.com/users/123",
        "https://images.example.com/photo.jpg",
        "not-a-valid-url",
    ]

    for url in urls:
        info = parse_url(url)
        display_url_info(info)
        print("---")
    
'''
🔴 Very Hard Level (3 Questions)

Q5: The URL Parser with Pattern Matching (Hard)

Write a function parse_url(url) that uses match to parse URLs.

The function should:

1. Take a URL string as input
2. Use match (pattern matching) to handle these URL patterns:
   · "https://example.com/page" → returns {"protocol": "https", "domain": "example.com", "path": "/page"}
   · "http://example.com" → returns {"protocol": "http", "domain": "example.com", "path": "/"}
   · "ftp://files.example.com/data.zip" → returns {"protocol": "ftp", "domain": "files.example.com", "path": "/data.zip"}
   · Any other URL → returns "Invalid URL"
3. Hard part: Use match with guards (conditions) to handle:
   · URLs ending in .jpg, .png → add {"type": "image"}
   · URLs containing api → add {"type": "api"}
4. Write a second function display_url_info(url_info) that prints the parsed info neatly.

Concepts: match statement, functions, dictionaries, string methods

Example:

url = "https://api.example.com/users/123"
info = parse_url(url)
display_url_info(info)
Output:

Protocol: https
Domain: api.example.com
Path: /users/123
Type: api
---
'''
