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
    
