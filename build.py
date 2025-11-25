import requests
import re
import yaml
import os

# Load config
with open("sports-config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

site_url = cfg["site"]["url"]
timeout = cfg["site"]["timeout"]
user_agent = cfg["site"]["user_agent"]

output_file = cfg["output"]["file"]
logo_url = cfg["output"]["logo"]
group_name = cfg["output"]["group"]

headers = {"User-Agent": user_agent}

print(f"Scanning site: {site_url}")

try:
    r = requests.get(site_url, headers=headers, timeout=timeout)
    html = r.text
except Exception as e:
    print(f"Error fetching site: {e}")
    exit()

# Find all m3u8 links
m3u_links = re.findall(r'https?://[^\'" ]+\.m3u8', html)

if not m3u_links:
    print("No m3u8 links found.")
    exit()

print(f"Found {len(m3u_links)} m3u8 links.")

# Build M3U content
m3u_content = "#EXTM3U\n\n"

for link in m3u_links:
    # Extract channel name from URL
    chan_name = link.split('/')[-1].replace('.m3u8','')
    m3u_content += f'''#EXTINF:-1 tvg-logo="{logo_url}" group-title="{group_name}", {chan_name}
{link}

'''

# Save M3U file
output_path = os.path.join(os.getcwd(), output_file)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(m3u_content)

print(f"M3U file created: {output_path}")
