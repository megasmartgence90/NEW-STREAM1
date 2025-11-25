import requests
import yaml
import os

# Load config
with open("sports-config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

channels = cfg["channels"]
output_file = cfg["output"]["file"]

user_agent = "Mozilla/5.0"
headers = {"User-Agent": user_agent}

m3u_content = "#EXTM3U\n\n"

for link, chan_name in channels.items():
    try:
        r = requests.head(link, headers=headers, timeout=5)
        if r.status_code == 200:
            m3u_content += f"#EXTINF:-1,{chan_name}\n{link}\n\n"
            print(f"✔ Added: {chan_name}")
        else:
            print(f"- Offline: {chan_name}")
    except Exception as e:
        print(f"- Error checking {chan_name}: {e}")

output_path = os.path.join(os.getcwd(), output_file)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(m3u_content)

print(f"\n✅ M3U file created: {output_path}")
