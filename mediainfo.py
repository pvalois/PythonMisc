#!/usr/bin/env python3
import os
import sys
from pymediainfo import MediaInfo
from colorama import init, Fore, Style
from datetime import timedelta
from dumper import dump

# Initialisation de Colorama
init(autoreset=True)

# Extensions de fichiers multimédias à considérer
EXTENSIONS = {'.mp4', '.webm', '.mkv', '.avi', '.mov', '.m4a', '.mp3', '.flac', '.wav', '.aac'}

def format_duration_ms(duration_ms):
    """Convertit une durée en millisecondes en une chaîne au format HH:MM:SS."""
    try:
      td = timedelta(milliseconds=duration_ms)
      total_seconds = int(td.total_seconds())
      hours, remainder = divmod(total_seconds, 3600)
      minutes, seconds = divmod(remainder, 60)
      return f"{hours:02}:{minutes:02}:{seconds:02}"
    except:
      return f"{duration_ms} ms"


def print_general_info(track):
   if track.track_type == "General":
        duration=format_duration_ms(track.duration)
        print(f"    Durée : {duration}")
        print(f"    Taille du fichier : {track.file_size} octets")
        print(f"    Format : {track.format}")
        print(f"    Nom du fichier : {track.file_name}")
        print()

def print_video_info(track):
    if track.track_type == "Video":
        print(f"    Video.Codec : {track.codec}")
        print(f"    Video.Resolution : {track.width} x {track.height}")
        print(f"    Video.Fréquence d'images : {track.frame_rate}")
        print(f"    Video.Bitrate : {track.bit_rate}")

def print_audio_info(track):
    if track.track_type == "Audio":
        print ()
        print(f"    Audio.Codec : {track.codec}")
        print(f"    Audio.Language : {track.language}")
        print(f"    Audio.Canaux : {track.channel_s}")
        print(f"    Audio.Fréquence d'échantillonnage : {track.sampling_rate}")
        print(f"    Audio.Bitrate : {track.bit_rate}")


def display_media_info(file_path):
    media_info = MediaInfo.parse(file_path)
    print(f"\n{Fore.GREEN}Fichier : {file_path}{Style.RESET_ALL}")

    for track in media_info.tracks:
        print_general_info(track)
        print_video_info(track)
        print_audio_info(track)

def process_directory(start_path):
    for dirpath, dirnames, filenames in os.walk(start_path):
        dirnames.sort()
        for filename in sorted(filenames):
            ext = os.path.splitext(filename)[1].lower()
            if ext in EXTENSIONS:
                full_path = os.path.join(dirpath, filename)
                display_media_info(full_path)

if __name__ == "__main__":
  paths=sys.argv[1:] if len(sys.argv) > 1 else ['.']
  for path in paths:
    if os.path.isdir(path): process_directory(path)
    if os.path.isfile(path): display_media_info(path)


