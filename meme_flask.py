from flask import Flask, render_template
import requests

app = Flask(__name__)


def get_meme(subreddit):
    url = f"https://meme-api.com/gimme/{subreddit}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        meme_large = data["preview"][-1]
        title = data["title"]
        return meme_large, title
    except requests.exceptions.RequestException as e:
        print(f"Error fetching meme from {subreddit}: {e}")
        return None, None


# Dynamic route that matches /<subreddit>
@app.route("/<string:subreddit>")
def dynamic_route(subreddit):
    meme_pic, title = get_meme(subreddit)
    if meme_pic:  # Check if meme was fetched successfully
        return render_template("index.html", meme_pic=meme_pic, title=title, subreddit=subreddit)
    else:
        return f"Failed to fetch meme from r/{subreddit}. Try a meme subreddit. ", 500  # Error handling if meme fetch fails


@app.route("/")
def index():
    # Default homepage (if you want to show a default meme or something else here)
    meme_pic, title = get_meme("lies")
    return render_template("index.html", meme_pic=meme_pic, title=title, subreddit="lies")


if __name__ == "__main__":
    app.run(debug=True)
