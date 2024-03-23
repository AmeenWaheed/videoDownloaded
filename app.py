from flask import (
    Flask,
    render_template,
    request,
    jsonify,
)
from pytube import YouTube, Playlist  # Import libraries for working with YouTube videos
import os

app = Flask(__name__)  # Create a Flask application instance
DOWNLOAD_FOLDER = "YT.D"
app.config["DOWNLOAD_FOLDER"] = DOWNLOAD_FOLDER

# Define the port
port = int(os.environ.get("PORT", 5000))


# Function to get video information (title and thumbnail URL)
def get_video_info(url):
    try:
        yt = YouTube(url)  # Create a YouTube video object
        title = yt.title  # Get the video title
        thumbnail_url = yt.thumbnail_url  # Get the thumbnail URL
        return title, thumbnail_url  # Return the video title and thumbnail URL
    except:
        return None, None  # Return None values if an exception occurs


@app.route("/")  # Define the root route of the application
def index():
    return render_template(
        "index.html", title="YT.Downloader"
    )  # Render the index.html template with the title "YT.Downloader"


@app.route(
    "/download/video", methods=["GET"]
)  # Define a route for downloading a single video (POST method)
def download_video():
    video_url = request.args.get("url")
    resolution = request.args.get("resolution", "highest")

    try:
        yt = YouTube(video_url)  # Create a YouTube video object

        if resolution == "highest":
            stream = (
                yt.streams.get_highest_resolution()
            )  # Get the highest available resolution stream
        else:
            stream = yt.streams.filter(
                res=resolution
            ).first()  # Get the stream with the specified resolution

        if stream:
            file_path = stream.download(output_path=app.config["DOWNLOAD_FOLDER"])
            title, thumbnail_url = get_video_info(video_url)  # Get video information
            filename = os.path.basename(file_path)
            download_url = f"{request.base_url}downloaded/{filename}"
            response = {
                "message": "Video downloaded!",  # Success message
                "title": title,  # Video title
                "thumbnail_url": thumbnail_url,  # Thumbnail URL
                "resolution": resolution,  # Resolution of the downloaded video
                "download_url": download_url,  # Download the video
            }

            return jsonify(response)  # Return the response as JSON
        else:
            return (
                jsonify({"error"}),
                404,
            )  # Return an error message if the stream is not found

    except Exception as ex:
        return (
            jsonify({"error", str(ex)}),
            505,
        )  # Return an error message if an exception occurs


@app.route(
    "/download/play_list", methods=["GET"]
)  # Define a route for downloading a playlist (POST method)
def download_play_list():
    playlist_url = request.args.get("url")  # Get playlist URL from query parameter
    resolution = request.args.get(
        "resolution", "highest"
    )  # Get resolution, default to 'highest'

    downloaded_videos = []

    try:
        playlist = Playlist(playlist_url)  # Create a Playlist object

        for video in playlist.video_urls:  # Loop through each video in the playlist
            yt = YouTube(video)  # Create a YouTube video object
            if resolution == "highest":
                stream = (
                    yt.streams.get_highest_resolution()
                )  # Get the highest available resolution stream
            else:
                stream = yt.streams.filter(
                    progressive=True
                ).first()  # Get the progressive stream

            if stream:
                file_path = stream.download(output_path=app.config[f"DOWNLOAD_FOLDER"])
                title, thumbnail_url = get_video_info(video)  # Get video information
                filename = os.path.basename(file_path)
                download_url = f"{request.base_url}downloaded/{filename}"

                downloaded_videos.append(
                    {
                        "message": "Videos Downloaded",  # Success message
                        "title": title,  # Video title
                        "thumbnail_url": thumbnail_url,  # Thumbnail URL
                        "resolution": resolution,  # Resolution of the downloaded videos
                        "download_url": download_url,
                    }
                )
                # We can return the response inside the loop if we want to show information for each video downloaded
            else:
                return jsonify(
                    {"error"}
                )  # Return an error message if the stream is not found

        response = {
            "message": "Playlist Downloaded",
            "downloaded_videos": downloaded_videos,
        }

        return jsonify(response)
    # Return the response as JSON (for the last video in the playlist)

    except Exception as ex:
        return jsonify(
            {"error": str(ex)}
        )  # Return an error message if an exception occurs


if __name__ == "__main__":
    app.run(
        debug=False, port=port, host="0.0.0.0"
    )  # Run the Flask application in debug mode on port 9000
