[![Build Status](https://travis-ci.org/pierscin/pollution-globe.svg?branch=master)](https://travis-ci.org/pierscin/pollution-globe)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/pierscin/pollution-globe/master/LICENSE)

# Pollution globe

### [How it looks](https://cdn.rawgit.com/pierscin/pollution-globe/6c7ca946/globe.png)

Pollution globe visualizes air quality around the world using
[WebGL Globe](https://experiments.withgoogle.com/chrome/globe) and data from
[aqicn](http://aqicn.org/).


## Quick setup

Create virtual environment in cloned/downloaded repository and install required packages.

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Run app.

```
python runner.py
```


Open `localhost:5000` in your browser.


<p align='center'>
<img src='https://cdn.rawgit.com/pierscin/pollution-globe/57fe0853/term.gif' alt='setup and run'>
</p>
