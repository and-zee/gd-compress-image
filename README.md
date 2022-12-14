# Compress Image

GreatDay Image Compress
JPG/JPEG only

## Run Locally

Install python package dependencies
```bash
  sudo su
  apt install python3.8 python3.8-venv python3.8-pip
``` 

or if you're already have python3 package
```bash
  sudo su
  apt install python3 python3-venv python3-pip
``` 

Go to working directory
```bash
  mkdir -p /opt/app
  cd /opt
```

Clone the project and to the project directory
```bash
  git clone https://github.com/and-zee/gd-compress-image.git app
```

Export env, update python binary alias, and create python3 virtual environment
```bash
  echo "export env='/opt/app/.env'" | tee -a ~/.bashrc
  echo "alias python-3='/opt/env/bin/python3'" | tee -a ~/.bashrc
  echo "alias pip-3='/opt/env/bin/pip3'" | tee -a ~/.bashrc
  python3 -m venv env
  . ~/.bashrc
  . /opt/env/bin/activate
  cd app
```

Install required module
```bash
  pip-3 install -r requirements.txt
```

if you catch some errors try this
```bash
  pip-3 install -r requirements-general.txt
```

Alternatively if you still catch some errors while installing PIL, try folllowing command
```bash
  python-3 -m pip install --upgrade pip
  python-3 -m pip install --upgrade Pillow
```

Test if all module are installed correctly
```bash
  python-3 main.py --test
```

Update .env
- set `REPLACE` to `True`  : to replace all files while compressing image
- set `REPLACE` to `False` : compressed image will be created into a new file
- set `DESTINATION_DIR` to where commpressed image will be place, this directory will be used when `REPLACE` is set to `FALSE`
- set `SOURCE_DIR` to where image will be load

Start the program
```bash
python-3 main.py
```
