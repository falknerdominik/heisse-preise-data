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
    console.error(`Error downloading data: ${err.message}`);
});
```

## Contributing
If you wish to contribute or improve the project, feel free to open an issue or submit a pull request.

## License
This project is licensed under the terms provided by the original data sources.

