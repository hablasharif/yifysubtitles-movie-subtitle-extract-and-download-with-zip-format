
from bs4 import BeautifulSoup
from lxml import html
import os
import requests

# Base URL
base_url = "https://yifysubtitles.ch/"

# Create the folder to save the subtitle files
if not os.path.exists("mysubfiles"):
    os.makedirs("mysubfiles")

# Function to download subtitles from a list of URLs
def download_subtitles(url_list):
    for url in url_list:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the first <span> element with class "sub-lang" containing "English"
            english_subtitle = soup.find('span', class_='sub-lang', text='English')

            if english_subtitle:
                # Extract the URL associated with the English subtitle
                subtitle_url = english_subtitle.find_next('a')['href']

                # Combine the base URL with the subtitle URL
                full_subtitle_url = base_url + subtitle_url

                print("Subtitle URL:", full_subtitle_url)

                # Send an HTTP GET request to the subtitle page
                subtitle_response = requests.get(full_subtitle_url)

                if subtitle_response.status_code == 200:
                    # Parse the HTML content of the subtitle page using lxml
                    subtitle_page_content = html.fromstring(subtitle_response.text)

                    # Find the download link for the subtitles using the provided XPath
                    download_link = subtitle_page_content.xpath('/html/body/div[3]/div[1]/div[3]/div[2]/div[4]/a/span[2]')

                    if download_link:
                        download_url = download_link[0].getparent().get('href')
                        full_download_url = base_url + download_url

                        # Get the subtitle filename from the URL
                        subtitle_filename = os.path.basename(full_download_url)

                        # Save the subtitle file in the "mysubfiles" folder
                        subtitle_filepath = os.path.join("mysubfiles", subtitle_filename)

                        with requests.get(full_download_url, stream=True) as download_response:
                            if download_response.status_code == 200:
                                with open(subtitle_filepath, 'wb') as subtitle_file:
                                    for chunk in download_response.iter_content(chunk_size=1024):
                                        subtitle_file.write(chunk)
                                print("Subtitle downloaded as:", subtitle_filepath)
                            else:
                                print("Failed to download the subtitle.")
                    else:
                        print("Download link not found on the subtitle page.")
                else:
                    print("Failed to retrieve the subtitle page. Status code:", subtitle_response.status_code)
            else:
                print("No English subtitles found on the page.")
        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)

# List of URLs to download subtitles from
url_list = [
"https://yifysubtitles.ch/movie-imdb/tt0111161","https://yifysubtitles.ch/movie-imdb/tt0068646","https://yifysubtitles.ch/movie-imdb/tt0468569","https://yifysubtitles.ch/movie-imdb/tt0071562","https://yifysubtitles.ch/movie-imdb/tt0050083","https://yifysubtitles.ch/movie-imdb/tt0108052"
]

# Call the function to download subtitles
download_subtitles(url_list)
