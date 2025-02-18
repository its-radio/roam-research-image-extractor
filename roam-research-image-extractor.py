#!/bin/env python3

import requests
import argparse
from urllib.parse import urlparse
import re

def tool_error(error_type):
    print(f'Something went wrong.')
    print(f'Error Description: {error_type}')
    print('Please report this to me on github copy-pasting your terminal output into an issue submission.')
    exit()

def is_valid_url(url_string):
    try:
        result = urlparse(url_string)
        # Basic check for scheme and netloc
        valid_scheme_netloc = all([result.scheme, result.netloc])
        
        # Additional regex check for common URL patterns
        regex_pattern = re.compile(
            r'^(?:http|https)://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ipv4
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        url_valid = bool(regex_pattern.match(url_string))
        
        return valid_scheme_netloc and url_valid
    except (ValueError, AttributeError):
        return False

def get_image_urls(filename):
        #  get each line of the roam markdown file
    with open(f'{filename}', 'rt') as file:
        roam_markdown = file.read().split('\n')

    # separate out lines that include images hosted on firebase (roam research's default method)
    lines_with_image_urls = [line.strip() for line in roam_markdown if 'firebasestorage.googleapis.com' in line]
    
    # extract just the image URL from the embeded link
    image_urls = []
    
    for line in lines_with_image_urls:
        begin_url = ''
        url = ''
        for letter in line:
            if begin_url[-4:] != '![](':
                begin_url += letter
            elif letter == ')':
                image_urls.append(url)
            else:
                url += letter

    # check if all lines with images were converted into urls.
    if len(lines_with_image_urls) != len(image_urls):
        tool_error(f'lines_with_image_urls ({len(lines_with_image_urls)}) length mismatch compared to image_urls ({len(image_urls)})')

    # check that we didn't somehow capture something that isn't a url.
    for url in image_urls:
        if not is_valid_url(url):
            tool_error(f'"{url}" is not a valid URL')


    return image_urls

def confirm_download(args, urls):

    # check for confirmation bypass
    if args.yes:
        return True

    # give action summary
    print(f'The provided file, {args.file}, contains {len(urls)} images.')
    print(f'They will be downloaded with names {args.base_name}1.png, {args.base_name}2.png, etc.')
    print(f'They will be downloaded into the current directory. \n')

    # ask for confirmation
    confirm = input('To confirm the above and continue with the download, enter "yes". To exit, enter "no"): ')

    # correct input 3 times, else exit
    count = 0
    while confirm not in ['yes', 'no']:
        confirm = input('To confirm, you must exactly type the letters "yes" or "no": ')
        if count > 2:
            print("Too many incorrect attempts. Exiting...")
            exit()
        count += 1

    if confirm == 'yes':
        return True
    else:
        print('Okay, operation cancelled.')
        exit()

def download_images(base_name, image_urls):
    # Performing the actual downloads

    # spoof a User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i, url in enumerate(image_urls):  # for each extracted URL
        j = i + 1
        response = requests.get(url, headers=headers)  # do a get request
        # check if the request worked
        if response.status_code == 200:
            # if so, save the image
            with open(f'{base_name}{j}.png', 'wb') as file:
                file.write(response.content)
            print(f'Downloading image {j}/{len(image_urls)} as {base_name}{j}.png in the current directory')
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            print(f"Response: {response.text}")


def main():

    # help menu and arg parsing
    parser = argparse.ArgumentParser(description='Extract and download images that you have embeded in roam research pages or graphs')
    parser.add_argument('-f', '--file', help='File you want to extract images from (i.e. the exported roam page)', type=str)  # reference this as args.file
    parser.add_argument('-b', '--base-name', help='Base name for the output files.\n \t"-b name" would result in name-1.png, name-2.png, etc. Default is 1.png, 2.png, etc. ', default='',type=str)
    parser.add_argument('-y', '--yes', help='Bypass confirmations', action='store_true')
    args = parser.parse_args()

    # add a hyphen for basenames
    if args.base_name != '':
        args.base_name += '-'

    # get the image urls
    urls = get_image_urls(args.file)

    # confirm the download
    confirmed = confirm_download(args, urls)

    # double check confirmation and execute the download
    if confirmed:
        download_images(args.base_name, urls)
    else:
        tool_error('Download not confirmed')

if __name__ == '__main__':
    main()