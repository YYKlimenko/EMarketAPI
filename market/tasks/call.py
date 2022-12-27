from celery import Celery

app = Celery('cll', broker='pyamqp://guest@localhost//', backend='redis://localhost:6379/1')

@app.task
def fetch_url(url):
    return url

def func(urls):
    for url in urls:
        result = fetch_url.delay(url)
        print(result.get())

func(
    ["http://google.com", "https://amazon.in", "https://facebook.com", "https://twitter.com"]
)