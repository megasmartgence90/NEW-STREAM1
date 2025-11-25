import requests
import yaml
import os

# Load config
with open("sports-config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

site_url = cfg["site"]["url"]
timeout = cfg["site"]["timeout"]
user_agent = cfg["site"]["user_agent"]

channels = cfg["channels"]
output_file = cfg["output"]["file"]
logo_url = cfg["output"]["logo"]
group_name = cfg["output"]["group"]

headers = {
    "User-Agent": user_agent,
    "Referer": site_url,
    "Origin": site_url
}

m3u_content = "#EXTM3U\n\n"

for link, chan_name in channels.items():
    try:
        r = requests.head(link, headers=headers, timeout=5)
        if r.status_code == 200:
            m3u_content += f'''#EXTINF:-1 tvg-logo="{logo_url}" group-title="{group_name}", {chan_name}
{link}

'''
            print(f"✔ Added: {chan_name}")
        else:
            print(f"- Offline: {chan_name}")
    except Exception as e:
        print(f"- Error checking {chan_name}: {e}")

output_path = os.path.join(os.getcwd(), output_file)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(m3u_content)

print(f"\n✅ M3U file created: {output_path}")
