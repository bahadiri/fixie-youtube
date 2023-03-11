import urllib.parse
from bs4 import BeautifulSoup
import re

import fixieai

BASE_PROMPT = """I am an agent that finds and recommends Youtube videos."""

FEW_SHOTS = """
Q: Show me a video with cats?
Thought: I can recommend Youtube videos about cats that you may find interesting.
Ask Func[search]: cats
Func[search] says: https://www.youtube.com/shorts/WeiONy5Q9cQ [image1]
A: You can watch https://www.youtube.com/shorts/WeiONy5Q9cQ [image1]
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def search(query: fixieai.Message) -> fixieai.Message:
    # TODO: find and return a youtube video
    text = query.text.replace("[[", "[").replace("]]", "]")
    search_uri = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(text)
    
    html = urllib.request.urlopen(search_uri).read().decode("utf-8") 
    def write_to_file(text):
        with open("youtube_results.out", "w") as f:
            f.write(text)
    write_to_file(html)
    def parse_results(html):
        regex = re.compile(r"videoId\":\"([^\"]*)")
        regex_results = regex.findall(html)
        return regex_results
        
        
    results = parse_results(html)
    thumbnail_uri = "https://i.ytimg.com/vi/" + results[0] + "/hq720.jpg"
    embed = fixieai.Embed(content_type="image/jpg", uri=thumbnail_uri)
    print("Thumbnail URI: " + thumbnail_uri)
    url = "https://www.youtube.com/watch?v=" + results[0]
    return fixieai.Message(text="You can watch " + url + " [image1]", embeds={"image1": embed})