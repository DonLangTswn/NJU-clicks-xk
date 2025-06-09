"""
    Providing a set of utility functions for logging messages 
    to the console with different levels of importance
"""
import filelock
import os
import json
from colorama import Fore, Style, init

init(autoreset=True)

def INFO(s, cover=False):
    """ Prints an informational message in blue. 
    If `cover` is True, it overwrites the current line.
    """
    info = f'{Fore.BLUE}[INFO]:  {Style.RESET_ALL}'
    print('\r' + info + s, end='', flush=True) if cover else print(info + s, flush=True)

def DONE(s=''):
    done = f'{Fore.GREEN}[Done]:  {Style.RESET_ALL}'
    print(done + s, flush=True)

def WARN(s):
    warn = f'{Fore.YELLOW}[WARN]:  {Style.RESET_ALL}'
    print(warn + s, flush=True)

def FAIL(s):
    fail = f'{Fore.RED}[Fail]:  {Style.RESET_ALL}'
    print(fail + s, flush=True)

def CONF(s=''):
    conf = f'{Fore.CYAN}[Confirm]:  {Style.RESET_ALL}'
    print(conf + s, flush=True)
    return input()

def read_json(key: str, path = 'config.json'):
    lock_path = path + '.lock'
    lock = filelock.FileLock(lock_path)
    try:
        with lock:
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            try:
                val = data[key]
                return val
            except KeyError:
                FAIL(f'KeyError while reading: key=\"{key}\"')
    except IOError as e:
        FAIL(f'<JSON>: Error while reading: {e}')
        exit()