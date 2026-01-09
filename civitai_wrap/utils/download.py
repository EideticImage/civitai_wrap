def download_image(url, folder, filename):
    import os, requests

    resp = requests.get(url)
    resp.raise_for_status()

    content_type = resp.headers.get('Content-Type', 'image/png')
    extension = content_type.split('/')[-1] if content_type.split('/') else 'png'

    filename = os.path.join(folder, f"{filename}.{extension}")

    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(filename, "wb") as f:
        f.write(resp.content)

def save_json(data, folder, filename):
    import json, os

    json_data = json.dumps(data)
    with open(os.path.join(folder, f'{filename}.json'), 'wt') as f:
        f.write(json_data)

def read_json(folder, filename):
    import json, os
    with open(os.path.join(folder, f'{filename}.json'), 'rt') as f:
        json_data = f.read()
    return json.loads(json_data)