# Compress Image

GreatDay Image Compress

## Run Locally

Install python package dependencies
```bash
  sudo su
  apt install python3.8 python3.8-venv
``` 

Go to working directory
```bash
  mkdir -p /opt/app
  cd /opt
```

Create python3 virtual environment
```bash
  python3 -m venv env
  . env/bin/activate
```

Clone the project and to the project directory
```bash
  git clone https://github.com/and-zee/gd-compress-image.git app && cd app
```

Export env and update python
```bash
  echo "export env='/opt/app/.env'" | tee -a ~/.bashrc
  echo "export python3='/opt/env/bin/python3'" | tee -a ~/.bashrc
  echo "export pip3='/opt/env/bin/pip3'" | tee -a ~/.bashrc
  . ~/.bashrc
```

Install required module
```bash
  pip3 install -r requirements.txt
```

Test if all module are installed correctly
```bash
  python3 main.py --test
```

Update .env
- set `REPLACE` to `True`  : to replace all files while compressing image
- set `REPLACE` to `False` : compressed image will be created into a new file
- set `DESTINATION_DIR` to where commpressed image will be place, this directory will be used when `REPLACE` is set to `FALSE`
- set `SOURCE_DIR` to where image will be load

Start the program
```bash
pyrhon3 main.py
```
