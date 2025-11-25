import requests
import re

print("Test")

active_domain = None
REF_SITE = None

for i in range(1, 100):
    test_site = f"https://ontvizle{i}.live"
    try:
        r = requests.get(test_site, timeout=5)
        if r.status_code == 200 and len(r.text) > 500:
            active_domain = test_site
            REF_SITE = test_site
            print(f"Active domain found: {active_domain}")
            break
    except:
        pass

if not active_domain:
    print("No active domain found.")
    exit()

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
    "Referer": REF_SITE,
    "Origin": REF_SITE,
    "User-Agent": "Mozilla/5.0"
}

print("Testing domains...")

for domain in domains:
    test_url = f"{domain}/705/mono.m3u8"
    try:
        r = requests.get(test_url, headers=test_headers, timeout=5)
        if r.status_code == 200 and "#EXTM3U" in r.text[:100]:
            working_stream_domain = domain
            print(f"ACTIVE STREAM: {domain}")
            break
        else:
            print(f"Inactive: {domain}")
    except:
        print(f"Error: {domain}")

if not working_stream_domain:
    print("No working stream domain found.")
    exit()

channels = {
    701: "beIN sport 1",
    702: "beIN sport 2",
    703: "beIN sport 3",
    704: "beIN sport 4",
    705: "S sport 1",
    706: "Tivibu sport 1",
    707: "smart sport 1",
    708: "Tivibu spor",
    709: "a spor",
    710: "smart sport 2",
    711: "Tivibu sport 2",
    713: "Tivibu sport 4",
    715: "beIN sport max 2",
    730: "S sport 2",
    "tabii": "tabii spor",
    "tabii1": "tabii spor 1",
    "tabii2": "tabii spor 2", 
    "tabii3": "tabii spor 3",
    "tabii4": "tabii spor 4",
    "tabii5": "tabii spor 5",
    "tabii6": "tabii spor 6"
}

print("Adding channels...")

m3u = "#EXTM3U\n\n"

for cid, name in channels.items():
    stream_url = f"{working_stream_domain}/{cid}/mono.m3u8"
    try:
        r = requests.head(stream_url, headers=test_headers, timeout=5)
        if r.status_code == 200:
            print(f"ADDED: {name}")
        else:
            print(f"INACTIVE: {name}")
    except:
        print(f"ERROR: {name}")
    
    m3u += f'''#EXTINF:-1 tvg-logo="https://i.hizliresim.com/ska5t9e.jpg" group-title="SPORTS", {name}
#EXTVLCOPT:http-referrer={REF_SITE}
#EXTVLCOPT:http-origin={REF_SITE}
{stream_url}

'''

file_name = "DeaTHLesS-sports.m3u"
with open(file_name, "w", encoding="utf-8") as f:
    f.write(m3u)

print("Complete!")
print(f"File created: {file_name}")        {"id": "781", "name": "beIN Sports Max 1"},
        {"id": "782", "name": "beIN Sports Max 2"},
        {"id": "786", "name": "beIN Sports 5"},
        {"id": "763", "name": "S Sport"},
        {"id": "610", "name": "Spor Smart"},
        {"id": "1010", "name": "CBC Sport"},
        {"id": "1020", "name": "İDMAN TV"},
        {"id": "1030", "name": "İCTİMAİ TV"},
        {"id": "69", "name": "TV8,5"},
        {"id": "73", "name": "A Spor"},
        {"id": "74", "name": "HT Spor"},
        {"id": "75", "name": "Tivibu Spor"},
        {"id": "76", "name": "FB TV"},
        {"id": "77", "name": "TRT Spor"},
        {"id": "78", "name": "beIN Sports Haber"},
        {"id": "79", "name": "TRT Spor Yıldız"},
        {"id": "1080", "name": "tabii Spor"},
        {"id": "46", "name": "Ekol Sports"},
        {"id": "631", "name": "Eurosport 1"},
        {"id": "641", "name": "Eurosport 2"},
        {"id": "464", "name": "sportstv"},
        {"id": "608", "name": "NBA TV"}
    ]
    
    m3u_content = '#EXTM3U\n'
    
    for channel in channels:
        m3u8_url = f"https://{pages_dev}/{hash_code}/-/{channel['id']}/playlist.m3u8"
        m3u_content += f'#EXTINF:-1 tvg-logo="https://i.hizliresim.com/ska5t9e.jpg" group-title="BOSS-SPORTS", {channel["name"]}\n'
        m3u_content += f'#EXTVLCOPT:http-referrer={domain}\n'
        m3u_content += f'#EXTVLCOPT:http-origin={domain}\n'
        m3u_content += f'{m3u8_url}\n\n'
    
    return m3u_content

def save_file(content, filename="DeaTHLesss-boss-iptv.m3u"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return filename
    except:
        return None

def main():
    domain = get_active_domain()
    if not domain:
        print("Aktif domain bulunamadı")
        return
    
    iframe_src = get_iframe_src(domain)
    if not iframe_src:
        print("Iframe src bulunamadı")
        return
    
    m3u_content = create_m3u(domain, iframe_src)
    if not m3u_content:
        print("M3U içeriği oluşturulamadı")
        return
    
    saved_path = save_file(m3u_content)
    if saved_path:
        print(f"M3U dosyası oluşturuldu: {saved_path}")
    else:
        print("Dosya kaydedilemedi")

if __name__ == "__main__":
    main()
