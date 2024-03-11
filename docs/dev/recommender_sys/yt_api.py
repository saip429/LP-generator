import csv
from googleapiclient.discovery import build
import json

# API key for YouTube Data API
import constants as c


# Function to search for videos based on keyword and retrieve views and likes
def search_videos(keyword, order_by="relevance", max_results=1):
    # Initialize YouTube Data API client
    youtube = build("youtube", "v3", developerKey=c.YOUTUBE_API)

    # Search for videos based on keyword and filter criteria
    search_response = (
        youtube.search()
        .list(
            q=keyword, part="id", type="video", order=order_by, maxResults=max_results
        )
        .execute()
    )

    # Extract video IDs from search results
    video_ids = [item["id"]["videoId"] for item in search_response["items"]]

    # Initialize list to store video information
    video_info = []

    # Retrieve views and likes for each video
    for video_id in video_ids:
        video_response = youtube.videos().list(part="statistics", id=video_id).execute()

        # Extract views and likes for the video
        views = video_response["items"][0]["statistics"]["viewCount"]
        likes = video_response["items"][0]["statistics"]["likeCount"]

        # Construct video URL
        video_url = f"https://www.youtube.com/watch?v={video_id}"

        # Add video information to the list
        video_info.append({"url": video_url, "views": views, "likes": likes})

    return video_info


# Example usage
# keyword = "python tutorial"
order_by = "viewCount"  # Order search results by views
max_results = 5  # Number of search results to retrieve
# video_info = search_videos(keyword, order_by, max_results)

# Save video information to a CSV file
output_file = "docs/dev/recommender_sys/info.csv"
# with open(output_file, "w", newline="") as csvfile:
#     fieldnames = ["topic", "url", "views", "likes"]
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     # Write the header row with the "topic" field populated
#     writer.writeheader()
#     for video in video_info:
#         video["topic"] = keyword
#         writer.writerow(video)

# print(f"Video information saved to {output_file}")


with open(
    "C:/Users/saipr/Desktop/Learning Path generator/docs/dev/path_generator/course_data.json",
    "r",
) as file:
    # Parse the JSON data
    json_data = json.load(file)

    # Iterate through each topic
    for entry in json_data:
        # Extract the modules
        modules = entry["modules"]

        # Log operations
        with open("docs/dev/recommender_sys/log.txt", "a") as logfile:
            logfile.write(f"Modules for {entry['title']}:")
        for module in modules:

            with open("docs/dev/recommender_sys/log.txt", "a") as logfile:
                logfile.write(f"fetching videos for module: {module}")
            video_info = search_videos(module, order_by, max_results)
            with open(output_file, "a", newline="") as csvfile:
                fieldnames = ["topic", "url", "views", "likes"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for video in video_info:
                    video["topic"] = module
                    writer.writerow(video)
