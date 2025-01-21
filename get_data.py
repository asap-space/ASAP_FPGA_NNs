import os
import sys
import requests
import pandas as pd


def download_file(url, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filename, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")


def read_and_download(csv_file, base_url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        file_url = f"{base_url}?file={row['file']}"
        filename = os.path.join(dest_folder, row["file"])
        if not os.path.exists(filename):
            download_file(file_url, filename)
        else:
            print(f"File {filename} already exists, skipping download.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python get_data.py <csv_file> <base_url> <dest_folder>")
        sys.exit(1)

    csv_file = sys.argv[1]
    base_url = sys.argv[2]
    dest_folder = sys.argv[3]

    read_and_download(csv_file, base_url, dest_folder)
