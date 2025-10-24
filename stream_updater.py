import os
import sys
import json
import yaml
import streamlink

def info_to_text(stream_info, url):
    text = '#EXT-X-STREAM-INF:'
    bandwidth = getattr(stream_info, "bandwidth", None)
    codecs = getattr(stream_info, "codecs", None)
    resolution = getattr(stream_info, "resolution", None)
    program_id = getattr(stream_info, "program_id", None)

    if program_id:
        text += f'PROGRAM-ID={program_id},'
    if bandwidth:
        text += f'BANDWIDTH={bandwidth},'
    if codecs:
        text += 'CODECS="' + ",".join(codecs) + '",'
    if resolution and getattr(resolution, "width", None):
        text += f'RESOLUTION={resolution.width}x{resolution.height}'
    text += "\n" + url + "\n"
    return text


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        if path.endswith(".yaml") or path.endswith(".yml"):
            return yaml.safe_load(f)
        return json.load(f)


def ensure_folder(path):
    os.makedirs(path, exist_ok=True)
    return path


def main():
    if len(sys.argv) < 2:
        print("İstifadə: python stream_updater.py config.json (və ya config.yaml)")
        sys.exit(1)

    config = load_config(sys.argv[1])

    output_cfg = config.get("output", {})
    folder_name = output_cfg.get("folder", "streams")
    best_folder_name = output_cfg.get("bestFolder", "best")
    master_folder_name = output_cfg.get("masterFolder", "master")

    root_folder = ensure_folder(os.path.join(os.getcwd(), folder_name))
    best_folder = ensure_folder(os.path.join(root_folder, best_folder_name))
    master_folder = ensure_folder(os.path.join(root_folder, master_folder_name))

    channels = config.get("channels", [])

    for channel in channels:
        name = channel.get("name", "")
        slug = channel.get("slug", "unknown")
        url = channel.get("url", "")
        print(f"🔎 {name} üçün link yoxlanır...")

        master_file_path = os.path.join(master_folder, f"{slug}.m3u8")
        best_file_path = os.path.join(best_folder, f"{slug}.m3u8")

        try:
            session = streamlink.Streamlink()
            streams = session.streams(url)

            if not streams:
                print(f"⚠️ {name}: Heç bir stream tapılmadı.")
                continue

            best_stream = streams.get("best")
            if not best_stream:
                print(f"⚠️ {name}: 'best' stream yoxdur.")
                continue

            playlists = getattr(best_stream, "multivariant", None)
            master_text = "#EXTM3U\n"
            best_text = "#EXTM3U\n"

            if playlists and getattr(playlists, "playlists", None):
                version = getattr(playlists, "version", 4)
                master_text = f"#EXTM3U\n#EXT-X-VERSION:{version}\n"
                best_text = f"#EXTM3U\n#EXT-X-VERSION:{version}\n"

                previous_res_height = 0
                for p in playlists.playlists:
                    info = p.stream_info
                    uri = p.uri
                    if not info:
                        continue

                    sub_text = info_to_text(info, uri)
                    res = getattr(info, "resolution", None)
                    height = getattr(res, "height", 0) if res else 0
                    if height > previous_res_height:
                        best_text = sub_text
                        master_text = sub_text + master_text
                        previous_res_height = height
                    else:
                        master_text += sub_text
            else:
                stream_url = best_stream.url
                master_text = f"#EXTM3U\n{stream_url}\n"
                best_text = master_text

            with open(master_file_path, "w", encoding="utf-8") as mf:
                mf.write(master_text)
            with open(best_file_path, "w", encoding="utf-8") as bf:
                bf.write(best_text)

            print(f"✅ {name}: M3U8 fayllar yaradıldı.")
        except Exception as e:
            print(f"❌ {name}: Xəta baş verdi -> {e}")
            if os.path.isfile(master_file_path):
                os.remove(master_file_path)
            if os.path.isfile(best_file_path):
                os.remove(best_file_path)


if __name__ == "__main__":
    main()
