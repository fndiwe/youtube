from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from math import floor
from pytube import YouTube
import os
from shutil import rmtree
# from .models import Suggestions
from datetime import datetime
from pytube.contrib.search import Search

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url1 = "https://youtube.com/watch?v="
url2 = "https://youtu.be/"


# Create your views here.
def home(request):
    global yt
    if request.method == 'POST':
        link = request.POST.get('link')
        search = ""
        if not link.startswith(("https://", "http://")) and link != "":
            search += link
            return redirect("select_video", search=search)
        try:
            yt = YouTube(link)
        except:
            messages.error(request, "There was an error getting the video, try again")
        else:
            return redirect("select")

    return render(request, 'index.html', {"year": datetime.now().year})


def select(request):
    global res480, res720, res1080, audio, subtitle, res720_filesize, res480_filesize, res1080_filesize

    try:
        video = yt
        title = video.title
        image = video.thumbnail_url
        length = video.length
        minutes = floor(length / 60)
        res480 = video.streams.get_by_itag(135)
        res720 = video.streams.get_by_itag(22)
        res1080 = video.streams.get_by_itag(137)
        audio = video.streams.get_by_itag(251)
    except:
        messages.error(request, "Sorry, try again")
        return HttpResponseRedirect("/")
    try:
        res480_filesize = round(float(res480.filesize / 1000000), 1)
    except:
        res480_filesize = 0
    try:
        res720_filesize = round(float(res720.filesize / 1000000), 1)
    except:
        res720_filesize = 0
    try:
        res1080_filesize = round(float(res1080.filesize / 1000000), 1)
    except:
        res1080_filesize = 0
    context = {
        "title": title,
        "image": image,
        "minutes": minutes,
        "res480": res480,
        "res720": res720,
        "res1080": res1080,
        "audio": audio,
        "res480_filesize": res480_filesize,
        "res720_filesize": res720_filesize,
        "res1080_filesize": res1080_filesize,
        "year": datetime.now().year
    }
    return render(request, "select.html", context)


def remove_video():
    time = datetime.now().hour
    if time == 23 or time == 12:
        try:
            rmtree(os.path.join(BASE_DIR + "/videos"))
        except:
            pass


def res480_version(request):
    global filename
    video = res480
    if not os.path.exists(os.path.join(BASE_DIR + "/videos", yt.title + ".mp4")):
        try:
            video.download(os.path.join(BASE_DIR + "/videos"))
        except:
            dir = os.path.join(BASE_DIR + "/videos")
            if not os.path.exists(dir):
                os.mkdir(dir)
    filename = yt.title
    # read_file
    with open(os.path.join(BASE_DIR + "/videos", filename + ".mp4"), 'rb') as f:
        data = f.read()
    # download file by response
    response = HttpResponse(data, content_type='application/vnd.mp4')
    response['Content-Disposition'] = f'attachment; filename= "{yt.title}.mp4"'
    return response


def res720_version(request):
    video = res720
    if not os.path.exists(os.path.join(BASE_DIR + "/videos", yt.title + ".mp4")):
        try:
            video.download(os.path.join(BASE_DIR + "/videos"))
        except:
            dir = os.path.join(BASE_DIR + "/videos")
            if not os.path.exists(dir):
                os.mkdir(dir)
    # read_file
    with open(os.path.join(BASE_DIR + "/videos", filename + ".mp4"), 'rb') as f:
        data = f.read()
    #     # download file by response
    response = HttpResponse(data, content_type='application/vnd.mp4')
    response['Content-Disposition'] = f'attachment; filename= "{yt.title}.mp4"'
    return response


def res1080_version(request):
    video = res1080
    if not os.path.exists(os.path.join(BASE_DIR + "/videos", yt.title + ".mp4")):
        try:
            video.download(os.path.join(BASE_DIR + "/videos"))
        except:
            dir = os.path.join(BASE_DIR + "/videos")
            if not os.path.exists(dir):
                os.mkdir(dir)
    # read_file
    with open(os.path.join(BASE_DIR + "/videos", filename + ".mp4"), 'rb') as f:
        data = f.read()
    # # download file by response
    response = HttpResponse(data, content_type='application/vnd.mp4')
    response['Content-Disposition'] = f'attachment; filename= "{yt.title}.mp4"'
    return response


def audio(request):
    mp3 = audio
    if not os.path.exists(os.path.join(BASE_DIR + "/videos", yt.title + ".webm")):
        try:
            mp3.download(os.path.join(BASE_DIR + "/videos"))
        except:
            dir = os.path.join(BASE_DIR + "/videos")
            if not os.path.exists(dir):
                os.mkdir(dir)
    # read_file
    with open(os.path.join(BASE_DIR + "/videos", yt.title + ".webm"), 'rb') as f:
        data = f.read()
    # # download file by response
    response = HttpResponse(data, content_type='application/vnd.webm')
    response['Content-Disposition'] = f'attachment; filename= "{yt.title}.mp3"'
    return response


def select_video(request, search):
    global context
    input = search
    try:
        results = Search(query=input).fetch_query()
    except:
        return HttpResponseRedirect("/")
    contents = \
        results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][
            0][
            "itemSectionRenderer"]["contents"]
    lengths = []
    titles = []
    video_ids = []
    for all_video in contents:
        try:
            all_videos = all_video["videoRenderer"]
        except KeyError:
            pass
        # image = all_videos["thumbnail"]["thumbnails"][0]["url"]
        else:
            video_ids.append(all_videos["videoId"])
            titles.append(all_videos["title"]["runs"][0]["text"])
            lengths.append(all_videos["lengthText"]["accessibility"]["accessibilityData"]["label"])

        context = {"year": datetime.now().year, "titles": titles, "lengths": lengths, "video_ids": video_ids,
                   "zip": zip(titles, video_ids, lengths)}
    return render(request, "selectvideo.html", context)


def get_link(request, video_id):
    global yt
    try:
        yt = YouTube(url1 + video_id)
    except:
        try:
            yt = YouTube(url2 + video_id)
        except:
            messages.error(request, "The link to the video was not found")

    return redirect("select")


remove_video()
