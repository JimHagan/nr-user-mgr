import argparse
import copy
import csv
import logging
import os
import sys

from datetime import datetime
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

global csv_keys
csv_keys = []

root = logging.getLogger()
root.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

handler = logging.FileHandler('nr-user-mgr.log')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)


def validate_user(user_dict):
    logging.debug("validating user {}".format(user_dict['Email']))
    if True:
        return user_dict
    else:
        return None

def load_users_from_file(file_name):
    global csv_keys
    logging.info("Reading users from {}".format(file_name))
    valid_users = []
    with open(file_name, 'r') as user_csv_file:
        reader = csv.DictReader(user_csv_file)
        csv_keys = reader.fieldnames
        for row in reader:
            user_dict = dict(row)
            user = validate_user(user_dict)
            if user:
                valid_users.append(user)
            else:
                raise Exception("User validation error on {}".format(user_dict))
    return(valid_users)

def write_users_to_file(user_list, file_name):
    logging.info("Writing users to {}".format(file_name))
    with open(file_name, 'w')  as output_file:
        dict_writer = csv.DictWriter(output_file, csv_keys + ['change', 'change_reason'])
        dict_writer.writeheader()
        dict_writer.writerows(user_list)

def process_user_list(user_list, config):
    processed_users = []
    if config['force_upgrade_all_users'] and config['force_downgrade_all_users']:
        raise Exception('Invalid configuration: Cannot upgrade and downgrade all users in the same run')

    if config['downgrade_never_active_accounts'] and config['purge_never_active_accounts']:
        raise Exception('downgrade_never_active_accounts and purge_never_active_accounts are mutually exclussive parameters.  Both cannot be set to true.')

    if config['downgrade_pending_accounts'] and config['purge_pending_accounts']:
        raise Exception('downgrade_pending_accounts and purge_pending_accounts are mutually exclussive parameters.  Both cannot be set to true.')

    for user in user_list:
        if user['Last active'] == '' or user['Last active'] == 'Pending':
            user_last_active = None
        else:
            user_last_active = datetime.strptime(user['Last active'], "%b %d, %Y %H:%M:%S %p")

        processed_user = copy.deepcopy(user)
        if config['force_upgrade_all_users']:
            if processed_user['User type'] == 'basic':
                processed_user['User type'] = 'full'
                processed_user['change'] = 'UPGRADE'
                processed_user['change_reason'] = 'FORCE_ALL'
        elif config['force_downgrade_all_users']:
            if processed_user['User type'] == 'full':
                processed_user['User type'] = 'basic'
                processed_user['change'] = 'DOWNGRADE'
                processed_user['change_reason'] = 'FORCE_ALL'
        elif processed_user['Email'] in config['force_purge_user_list']:
            processed_user['User type'] = 'basic' # Prepare for purge
            processed_user['change'] = 'PURGE'
            processed_user['change_reason'] = 'PURGE_LIST'
        elif processed_user['User type'] == 'basic' and processed_user['Email'] in config['force_upgrade_user_list']:
            processed_user['User type'] = 'full'
            processed_user['change'] = 'UPGRADE'
            processed_user['change_reason'] = 'UPGRADE_LIST'
        elif processed_user['User type'] == 'full' and processed_user['Email'] in config['force_downgrade_user_list']:
            processed_user['User type'] = 'basic'
            processed_user['change'] = 'DOWNGRADE'
            processed_user['change_reason'] = 'DOWNGRADE_LIST'
        elif config['purge_never_active_accounts'] and processed_user['Last active'] == '':
            processed_user['User type'] == 'basic'
            processed_user['change'] = 'PURGE'
            processed_user['change_reason'] = 'NEVER_ACTIVE'
        elif config['purge_pending_accounts'] and processed_user['Last active'] == 'Pending':
            processed_user['User type'] == 'basic'
            processed_user['change'] = 'PURGE'
            processed_user['change_reason'] = 'PENDING'
        elif config['downgrade_never_active_accounts'] and processed_user['Last active'] == '':
            processed_user['User type'] == 'basic'
            processed_user['change'] = 'DOWNGRADE'
            processed_user['change_reason'] = 'NEVER_ACTIVE'
        elif config['downgrade_pending_accounts'] and processed_user['Last active'] == 'Pending':
            processed_user['User type'] == 'basic'
            processed_user['change'] = 'DOWNGRADE'
            processed_user['change_reason'] = 'PENDING'
        elif processed_user['User type'] == 'full' and ((datetime.now() - user_last_active).days > config['downgradable_inactivity_days']):
            processed_user['User type'] = 'basic'
            processed_user['change'] = 'DOWNGRADE'
            processed_user['change_reason'] = 'INACTIVE_TIME'           
        else:
            processed_user['change'] = 'NONE'
            processed_user['change_reason'] = 'NO_CRITERIA'
        

        processed_users.append(processed_user)

    return(processed_users)


def main():
    logging.info("starting nr-user-mgr v. 1.0")
    parser = argparse.ArgumentParser(description='nr-user-mgr: Basic user management.')
    parser.add_argument('config', help='config yaml file')
    args = parser.parse_args()
    config_stream = open(args.config, 'r')
    config = load(config_stream, Loader=Loader)
    
    users = load_users_from_file(config['infile'])
    processed_users = process_user_list(users, config)
    
    _modify = []
    _purge = []
    for p in processed_users:
        if p['change'] == 'PURGE':
            _purge.append(p)
        elif p['change'] == 'NONE':
            pass
        else:
            _modify.append(p)


    # Get prefix
    base=os.path.basename(config['infile'])
    prefix=os.path.splitext(base)[0]



    write_users_to_file(_modify, prefix + '-modify.csv')
    write_users_to_file(_purge, prefix + '-purge.csv')

if __name__ == "__main__":
    main()
