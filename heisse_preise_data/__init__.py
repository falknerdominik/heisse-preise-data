import gzip
import json
import urllib.request
from io import BytesIO

LATEST_DOWNLOAD_URL = 'https://github.com/falknerdominik/heisse-preise-data/releases/latest/download/latest-canonical.tar.gz'

def download(url: str = LATEST_DOWNLOAD_URL) -> dict:
    """
    Downloads a tar.gz file from the given URL, extracts a JSON file,
    and returns the parsed JSON data as a Python dictionary.

    Args:
        url (str): The URL to the tar.gz file.

    Returns:
        dict: Parsed JSON data.

    Raises:
        RuntimeError: If the JSON file is not found in the archive.
        RuntimeError: If there is an error during the download.
        RuntimeError: If there is an error decoding the JSON data.
    """
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.URLError(f"Failed to download file. HTTP Status: {response.status}")

            # decompress the gzip data
            compressed_data = response.read()
            decompressed_data = gzip.decompress(compressed_data)

            # parse the tar structure manually - avoids dependecy
            buffer = BytesIO(decompressed_data)
            header = buffer.read(512)
            if len(header) < 512:
                ValueError("Invalid tar file: missing header")

            # get the file name from the header
            name = header[:100].decode("utf-8").strip("\x00")

            # get the file size from the header
            size_field = header[124:136].decode("utf-8").strip("\x00").strip()
            try:
                size = int(size_field, 8)
            except ValueError:
                raise ValueError(f"Invalid size field in tar header: {size_field}")

            # check if the current file is the JSON file
            json_filename = 'latest-canonical.json'
            if name == json_filename:
                json_data = buffer.read(size)
                return json.loads(json_data)

            raise ValueError(f"{json_filename} not found, at the first data block, in the tar archive.")

    except urllib.error.URLError as e:
        raise RuntimeError(f'Encounter a problem downloading the data from {url}') from e
    except ValueError as e:
        raise RuntimeError('Encounter a problem parsing the tar structure') from e
    except json.JSONDecodeError as e:
        raise RuntimeError('Encounter a problem parsing the JSON') from e