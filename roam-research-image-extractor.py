#!/bin/env python3

import requests
import argparse
from urllib.parse import urlparse
import re
import os

def tool_error(error_type):
    # Print error message and exit
    print("Something went wrong.")
    print(f"Error Description: {error_type}")
    print("Please report this to me on github copy-pasting your terminal output into an issue submission.")
    exit()

def is_valid_url(url_string):
    try:
        # Parse the URL
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
        
        # Check if the URL matches the regex pattern
        url_valid = bool(regex_pattern.match(url_string))
        
        # Return True if the URL is valid, False otherwise
        return valid_scheme_netloc and url_valid
    except (ValueError, AttributeError):
        # If there's an error, return False
        return False

def get_image_urls(filename):
    
    # basic file checks
    if not os.path.exists(filename):
        print(f'{filename} does not exist. Exiting...')
        exit()
    elif not filename.endswith('.md'):
        print(f'{filename} is not a markdown file. Exiting...')
        exit()


    # Open the file and read its contents
    with open(f'{filename}', 'rt') as file:
        roam_markdown = file.read().split('\n')

    # Separate out lines that include images hosted on firebase (roam research's default method)
    lines_with_image_urls = [line.strip() for line in roam_markdown if 'firebasestorage.googleapis.com' in line]
    
    # Initialize an empty list to store the image URLs
    image_urls = []
    
    # Iterate over the lines with image URLs
    for line in lines_with_image_urls:
        # Initialize an empty string to build the URL
        url = ''
        match_syntax = ''
        # Iterate over the characters in the line
        for letter in line:
            # If the URL hasn't started yet, keep adding characters
            if not match_syntax.endswith('![]('):
                match_syntax += letter
            # If the URL has ended, add it to the list and reset the URL
            elif letter == ')':
                image_urls.append(url)
            # If the URL is still being built, add the character
            else:
                url += letter

    # Check if all lines with images were converted into URLs
    if len(lines_with_image_urls) != len(image_urls):
        tool_error(f'lines_with_image_urls ({len(lines_with_image_urls)}) length mismatch compared to image_urls ({len(image_urls)})')

    # Check that we didn't somehow capture something that isn't a URL
    for url in image_urls:
        if not is_valid_url(url):
            tool_error(f'"{url}" is not a valid URL')

    # Return the list of image URLs
    return image_urls

def confirm_download(args, urls):
    # Check for confirmation bypass
    if args.yes:
        return True

    # Give action summary
    print(f'The provided file, {args.file}, contains {len(urls)} images.')
    print(f'They will be downloaded with names {args.base_name}1.png, {args.base_name}2.png, etc.')
    print(f'They will be downloaded into the current directory. \n')

    # Ask for confirmation
    confirm = input('Would you like to continue with the download? y/n: ')

    # Correct input 3 times, else exit
    count = 0
    while confirm not in ['yes', 'no', 'y', 'n']:
        confirm = input('To confirm or exit, enter "y" or "n": ')
        if count > 2:
            print("Too many incorrect attempts. Exiting...")
            exit()
        count += 1

    # Return True if confirmed, False otherwise
    if confirm in ['y', 'yes']:
        return True
    else:
        print('Okay, operation cancelled.')
        exit()

def download_images(args, image_urls):
    # Spoof a User-Agent
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Iterate over the image URLs
    for i, url in enumerate(image_urls):
        # Get the image number
        j = i + 1
        # Define the new filename
        filename = f'{args.base_name}{j}.png'

        # Check if that file already exists
        if os.path.exists(filename) and not args.yes:
            print(f'A file already exists with name {filename}. To skip all prompts like this one, rerun the command with -y. Ctrl + c to exit.')
            overwrite = input(f'Would you like to overwrite just {filename}? y/n: ')

            # prompt for correct input 3 times, else proceed without overwriting the file
            count = 0
            while overwrite not in ['yes', 'no', 'y', 'n']:
                overwrite = input(f'To choose whether or not to overwrite {filename}, enter "y" or "n": ')
                if count > 2:
                    print(f'Too many incorrent inputs. Proceeding without overwriting f{filename}')
                    overwrite = False
                    break
                count += 1    

            if overwrite in ['y', 'yes']:
                print(f'Overwriting {filename}')
            elif overwrite in ['n', 'no', False]:
                print(f'Skipping {filename}')
                continue

        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        # Check if the request worked
        if response.status_code == 200:
            # If so, save the image
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'Downloading image {j}/{len(image_urls)} as {filename} in the current directory')
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            print(f"Response: {response.text}")

def main():
    # Help menu and arg parsing
    parser = argparse.ArgumentParser(description='Extract and download images that you have embeded in roam research pages or graphs')
    parser.add_argument('-f', '--file', help='File you want to extract images from (i.e. the exported roam page)', type=str)
    parser.add_argument('-b', '--base-name', help='Base name for the output files.\n \t"-b name" would result in name-1.png, name-2.png, etc. Default is 1.png, 2.png, etc. ', default='', type=str)
    parser.add_argument('-y', '--yes', help='Bypass confirmations', action='store_true')
    args = parser.parse_args()

    # Add a hyphen for basenames
    if args.base_name:
        args.base_name += '-'

    # Get the image URLs
    urls = get_image_urls(args.file)

    # Confirm the download
    confirmed = confirm_download(args, urls)

    # Double check confirmation and execute the download
    if confirmed:
        download_images(args, urls)
    else:
        tool_error('Download not confirmed')

if __name__ == '__main__':
    main()