import urllib.parse

import fixieai

BASE_PROMPT = """I am an agent that finds and recommends Youtube videos."""

FEW_SHOTS = """
Q: ...
Thought: ...
A: ...

Q: ...
Thought: ...
A: ...

Q: ...
Thought: ...
A: ... 
"""
agent = fixieai.CodeShotAgent(BASE_PROMPT, FEW_SHOTS)


@agent.register_func
def search(query: fixieai.Message) -> str:
    # TODO: find and return a youtube video
    assert query.text == "input"
    return "output"

    text = query.text.replace("[[", "[").replace("]]", "]")
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(text)
    embed = fixieai.Embed(content_type="image/png", uri=url)
    return fixieai.Message(text="Here you go! [image1]", embeds={"image1": embed})
