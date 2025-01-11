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

#### Python Package

- No dependencies
- Minimal python version should be 3.6
- Package: https://pypi.org/project/heisse-preise-data

```
pip install heisse-preise-data
```

```python
from heisse_preise_data import download

try:
    raw = download()
    print(json.dumps(raw, indent=2))
except RuntimeError as e:
    print(f"An error occurred: {e}")

```

```python
from heisse_preise_data import download
import pandas as pd

try:
    data = pd.DataFrame(download())
    data.head(5)
except RuntimeError as e:
    print(f"An error occurred: {e}")
```

#### Python Example
```python
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

#### JavaScript Example (Node.js)
```javascript
const https = require('https');
const fs = require('fs');
const tar = require('tar');

const url = 'https://github.com/falknerdominik/heisse-preise-data/releases/latest/download/latest-canonical.tar.gz';

https.get(url, (response) => {
    const file = fs.createWriteStream('latest-canonical.tar.gz');
    response.pipe(file);
    file.on('finish', () => {
        file.close();
        tar.x({ file: 'latest-canonical.tar.gz' }).then(() => {
            fs.readFile('latest-canonical.json', (err, data) => {
                if (err) throw err;
                const jsonData = JSON.parse(data);
                console.log(JSON.stringify(jsonData, null, 2));
            });
        });
    });
}).on('error', (err) => {
    console.error(Error downloading data: ${err.message});
});
```

## Contributing
If you wish to contribute or improve the project, feel free to open an issue or submit a pull request.

## Build

```sh
python -m build
```

## License
This project is licensed under the terms provided by the original data sources.

