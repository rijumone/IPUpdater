import os
import time
import subprocess
from loguru import logger
# from git import Repo

import configparser
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini'))
logger.add(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.log'), rotation="10 MB", retention="10 days")

def main():
    logger.debug('fetch external IP')
    ip = subprocess.check_output(['curl', 'icanhazip.com']).decode().strip()
    # print(ip)
    logger.debug('checking IP on remote path')
    remote_location_ip = subprocess.check_output(['curl', config['REMOTE_IP']['URL_PREFIX'] + config['REMOTE_IP']['NODE_FILE']]).decode().strip()
    if '.' in remote_location_ip:
        # remote_location_ip = remote_location_ip.split('IP: ')[1].split(' ')[0]
        if remote_location_ip == ip:
            logger.info('IP updated to remote location is same as current external IP')
            return
        else:
            upload_ip(ip)    
    else:
        logger.info('IP not updated to remote location')
        upload_ip(ip)
    
def upload_ip(ip):
    logger.info('updating IP to remote location')
    with open(os.path.join(config['LOCAL_REPO']['PATH'], config['LOCAL_REPO']['NODE_FILE']), 'w') as out:
        out.write(ip)
    # subprocess.run(['cd', config['LOCAL_REPO']['PATH']])
    subprocess.run(['git', 'add', os.path.join(config['LOCAL_REPO']['PATH'], config['LOCAL_REPO']['NODE_FILE'])], cwd=config['LOCAL_REPO']['PATH'])
    subprocess.run(['git', 'commit', '-m', 'updating external IP at {}'.format(int(time.time()))], cwd=config['LOCAL_REPO']['PATH'])
    subprocess.run(['git', 'push', '-v', ], cwd=config['LOCAL_REPO']['PATH'])

if __name__ == '__main__':
    main()
