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

# Python app

* Run python app

```sh
λ cd /path/to/itheory
λ ./src/main.py
```

# Docker image

* Build docker image

```sh
λ cd /path/to/itheory
λ docker build -t itheory .
```

* Run docker image

```sh
λ docker run --rm itheory
```
