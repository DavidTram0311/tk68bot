# tk68bot
This bot retrieve BTC ticket price through binance API, then calculating the ADX indicator, and apply a simple algorithm trading for future trading.

# I. Overview
This bot retrieve BTC ticket price through binance API, then calculating the ADX indicator, and apply a simple algorithm trading for future trading. Then push signal to google sheet.  

# II. How to install

- Clone the code into local
  
```
git clone https://github.com/DavidTram0311/tk68bot
```
- Install requirements

```
pip install -r requirements.txt
```

## Example Usage

The easiest way to get a transcript for a given video is to execute:

```
from youtube_transcript_api import YouTubeTranscriptApi

YouTubeTranscriptApi.get_transcript(video_id)
```

***Note:** By default, this will try to access the English transcript of the video. If your video has a different language, or you are interested in fetching a different language's transcript, please read the section below.*

```
[
    {
        'text': 'Hey there',
        'start': 7.58,
        'duration': 6.13
    },
    {
        'text': 'how are you',
        'start': 14.08,
        'duration': 7.58
    },
    # ...
]
```


# III. Functions
## retrieve_sub

```
def retrieve_sub(url):

  video_id = url.replace('https://www.youtube.com/watch?v=','')

  transcript = YouTubeTranscriptApi.get_transcript(video_id)

  return transcript
```

The function extract the video url id, then using `YouTubeTranscriptApi.get_transcript` to get the subtitles during the video

# IV. How to run project
*Running Source code: [youtube-subtitle.ipynb - Colab (google.com)](https://colab.research.google.com/drive/1up7jFR7TjnlqVmqeDesIZEwva48PTsnM?authuser=1#scrollTo=z1QC0vCdVUqO)*

## 1. Retrieving youtube video subtitle from single youtube url

Step 1: Run all code (CTRL  + F9).

Step 2: Type 1 to choose the first method (input single URL).

Step 3: Paste the youtube url into the box.

Step 4: Check the csv exporting into Drive (My Drive) after finishing.
*Format csv file name: youtube_subtitle_yyyy-mm-dd_hourmin.csv*.

![[Pasted image 20240425201402.png]]
## 2.Retrieving youtube video subtitle from multiple youtube url

Step 1: Run all code (CTRL  + F9).

Step 2: Type 2 to choose the second method (input multiple URL).

Step 3: Choose csv or excel file contains youtube links from computer.
*Format file:*
![[Pasted image 20240425200853.png]]

Step 4: Check the csv exporting into Drive (My Drive) after finishing.
*Format csv file name: youtube_subtitle_yyyy-mm-dd_hourmin.csv.*

![[Pasted image 20240425201350.png]]
