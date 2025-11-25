import requests
import re
import yaml

# Load YAML configuration
with open("sports-config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

settings = config["settings"]
paths = config["paths"]
channels = config["channels"]
output = config["output"]

domain_pattern = settings["domain_pattern"]
timeout = settings["timeout"]
min_html_length = settings["min_html_length"]

headers_base = {
    "User-Agent": settings["user_agent"]
}

print("Scanning domains...")

active_domain = None

# Search active domain
for i in range(settings["domain_scan_start"], settings["domain_scan_end"]):
    test_site = domain_pattern.format(n=i)

    try:
        r = requests.get(test_site, timeout=timeout)
        if r.status_code == 200 and len(r.text) > min_html_length:
            active_domain = test_site
            print(f"Active domain found: {active_domain}")
            break
    except:
        pass

if not active_domain:
    print("No active domain found.")
    exit()

# Scan source code for m3u8 links
print("Scanning source code...")
html = requests.get(active_domain).text
all_m3u8 = re.findall(r'https?://[^\'" ]+\.m3u8', html)

if not all_m3u8:
    print("No m3u8 links found.")
    exit()

domains = list(set([link.split("/")[0] + "//" + link.split("/")[2] for link in all_m3u8]))
print(f"Found stream domains: {domains}")

working_stream_domain = None

test_headers = {
    "Referer": active_domain,
    "Origin": active_domain,
    "User-Agent": settings["user_agent"]
}

print("Testing domains...")

# Test stream domains
for domain in domains:
    test_url = f"{domain}{paths['stream_test_path']}"
    try:
        r = requests.get(test_url, headers=test_headers, timeout=timeout)
        if r.status_code == 200 and "#EXTM3U" in r.text[:100]:
            working_stream_domain = domain
            print(f"ACTIVE STREAM DOMAIN: {domain}")
            break
        else:
            print(f"Inactive: {domain}")
    except:
        print(f"Error: {domain}")

if not working_stream_domain:
    print("No working stream domain found.")
    exit()

print("Building M3U file...")

m3u = "#EXTM3U\n\n"

# Add channels
for cid, name in channels.items():
    stream_url = f"{working_stream_domain}/{cid}/{paths['stream_suffix']}"

    try:
        r = requests.head(stream_url, headers=test_headers, timeout=timeout)
        if r.status_code == 200:
            print(f"ADDED: {name}")
        else:
            print(f"INACTIVE: {name}")
    except:
        print(f"ERROR: {name}")

    m3u += f'''#EXTINF:-1 tvg-logo="{output["logo_url"]}" group-title="{output["group_title"]}", {name}
#EXTVLCOPT:http-referrer={active_domain}
#EXTVLCOPT:http-origin={active_domain}
{stream_url}

'''

# Save M3U
with open(output["file_name"], "w", encoding="utf-8") as f:
    f.write(m3u)

print("Complete!")
print(f"File created: {output['file_name']}")
