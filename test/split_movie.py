import cv2
import os
import shutil
import unittest

from src.split_movie import AssignSubtitleInFrame
from src.split_movie import ConvertToSec
from src.split_movie import ConvertToTime
from src.split_movie import GetOutputDirectory
from src.split_movie import GetTime
from src.split_movie import GetTimestamps
from src.split_movie import LoadSubtitleFile
from src.split_movie import PadBbox
from src.split_movie import SplitMovie


class SplitMovieTest(unittest.TestCase):

    def test_GetOutputDirectory_1_layer(self):
        test_path = "hoge/fuga"
        expected_str = "hoge"
        self.assertEqual(GetOutputDirectory(test_path), expected_str)

    def test_GetOutputDirectory_2_layer(self):
        test_path = "hoge/hoge/fuga"
        expected_str = "hoge/hoge"
        self.assertEqual(GetOutputDirectory(test_path), expected_str)

    def test_SplitMovie_type_of_frame_image_paths(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        frame_image_paths, _ = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        self.assertEqual(type(frame_image_paths), list)

    def test_SplitMovie_type_of_frame_image_paths_0(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        frame_image_paths, _ = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        self.assertEqual(type(frame_image_paths[0]), str)

    def test_SplitMovie_msec_digits_of_frame_image_paths_0(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        frame_image_paths, _ = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        frame_image_paths_0_basename: str = os.path.splitext(
            os.path.basename(frame_image_paths[0]))[0]
        sec = frame_image_paths_0_basename.split("_")[-1]
        msec = sec.split(".")[-1]
        self.assertEqual(len(msec), 3)

    def test_SplitMovie_type_of_timestamps(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        _, timestamps = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        self.assertEqual(type(timestamps), list)

    def test_SplitMovie_type_of_timestamps_0(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        _, timestamps = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        self.assertEqual(type(timestamps[0]), tuple)

    def test_SplitMovie_length_of_timestamps_0(self):
        movie_path = "test/resource/test1.mp4"
        output_directory = "test/resource/"
        print()
        _, timestamps = SplitMovie(movie_path, output_directory)
        shutil.rmtree("test/resource/test1/")
        self.assertEqual(len(timestamps[0]), 3)

    def test_GetTimestamps_type_of_timestamps(self):
        movie_path = "test/resource/test1.mp4"
        cap = cv2.VideoCapture(movie_path)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        self.assertEqual(type(timestamps), list)

    def test_GetTimestamps_length_of_timestamps(self):
        movie_path = "test/resource/test1.mp4"
        cap = cv2.VideoCapture(movie_path)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        self.assertEqual(len(timestamps), 874)

    def test_GetTimestamps_type_of_timestamps_0(self):
        movie_path = "test/resource/test1.mp4"
        cap = cv2.VideoCapture(movie_path)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        self.assertEqual(type(timestamps[0]), tuple)

    def test_GetTimestamps_length_of_timestamps_0(self):
        movie_path = "test/resource/test1.mp4"
        cap = cv2.VideoCapture(movie_path)
        n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        self.assertEqual(len(timestamps[0]), 3)

    def test_LoadSubtitleFile_type_of_subtitles(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles), list)

    def test_LoadSubtitleFile_type_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles[0]), dict)

    def test_LoadSubtitleFile_type_of_num_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles[0]["num"]), int)

    def test_LoadSubtitleFile_type_of_start_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles[0]["start"]), tuple)

    def test_LoadSubtitleFile_length_of_start_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(len(subtitles[0]["start"]), 3)

    def test_LoadSubtitleFile_type_of_end_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles[0]["end"]), tuple)

    def test_LoadSubtitleFile_length_of_end_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(len(subtitles[0]["end"]), 3)

    def test_LoadSubtitleFile_type_of_body_of_subtitles_0(self):
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        self.assertEqual(type(subtitles[0]["body"]), str)

    def test_GetTime_start_hour(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        start, _ = GetTime(time_format)
        self.assertEqual(int(start[0]), 0)

    def test_GetTime_start_min(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        start, _ = GetTime(time_format)
        self.assertEqual(int(start[1]), 1)

    def test_GetTime_start_sec(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        start, _ = GetTime(time_format)
        self.assertAlmostEqual(start[2], 2.345, delta=0.0001)

    def test_GetTime_end_hour(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        _, end = GetTime(time_format)
        self.assertEqual(int(end[0]), 6)

    def test_GetTime_end_min(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        _, end = GetTime(time_format)
        self.assertEqual(int(end[1]), 7)

    def test_GetTime_end_sec(self):
        time_format = "00:01:02,345 --> 06:07:08,901"
        _, end = GetTime(time_format)
        self.assertAlmostEqual(end[2], 8.901, delta=0.0001)

    def test_ConvertToTime_hour(self):
        format = "00:01:02,345"
        time = ConvertToTime(format)
        self.assertEqual(int(time[0]), 0)

    def test_ConvertToTime_min(self):
        format = "00:01:02,345"
        time = ConvertToTime(format)
        self.assertEqual(int(time[1]), 1)

    def test_ConvertToTime_sec(self):
        format = "00:01:02,345"
        time = ConvertToTime(format)
        self.assertAlmostEqual(time[2], 2.345, delta=0.0001)

    def test_AssignSubtitleInFrame_type_of_subtitles_in_frames(self):
        movie_path = "test/resource/test1.mp4"
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        captured_movie = cv2.VideoCapture(movie_path)
        n_frames = int(captured_movie.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = captured_movie.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        subtitles_in_frames = AssignSubtitleInFrame(subtitles, timestamps)
        self.assertEqual(type(subtitles_in_frames), list)

    def test_AssignSubtitleInFrame_length_of_subtitles_in_frames(self):
        movie_path = "test/resource/test1.mp4"
        subtitle_file = "test/resource/test1.srt"
        subtitles = LoadSubtitleFile(subtitle_file)
        captured_movie = cv2.VideoCapture(movie_path)
        n_frames = int(captured_movie.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = captured_movie.get(cv2.CAP_PROP_FPS)
        timestamps = GetTimestamps(n_frames, fps)
        subtitles_in_frames = AssignSubtitleInFrame(subtitles, timestamps)
        self.assertEqual(len(subtitles_in_frames), len(timestamps))

    def test_ConvertToSec(self):
        time = (1, 2, 3.456)
        sec = ConvertToSec(time)
        self.assertAlmostEqual(sec, 3723.456, delta=0.0001)

    def test_PadBbox(self):
        rectangle = (10, 10, 12, 12)
        rectangle = PadBbox(rectangle, 1)
        self.assertEqual(rectangle, (9, 9, 13, 13))
