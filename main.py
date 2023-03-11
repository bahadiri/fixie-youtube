import urllib.parse
from bs4 import BeautifulSoup
import re

import fixieai

BASE_PROMPT = """I am an agent that finds and recommends Youtube videos."""

FEW_SHOTS = """
Q: Show me a video with cats?
Thought: I can recommend Youtube videos about cats that you may find interesting.
Ask Func[search]: cats
Func[search] says: https://www.youtube.com/watch?v=WeiONy5Q9cQ [image1]
A: You can watch https://www.youtube.com/watch?v=WeiONy5Q9cQ [image1]

Q: Recommend me a video on dogs
Thought: I can recommend Youtube videos about cots that you may find interesting.
Ask Func[search]: dogs
Func[search] says: https://www.youtube.com/watch?v=59rADhtMzWc [image1]
A: You can watch https://www.youtube.com/watch?v=59rADhtMzWc [image1]

Q: Recommend me a query based on the video.
Ask Func[createQuery]: https://www.youtube.com/watch?v=59rADhtMzWc
Func[createQuery] says: dogs and cows
A: dogs and cows
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)

@agent.register_func
def createQuery(url: str) -> fixieai.Message:
    # TODO: extract a textual query based on the provided URL
    query = fixieai.Message(text)
    return query

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