import requests
from typing import List, Tuple
import re
import os
from tqdm import tqdm
from scdl.scdl import main as scdl
import sys
from urllib.parse import quote


learning_center = "https://talktomeinkorean.com/learningcenter/"
soundcloud_client_id = ""
cookies = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def get_lessons() -> List[str]:
    """Gets the lessons from the learning center page.

    Returns:
        List[str]: A list of urls to the lessons.
    """
    # Get the learning center page.
    if os.path.exists("website/index.html"):
        with open("website/index.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        response = requests.get(learning_center, headers=headers, cookies=cookies).text
    
        with open("website/index.html", "w+", encoding="utf-8") as f:
            f.write(response)
    
    # Find all the lessons.
    lessons = re.findall(r"href=\"(https://talktomeinkorean.com/curriculum/level[^\"]+/lessons[^\"]+)", response)
        
    return lessons

def get_lesson(url: str) -> str:
    """Gets the lesson page and saves it to the /website/ directory.

    Args:
        url (str): The url of the lesson page.

    Returns:
        str: The html of the lesson page.
    """
    file_name = url.split("curriculum/")[-1].replace("/", "_")[:50]
    
    # Get the lesson page.
    if os.path.exists(f"website/{file_name}.html"):
        with open(f"website/{file_name}.html", "r", encoding="utf-8") as f:
            response = f.read()
    else:
        response = requests.get(url, headers=headers, cookies=cookies).text
        with open(f"website/{file_name}.html", "w+", encoding="utf-8") as f:
            f.write(response)
        
    return response

def hijack_html() -> None:
    """Replaces the links in the html files to the local files.
    """
    with open("resource.txt", "r", encoding="utf-8") as f:
        resource = f.read()
    
    for file in os.listdir("website"):
        if not file.endswith(".html"):
            continue
        
        with open(f"website/{file}", "r", encoding="utf-8") as f:
            html = f.read()
        
        if resource not in html:
            html = html.replace("<meta charset=\"UTF-8\">", resource)
            
        html = re.sub(r"https://soundcloud.com/[^\"<]+", f"<audio controls><source src=\"audio/{quote(file.replace('.html', '.mp3'))}\"></audio>", html)
        
        for hyperlink in re.findall(r"https://talktomeinkorean.com/curriculum/level[^\"]+/lessons[^\"]+", html):
            html = html.replace(hyperlink, f"./{quote(hyperlink.split('curriculum/')[-1].replace('/', '_')[:50])}.html")
        
        for hyperlink in re.findall(r"https://talktomeinkorean.com[^\"]+", html):
            html = html.replace(hyperlink, f"./index.html")
        
        with open(f"website/{file}", "w+", encoding="utf-8") as f:
            f.write(html)

def get_lesson_audio_link(url: str) -> List[Tuple[str, str]]:
    """Gets the audio link from the lesson page.

    Args:
        url (str): The url of the lesson page.

    Returns:
        List[Tuple[str, str]]: A list containing the name and url of the audio.
    """
    file_name = url.split("curriculum/")[-1].replace("/", "_")[:50]
    
    # Get the lesson page.
    lesson_html = get_lesson(url)
    soundcloud_url = re.findall(r"(https://soundcloud.com/[^\"<]+)", lesson_html)
    
    return [file_name, soundcloud_url[0] if soundcloud_url else None]

def download_soundcloud(urls: List[List[str]]) -> None:
    """Downloads the audio from soundcloud to the /website/audio/ directory.

    Args:
        urls (List[List[str]]): A list of lists containing the name and url of the audio.
    """
    # scdl switches the current working directory to the download directory.
    # It's easier to just change the directory here and use no argument.
    os.chdir("website/audio")
    
    for name, url in tqdm(urls, desc="Downloading Soundcloud"):
        name = name.strip()
        url = url.strip()
        
        if os.path.exists(f"{name}.mp3"):
            continue
        
        # Write client_id into commandline arguments.
        sys.argv = ["scdl", "-l", url, "--client-id", soundcloud_client_id, "--name-format", name]
        scdl()


def trim_filenames():
    for file in os.listdir("website"):
        if not file.endswith(".html"):
            continue
        
        os.rename(f"website/{file}", f"website/{file.replace('.html', '')[:50]}.html")
    
    for file in os.listdir("website/audio"):
        if not file.endswith(".mp3"):
            continue

        os.rename(f"website/audio/{file}", f"website/audio/{file.replace('.mp3', '')[:50]}.mp3")
        
def replace_mp3_links():
    for file in os.listdir("docs"):
        if not file.endswith(".html"):
            continue
        
        with open(f"docs/{file}", "r", encoding="utf-8") as f:
            html = f.read()
        
        html = html.replace(f"audio/{quote(file.replace('.html', '.mp3'))}", f"https://github.com/Marilyth/ttmik-selfhost/raw/audio/docs/audio/{file.replace('.html', '.mp3')}")
        
        with open(f"docs/{file}", "w+", encoding="utf-8") as f:
            f.write(html)
        

if __name__ == "__main__":
    replace_mp3_links()
    #trim_filenames()
    soundcloud_urls = []
    
    for lesson in tqdm(get_lessons(), desc="Downloading Lessons"):
        try:
            get_lesson(lesson)
            #soundcloud_urls.append(get_lesson_audio_link(lesson))
        except Exception as e:
            print(f"Failed to download {lesson}")
            print(e)
        
    hijack_html()
    #download_soundcloud(soundcloud_urls)
