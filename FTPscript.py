#FTP script python

#first install "pip install argparse"

import ftplib
import os
import schedule
import time
import logging
import argparse

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_file(ftp_server, filename, local_path, local_filename):
    try:
        ftp = ftplib.FTP(ftp_server)
        ftp.login()  # Add credentials here if required: ftp.login('username', 'password')
        with open(os.path.join(local_path, local_filename), 'wb') as file:
            ftp.retrbinary(f'RETR {filename}', file.write)
        ftp.quit()
        logging.info(f"Successfully downloaded {filename} from {ftp_server}")
    except Exception as e:
        logging.error(f"Failed to download from {ftp_server}: {e}")

def main(servers, local_path, download_schedule=None):
    filename = 'filtered.log'
    
    for i, server in enumerate(servers):
        local_filename = f"{server.replace('.', '_')}_filtered.log"
        if download_schedule:
            schedule.every().day.at(download_schedule).do(download_file, ftp_server=server, filename=filename, local_path=local_path, local_filename=local_filename)
        else:
            download_file(ftp_server=server, filename=filename, local_path=local_path, local_filename=local_filename)

    if download_schedule:
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FTP Download Script")
    parser.add_argument('--servers', nargs='+', help='List of FTP servers', required=True)
    parser.add_argument('--path', type=str, help='Local path for saving files', required=True)
    parser.add_argument('--schedule', type=str, help='Schedule time for daily download, e.g., "10:00"')
    args = parser.parse_args()

    main(servers=args.servers, local_path=args.path, download_schedule=args.schedule)

#to run once, cmd the below line without quotes/# and fill in IP
#python script.py --servers 192.168.1.1 192.168.1.2 --path /path/to/your/local/folder

#to run on schedule, cmd the below line without quotes/# and fill in IP
#python script.py --servers 192.168.1.1 192.168.1.2 --path /path/to/your/local/folder --schedule 10:00
