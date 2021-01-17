# Simple Script to get images from https://film-grab.com

import requests
import os
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


base_url = "http://www.film-grab.com/"
def valid_url(url):
    # checks that URL is valid
    parsed_url = urlparse(url)
    return bool(parsed_url.netloc) and bool(parsed_url.scheme)



def get_images(film):
    film = film.lower().replace(" ","-")
    url = base_url + film + "/"
    
    urls = []
    if valid_url(url):
        soup = bs(requests.get(url).content, "html.parser")
        for img in tqdm(soup.find_all("img"), "Collecting image URLs"):
            img_url = img.attrs.get("src").replace("/thumb","")
            img_url = urljoin(url, img_url)
            try:
                pos = img_url.index("?")
                img_url = img_url[:pos]
            except ValueError:
                pass

            if valid_url(img_url):
                urls.append(img_url)
        
        
    else:
        print("Film not available")
    
    return urls

def download(url, pathname):
    """
    Downloads a file given an URL and puts it in the folder `pathname`
    """
    # if path doesn't exist, make that path dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # download the body of response by chunk, not immediately
    response = requests.get(url, stream=True)
    # get the total file size
    file_size = int(response.headers.get("Content-Length", 0))
    # get the file name
    filename = os.path.join(pathname, url.split("/")[-1])
    # progress bar, changing the unit to bytes instead of iteration (default by tqdm)
    progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        for data in progress:
            # write data read to the file
            f.write(data)
            # update the progress bar manually
            progress.update(len(data))


def main(film, path):
    imgs = get_images(film)
    for img in imgs:
        # for each image, download it
        download(img, path)

main('blade runner 2049', '/Users/vinit/Desktop/2049')

'''


for img in get_images('blade runner 2049'):
    pass

    '''