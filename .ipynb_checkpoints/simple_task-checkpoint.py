import extract_data as ed

def simple_task():
    max_pages = 5  # You may want to set this or pass it as an argument
    full_urls = ed.get_URLs(max_pages)

    for url in full_urls:
        print(url)
