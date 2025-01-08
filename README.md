# Heisse Preise Data

## Project Overview
This project provides compressed datasets derived from [heisse-preise.io](https://github.com/badlogic/heissepreise), offering an easy and efficient way to access up-to-date pricing data from supermarkets in Austria.

### Data Sources
The data originates from:
- [heisse-preise.io](https://github.com/badlogic/heissepreise)
- [h43z](https://h.43z.one)
- [Dossier: Anatomie eines Supermarkts - Die Methodik](https://www.dossier.at/dossiers/supermaerkte/quellen/anatomie-eines-supermarkts-die-methodik/)

### Build Process
- The dataset is built daily to ensure the latest pricing data is available.
- The most recent build can be downloaded from the following link:
  `https://github.com/falknerdominik/heisse-preise-data/releases/latest/download/latest-canonical.tar.gz`

## Usage Examples

### Download and Extract Data

#### Python Example
```python
import requests
import tarfile
import io
import json

url = 'https://github.com/falknerdominik/heisse-preise-data/releases/latest/download/latest-canonical.tar.gz'
response = requests.get(url)

if response.status_code == 200:
    tar = tarfile.open(fileobj=io.BytesIO(response.content), mode='r:gz')
    for member in tar.getmembers():
        if member.name.endswith('.json'):
            f = tar.extractfile(member)
            data = json.load(f)
            print(json.dumps(data, indent=2))
else:
    print("Failed to download the data.")
```

#### JavaScript Example (Node.js)
```javascript
import requests
import tarfile
import io
import json

url = 'https://github.com/falknerdominik/heisse-preise-data/releases/latest/download/latest-canonical.tar.gz'
json_filename = 'latest-canonical.json'

try:
    # Download the tar.gz file into memory
    response = requests.get(url)
    response.raise_for_status()

    # Open the tar.gz file directly from memory
    with tarfile.open(fileobj=io.BytesIO(response.content), mode='r:gz') as tar:
        # Extract and read the JSON file directly from the tar archive
        json_file = tar.extractfile(json_filename)
        if json_file:
            json_data = json.load(json_file)
            print(json.dumps(json_data, indent=2))
        else:
            print(f"{json_filename} not found in the archive.")

except requests.RequestException as e:
    print(f"Error downloading data: {e}")
except (tarfile.TarError, json.JSONDecodeError) as e:
    print(f"Error processing files: {e}")
```

## Contributing
If you wish to contribute or improve the project, feel free to open an issue or submit a pull request.

## License
This project is licensed under the terms provided by the original data sources.

