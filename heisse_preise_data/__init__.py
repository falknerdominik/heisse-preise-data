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
        ValueError: If the JSON file is not found in the archive.
        urllib.error.URLError: If there is an error during the download.
        json.JSONDecodeError: If there is an error decoding the JSON data.
    """
    try:
        # Download the tar.gz file into memory
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise urllib.error.URLError(f"Failed to download file. HTTP Status: {response.status}")

            # Read and decompress the gzip data
            compressed_data = response.read()
            decompressed_data = gzip.decompress(compressed_data)

            # Parse the tar structure manually
            buffer = BytesIO(decompressed_data)
            while True:
                header = buffer.read(512)
                if len(header) < 512:
                    break

                # Get the file name from the header
                name = header[:100].decode("utf-8").strip("\x00")

                # Get the file size from the header
                size_field = header[124:136].decode("utf-8").strip("\x00").strip()
                try:
                    size = int(size_field, 8)
                except ValueError:
                    raise ValueError(f"Invalid size field in tar header: {size_field}")

                # Check if the current file is the JSON file
                json_filename = 'latest-canonical.json'
                if name == json_filename:
                    json_data = buffer.read(size)
                    return json.loads(json_data)

                # Move to the next file in the tar structure
                buffer.seek((size + 511) // 512 * 512, 1)

            raise ValueError(f"{json_filename} not found in the archive.")

    except urllib.error.URLError as e:
        raise RuntimeError(f'Encounter a problem downloading the data from {url}') from e
    except (ValueError, json.JSONDecodeError) as e:
        raise RuntimeError('Encounter a problem parsing the JSON') from e
