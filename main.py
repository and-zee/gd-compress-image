# import required libraries
import os
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path
import argparse
import math
import logging
from pathlib import Path
import time
import sys

def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def compressImg(src_file, destpath, filename):
    picture = Image.open(src_file)
    picture_rgb = picture.convert('RGB')
    img_size = os.path.getsize(src_file)
        
    file_compressed = destpath+"/"+filename
    picture_rgb.save(file_compressed,
                    optimize = True,
                    quality = 'low')
                    # quality = 18)
    new_img_size = os.path.getsize(file_compressed)
    return img_size, new_img_size

def compressReplaceImg(src_file):
    picture = Image.open(src_file)
    picture_rgb = picture.convert('RGB')
    img_size = os.path.getsize(src_file)
        
    picture_rgb.save(src_file,
                    optimize = True,
                    quality = 'low')
                    # quality = 18)
    new_img_size = os.path.getsize(src_file)
    return img_size, new_img_size

# Define a main function
def main(_basepath, debugcopy=False, debugreplace=False, copyAll=False, replaceAll=False, copyAcc=False, replaceAcc=False):
    st = time.time()
    if debugcopy:
        formats = ('.jpg', '.jpeg')
        parent_dir=os.path.abspath(os.path.join(_basepath, os.pardir))
        compressed_dir="_compressed"
        basename=os.path.basename(_basepath)
        destname = basename+compressed_dir
        destpath = os.path.join(parent_dir, destname)
        if not os.path.exists(destpath): os.mkdir(destpath)
        
        log_file = Path(str(destpath)+'/_process.log')
        if not os.path.exists(log_file): log_file.touch(exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        log_handler = logging.FileHandler(log_file)
        log_handler.setLevel(logging.INFO)
        log_handler_format = '%(asctime)s : %(message)s'
        log_handler.setFormatter(logging.Formatter(log_handler_format))
        logger.addHandler(log_handler) 
        
        for file in os.listdir(_basepath):
            filepath=str(_basepath)+"/"+file
            if os.path.splitext(file)[1].lower() in formats:
                logger.info("Compressing "+str(file))
                img_size, new_img_size = compressImg(filepath, destpath, file)
                saving_diff = new_img_size - img_size
                logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
            else: logger.error("Unsupported file format")
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
    elif debugreplace:
        formats = ('.jpg', '.jpeg')
        
        log_file = Path(str(_basepath)+'/_process.log')
        if not os.path.exists(log_file): log_file.touch(exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        log_handler = logging.FileHandler(log_file)
        log_handler.setLevel(logging.INFO)
        log_handler_format = '%(asctime)s : %(message)s'
        log_handler.setFormatter(logging.Formatter(log_handler_format))
        logger.addHandler(log_handler)
        
        for file in os.listdir(_basepath):
            filepath=str(_basepath)+"/"+file
            basefilename=os.path.basename(filepath)
            if basefilename == "_process.log": continue
            if os.path.splitext(file)[1].lower() in formats:
                logger.info("Compressing "+str(file))
                img_size, new_img_size = compressReplaceImg(filepath)
                saving_diff = new_img_size - img_size
                logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
            else: logger.error("Unsupported file format")
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
    elif replaceAcc: 
        formats = ('.jpg', '.jpeg')
        dotenv_path = Path(str(os.environ["env"]))
        load_dotenv(dotenv_path=dotenv_path)
        base_dir=str(os.getenv('SRC_ACCOUNT_DIR'))
        
        log_file = Path(str(base_dir)+'/_process.log')
        if not os.path.exists(log_file): log_file.touch(exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        log_handler = logging.FileHandler(log_file)
        log_handler.setLevel(logging.INFO)
        log_handler_format = '%(asctime)s : %(message)s'
        log_handler.setFormatter(logging.Formatter(log_handler_format))
        logger.addHandler(log_handler)
        
        account_dir=base_dir
        
        for month in os.listdir(str(account_dir)):
            # Loop through all days
            days = str(account_dir)+"/"+month
            basefilename=os.path.basename(days)
            if basefilename == "_process.log": continue
            for day in os.listdir(days):
                # Loop through all hours
                hours = str(days)+"/"+day
                for hour in os.listdir(hours):
                    # Loop through all files
                    src_dir=str(hours)+"/"+hour
                    for file in os.listdir(src_dir):
                        filepath=str(src_dir)+"/"+file
                        if os.path.splitext(file)[1].lower() in formats:
                            logger.info("Compressing "+str(file))
                            img_size, new_img_size = compressReplaceImg(filepath)
                            saving_diff = new_img_size - img_size
                            logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                            logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                            logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
                        else: logger.error("Unsupported file format")
        logger.info("Compressed directory : {}".format(account_dir))
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
    elif replaceAll: 
        formats = ('.jpg', '.jpeg')
        dotenv_path = Path(str(os.environ["env"]))
        load_dotenv(dotenv_path=dotenv_path)
        base_dir=str(os.getenv('SOURCE_DIR'))
        
        # Loop though all account
        for account in os.listdir(str(base_dir)):
            # Loop through all years and month
            account_dir=base_dir+"/"+str(account)
            
            log_file = Path(str(account_dir)+'/_process.log')
            if not os.path.exists(log_file): log_file.touch(exist_ok=True)
            
            logger = logging.getLogger()
            logger.setLevel(logging.NOTSET)
            log_handler = logging.FileHandler(log_file)
            log_handler.setLevel(logging.INFO)
            log_handler_format = '%(asctime)s : %(message)s'
            log_handler.setFormatter(logging.Formatter(log_handler_format))
            logger.addHandler(log_handler)
            
            for month in os.listdir(str(account_dir)):
                # Loop through all days
                days = str(account_dir)+"/"+month
                basefilename=os.path.basename(days)
                if basefilename == "_process.log": continue
                for day in os.listdir(days):
                    # Loop through all hours
                    hours = str(days)+"/"+day
                    for hour in os.listdir(hours):
                        # Loop through all files
                        src_dir=str(hours)+"/"+hour
                        for file in os.listdir(src_dir):
                            filepath=str(src_dir)+"/"+file
                            if os.path.splitext(file)[1].lower() in formats:
                                logger.info("Compressing "+str(file))
                                img_size, new_img_size = compressReplaceImg(filepath)
                                saving_diff = new_img_size - img_size
                                logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                                logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                                logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
                            else: logger.error("Unsupported file format")
            logger.info("Compressed directory : {}".format(account_dir))
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
    elif copyAcc: 
        formats = ('.jpg', '.jpeg')
        dotenv_path = Path(str(os.environ["env"]))
        load_dotenv(dotenv_path=dotenv_path)
        base_dir=str(os.getenv('SRC_ACCOUNT_DIR'))
        dest_dir=str(os.getenv('DEST_ACCOUNT_DIR'))
        if not dest_dir: # Variable defined but with no value
            parent_dir=os.path.abspath(os.path.join(base_dir, os.pardir))
            dest_dir=parent_dir+"/compressed"
        elif dest_dir == "None": # No variable defined on .env
            parent_dir=os.path.abspath(os.path.join(base_dir, os.pardir))
            dest_dir=parent_dir+"/compressed"
        else:  # Variable defined with its value
            if not os.path.exists(dest_dir): os.mkdir(dest_dir)
            
        account_dir=base_dir
        destname=os.path.basename(base_dir)
        account_dir_compressed = os.path.join(dest_dir, destname)
        if not os.path.exists(account_dir_compressed): os.mkdir(account_dir_compressed)
        log_file = Path(str(account_dir_compressed)+'/_process.log')
        if not os.path.exists(log_file): log_file.touch(exist_ok=True)
        logger = logging.getLogger()
        logger.setLevel(logging.NOTSET)
        log_handler = logging.FileHandler(log_file)
        log_handler.setLevel(logging.INFO)
        log_handler_format = '%(asctime)s : %(message)s'
        log_handler.setFormatter(logging.Formatter(log_handler_format))
        logger.addHandler(log_handler)
        
        for month in os.listdir(str(account_dir)):
            # Loop through all days
            days = str(account_dir)+"/"+month
            days_compressed = str(account_dir_compressed)+"/"+month
            if not os.path.exists(days_compressed): os.mkdir(days_compressed)
            for day in os.listdir(days):
                # Loop through all hours
                hours = str(days)+"/"+day
                hours_compressed = str(days_compressed)+"/"+day
                if not os.path.exists(hours_compressed): os.mkdir(hours_compressed)
                for hour in os.listdir(hours):
                    # Loop through all files
                    src_dir=str(hours)+"/"+hour
                    dest_dir_compressed = str(hours_compressed)+"/"+hour
                    if not os.path.exists(dest_dir_compressed): os.mkdir(dest_dir_compressed)
                    for file in os.listdir(src_dir):
                        filepath=str(src_dir)+"/"+file
                        if os.path.splitext(file)[1].lower() in formats:
                            logger.info("Compressing "+str(file))
                            img_size, new_img_size = compressImg(filepath, dest_dir_compressed, file)
                            saving_diff = new_img_size - img_size
                            logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                            logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                            logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
                        else: logger.error("Unsupported file format")
        logger.info("Compressed directory : {}".format(account_dir_compressed))
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
    elif copyAll:
        formats = ('.jpg', '.jpeg')
        dotenv_path = Path(str(os.environ["env"]))
        load_dotenv(dotenv_path=dotenv_path)
        base_dir=str(os.getenv('SOURCE_DIR'))
        dest_dir=str(os.getenv('DESTINATION_DIR'))
        if not dest_dir: # Variable defined but with no value
            parent_dir=os.path.abspath(os.path.join(base_dir, os.pardir))
            dest_dir=parent_dir+"/compressed"
        elif dest_dir == "None": # No variable defined on .env
            parent_dir=os.path.abspath(os.path.join(base_dir, os.pardir))
            dest_dir=parent_dir+"/compressed"
        else:  # Variable defined with its value
            if not os.path.exists(dest_dir): os.mkdir(dest_dir)
        
        # Loop though all account
        for account in os.listdir(str(base_dir)):
            # Loop through all years and month
            account_dir=base_dir+"/"+str(account)
            destname = account
            
            account_dir_compressed = os.path.join(dest_dir, destname)
            if not os.path.exists(account_dir_compressed): os.mkdir(account_dir_compressed)
            log_file = Path(str(account_dir_compressed)+'/_process.log')
            if not os.path.exists(log_file): log_file.touch(exist_ok=True)
            
            logger = logging.getLogger()
            logger.setLevel(logging.NOTSET)
            log_handler = logging.FileHandler(log_file)
            log_handler.setLevel(logging.INFO)
            log_handler_format = '%(asctime)s : %(message)s'
            log_handler.setFormatter(logging.Formatter(log_handler_format))
            logger.addHandler(log_handler)
            
            for month in os.listdir(str(account_dir)):
                # Loop through all days
                days = str(account_dir)+"/"+month
                days_compressed = str(account_dir_compressed)+"/"+month
                if not os.path.exists(days_compressed): os.mkdir(days_compressed)
                for day in os.listdir(days):
                    # Loop through all hours
                    hours = str(days)+"/"+day
                    hours_compressed = str(days_compressed)+"/"+day
                    if not os.path.exists(hours_compressed): os.mkdir(hours_compressed)
                    for hour in os.listdir(hours):
                        # Loop through all files
                        src_dir=str(hours)+"/"+hour
                        dest_dir_compressed = str(hours_compressed)+"/"+hour
                        if not os.path.exists(dest_dir_compressed): os.mkdir(dest_dir_compressed)
                        for file in os.listdir(src_dir):
                            filepath=str(src_dir)+"/"+file
                            if os.path.splitext(file)[1].lower() in formats:
                                logger.info("Compressing "+str(file))
                                img_size, new_img_size = compressImg(filepath, dest_dir_compressed, file)
                                saving_diff = new_img_size - img_size
                                logger.info("[+] Original image size: {}".format(convert_size(img_size)))
                                logger.info("[+] Compressed image size: {}".format(convert_size(new_img_size)))
                                logger.info(f"[+] Image size change: {saving_diff/img_size*100:.2f}% of the original image size.")
                            else: logger.error("Unsupported file format")
            logger.info("Compressed directory : {}".format(account_dir_compressed))
        logger.info("Done")
        elapsed_time = time.time() - st
        logger.info("Execution time : "+str(time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))

def checkParam():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    parser.add_argument('--test', default=False, action='store_true')
    debug = subparser.add_parser('copy')
    debugreplace = subparser.add_parser('replace')
    debug.add_argument('--path', type=str, required=True)
    debugreplace.add_argument('--path', type=str, required=True)
    
    args = parser.parse_args()
    basepath=""
    _debugcopy=False
    _debugreplace=False
    _test=False
    
    if args.test: _test=True
    
    if args.command == 'copy':
        _debugcopy=True
        basepath=args.path
    elif args.command == 'replace':
        _debugreplace=True
        basepath=args.path
    
    return _debugcopy, _debugreplace, basepath, _test

def init():
    _debugcopy, _debugreplace, _basepath, test = checkParam()
    if test:
        from PIL import Image
        from dotenv import load_dotenv
        dotenv_path = Path(str(os.environ["env"]))
        load_dotenv(dotenv_path=dotenv_path)
        _test=str(os.getenv('TEST'))
        if not _test and _test == "None": print("No variable loaded")
        else:
            print("[-] :", _test)
            print("variable loaded from env")
        sys.exit()
    
    from dotenv import load_dotenv
    dotenv_path = Path(str(os.environ["env"]))
    load_dotenv(dotenv_path=dotenv_path)
    is_replace_all=str(os.getenv('REPLACE_ALL'))
    is_copy_all=str(os.getenv('COPY_ALL'))
    is_replace_acc=str(os.getenv('REPLACE'))
    is_copy_acc=str(os.getenv('COPY'))
    
    if is_replace_acc == "True" or is_replace_acc == "true": _replaceAcc=True   # Variable defined with its value
    elif is_replace_acc == "None": _replaceAcc=False                            # No variable defined on .env
    else: _replaceAcc=False                                                     # Variable defined but with no value or with value False
    
    if is_copy_acc == "True" or is_copy_acc == "true": _copyAcc=True            # Variable defined with its value
    elif is_copy_acc == "None": _copyAcc=False                                  # No variable defined on .env
    else: _copyAcc=False                                                        # Variable defined but with no value or with value False
    
    if is_replace_all == "True" or is_replace_all == "true": _replaceAll=True   # Variable defined with its value
    elif is_replace_all == "None": _replaceAll=False                            # No variable defined on .env
    else: _replaceAll=False                                                     # Variable defined but with no value or with value False
    
    if is_copy_all == "True" or is_copy_all == "true": _copyAll=True            # Variable defined with its value
    elif is_copy_all == "None": _copyAll=False                                  # No variable defined on .env
    else: _copyAll=False                                                        # Variable defined but with no value or with value False
    
    main(_basepath=str(_basepath), debugcopy=_debugcopy, debugreplace=_debugreplace, copyAll=_copyAll, replaceAll=_replaceAll, copyAcc=_copyAcc, replaceAcc=_replaceAcc)

# Driver code
if __name__ == "__main__":
    init()
