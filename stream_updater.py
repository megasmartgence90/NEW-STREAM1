import requests, yaml, json, time, os
from datetime import datetime

CONFIG_FILE = "config.json"
YAML_FILE = "stream.yaml"

def get_latest_stream_url():
    # Burada saytdan dinamik olaraq m3u8 linki çıxarılır.
    # Tədris məqsədli nümunə olaraq sadəcə mövcud link qaytarılır.
    return "https://demiroren.daioncdn.net/teve2/teve2.m3u8"

def update_files():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    url = get_latest_stream_url()
    config["stream_url"] = url
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

    yaml_data = {
        "stream": {
            "name": "teve2",
            "url": url,
            "updated": datetime.now().isoformat()
        }
    }
    with open(YAML_FILE, "w") as f:
        yaml.dump(yaml_data, f)

    os.makedirs(os.path.dirname(config["output_path"]), exist_ok=True)
    with open(config["output_path"], "w") as f:
        f.write(url)

    print(f"Yeniləndi: {url}")

if __name__ == "__main__":
    while True:
        update_files()
        time.sleep(7200)  # 2 saat
