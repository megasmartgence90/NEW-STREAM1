import requests
import re
import yaml

# Load YAML
with open("sports-config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

domain_cfg = cfg["domain"]
headers_cfg = cfg["headers"]
stream_cfg = cfg["stream"]
channels = cfg["channels"]
output = cfg["output"]

print("Starting auto M3U generator...\n")

# Build base headers
base_headers = {
    "User-Agent": headers_cfg["user_agent"]
}

active_domain = None

# Step 1 — Find active main page
print("Scanning domains for active REF_SITE...")

for i in range(domain_cfg["scan_start"], domain_cfg["scan_end"]):
    test_site = domain_cfg["pattern"].format(n=i)
    try:
        r = requests.get(test_site, timeout=domain_cfg["timeout"], headers=base_headers)
        if r.status_code == 200 and len(r.text) > domain_cfg["min_html_length"]:
            active_domain = test_site
            print(f"✔ Active site found: {active_domain}")
            break
    except:
        pass

if not active_domain:
    print("❌ No active domain found.")
    exit()

# Step 2 — Extract stream domains
print("\nExtracting stream domains...")
html = requests.get(active_domain, headers=base_headers).text
m3u_links = re.findall(r'https?://[^\'" ]+\.m3u8', html)

if not m3u_links:
    print("❌ No stream links found.")
    exit()

stream_domains = list(set([link.split("/")[0] + "//" + link.split("/")[2] for link in m3u_links]))
print(f"Found domains: {stream_domains}")

# Step 3 — Find active stream domain
print("\nChecking stream domains...")
working_domain = None

test_path = f"/{stream_cfg['test_channel']}/{stream_cfg['test_file']}"

stream_headers = {
    "Referer": active_domain,
    "Origin": active_domain,
    "User-Agent": headers_cfg["user_agent"]
}

for d in stream_domains:
    test_url = f"{d}{test_path}"
    try:
        r = requests.get(test_url, headers=stream_headers, timeout=domain_cfg["timeout"])
        if r.status_code == 200 and "#EXTM3U" in r.text[:100]:
            working_domain = d
            print(f"✔ Active stream server: {working_domain}")
            break
        else:
            print(f"- Inactive: {d}")
    except:
        print(f"- Error connecting: {d}")

if not working_domain:
    print("❌ No working stream domain.")
    exit()

# Step 4 — Build M3U
print("\nGenerating M3U playlist...\n")

m3u = "#EXTM3U\n\n"

for cid, name in channels.items():
    stream_url = f"{working_domain}/{cid}/{stream_cfg['suffix']}"

    try:
        r = requests.head(stream_url, headers=stream_headers, timeout=domain_cfg["timeout"])
        if r.status_code == 200:
            print(f"✔ Added: {name}")
        else:
            print(f"- Offline: {name}")
    except:
        print(f"- Error: {name}")

    m3u += f'''#EXTINF:-1 tvg-logo="{output["logo"]}" group-title="{output["group"]}", {name}
#EXTVLCOPT:http-referrer={active_domain}
#EXTVLCOPT:http-origin={active_domain}
{stream_url}

'''

with open(output["file"], "w", encoding="utf-8") as f:
    f.write(m3u)

print("\n✅ COMPLETE!")
print(f"Created file: {output['file']}")
