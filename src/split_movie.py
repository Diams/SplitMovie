import argparse
import cv2
import numpy as np
import os

from PIL import Image, ImageFont, ImageDraw
from tqdm import tqdm


def Main():
    args = SetupOption()
    movie_path = args.movie_path
    subtitle_path = args.subtitle_path
    output_directory = args.output_directory \
        if args.output_directory is not None \
        else GetOutputDirectory(movie_path)
    frame_image_paths, timestamps = SplitMovie(movie_path, output_directory)
    RenderSubtitle(frame_image_paths, timestamps, subtitle_path)


def SetupOption():
    parser = argparse.ArgumentParser()
    parser.add_argument("movie_path")
    parser.add_argument("subtitle_path")
    parser.add_argument("--output_directory", "-o")
    return parser.parse_args()


def GetOutputDirectory(movie_path: str):
    return os.path.dirname(movie_path)


def SplitMovie(movie_path: str, output_directory: str):
    captured_movie = cv2.VideoCapture(movie_path)
    n_frames = int(captured_movie.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = captured_movie.get(cv2.CAP_PROP_FPS)
    base_name = os.path.splitext(os.path.basename(movie_path))[0]
    output_full_path = os.path.join(output_directory, base_name)
    os.makedirs(output_full_path, exist_ok=True)
    timestamps = GetTimestamps(n_frames, fps)
    paths = []
    for i in tqdm(timestamps):
        _, frame = captured_movie.read()
        current_path = os.path.join(
            output_full_path, f"{int(i[0])}_{int(i[1])}_{i[2]:.3f}.png")
        imwrite(current_path, frame)
        paths.append(current_path)
    return paths, timestamps


def GetTimestamps(n_frames: int, fps: float):
    timestamps = np.linspace(0.0, n_frames / fps, n_frames)
    result = []
    for it in timestamps:
        hour = it // 60 // 60
        minuts = (it - hour * 60 * 60) // 60
        sec = (it - hour * 60 * 60 - minuts * 60)
        result.append((hour, minuts, sec))
    return result


def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)
        if result:
            with open(filename, mode="w+b") as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def RenderSubtitle(image_paths, timestamps, subtitle_file):
    subtitles = LoadSubtitleFile(subtitle_file)
    subtitles_in_frames = AssignSubtitleInFrame(subtitles, timestamps)
    for i, image_path in enumerate(tqdm(image_paths)):
        if subtitles_in_frames[i] == "":
            continue
        image = Image.open(image_path).convert("RGBA")
        width, height = image.size
        canvas = ImageDraw.Draw(image)
        font = ImageFont.truetype("C:\\Windows\\Fonts\\HGRSGU.TTC", 50)
        textbbox = canvas.textbbox((width // 2, height - 50),
                                   subtitles_in_frames[i], font=font,
                                   anchor="md")
        textbbox = PadBbox(textbbox, 5)
        rect_image = Image.new("RGBA", image.size)
        rect_canvas = ImageDraw.Draw(rect_image)
        rect_canvas.rectangle(textbbox, fill=(0, 0, 0, 200))
        image = Image.alpha_composite(image, rect_image).convert("RGB")
        canvas = ImageDraw.Draw(image)
        canvas.text((width // 2, height - 50),
                    subtitles_in_frames[i], font=font, fill="#FFFFFF",
                    anchor="md", align="center")
        image.save(image_path)


def LoadSubtitleFile(file: str):
    with open(file, "r", encoding="utf-8") as f:
        all_text = "".join(f.readlines()).replace("\u2000", "\u3000")
    subtitles = [list(filter(lambda x: x != "", it.split("\n")))
                 for it in (all_text).split("\n\n")]
    result = []
    for subtitle in subtitles:
        if len(subtitle) == 0:
            continue
        it = {}
        it["num"] = int(subtitle[0])
        start, end = GetTime(subtitle[1])
        it["start"] = start
        it["end"] = end
        it["body"] = "\n".join(subtitle[2:])
        result.append(it)
    return result


def GetTime(time_format: str):
    start, end = time_format.split(" --> ")
    return ConvertToTime(start), ConvertToTime(end)


def ConvertToTime(format: str):
    splited_format = format.split(":")
    hour = int(splited_format[0])
    min = int(splited_format[1])
    sec = float(splited_format[2].replace(",", "."))
    return hour, min, sec


def AssignSubtitleInFrame(subtitles, timestamps):
    result = [""] * len(timestamps)
    for subtitle in subtitles:
        for i, timestamp in enumerate(timestamps):
            start_sec = ConvertToSec(subtitle["start"])
            end_sec = ConvertToSec(subtitle["end"])
            timestamp_sec = ConvertToSec(timestamp)
            if start_sec < timestamp_sec < end_sec:
                result[i] = subtitle["body"]
    return result


def ConvertToSec(time):
    return time[0] * 3600 + time[1] * 60 + time[2]


def PadBbox(rectangle, padding):
    assert len(rectangle) == 4
    rectangle = list(rectangle)
    rectangle[0] -= padding
    rectangle[1] -= padding
    rectangle[2] += padding
    rectangle[3] += padding
    return tuple(rectangle)


if __name__ == "__main__":
    Main()
