[![Build Status](https://travis-ci.org/walking-turtle/itheory.svg?branch=master)](https://travis-ci.org/walking-turtle/itheory)

# Information theory project

# Workplace setup

* Add `~/.local/bin` to your `$PATH` just in case

* Install virtualenv if you need to

```sh
λ which virtualenv || pip install --user virtualenv
λ which virtualenv
~/.local/bin/virtualenv
```

* Setup virtual environment

```sh
λ cd /path/to/itheory
λ virtualenv --python=$(which python3) venv
```

* Enable virtual environment each time you want to work on the repository

```sh
λ cd /path/to/itheory
λ source venv/bin/activate
```

* Install the requirements the first time you work on it

```sh
λ pip install -r requirements.txt
```

*Note that* it might be easier to use `virtualenvwrapper` if you are already
used to it.

# Docker image

* Build docker image

```sh
λ cd /path/to/itheory
λ docker build --file Dockerfile_server -t itheory_server .
λ docker build --file Dockerfile_client -t itheory_client .
```

* Run docker image

```sh
λ cp data/text.txt /tmp/text.txt
λ docker run --name itheory_server -d -v /tmp/text.txt:/data.txt -p 8000:8000 itheory_server
λ docker logs itheory_server |& grep '^TOKEN='
TOKEN="xxxxxxxxx"
λ docker run --name itheory_client itheory_client xxxxxxxxx
```
