# SplitMovie

動画を分割しつつ字幕も焼き付ける

## Clone

```
$ git clone git@github.com:Diams/SplitMovie.git
```

## 環境構築

### 開発環境

- python: 3.9.13

### ライブラリ

- opencv-python==4.6.0.66
- tqdm==4.64.0
- Pillow==9.2.0

### コマンド

```
$ create_env.bat
```

### 使い方

```
$ python split_movie.py <movie path>.mp4 <subtitle file>.srt
```
