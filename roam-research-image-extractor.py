#!/bin/env python3

import requests

roam_markdown = open('latus (sherlock).md', 'rt').read().split('\n')

lines_with_image_urls = [line.strip() for line in roam_markdown if 'firebasestorage' in line]

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

if len(lines_with_image_urls) != len(image_urls):
    print('error: lengths dont match')
    exit()


# see if they want to download the images

really_download = 'no'
count = 1

while really_download != 'yes':
    really_download = input(f'This roam page contains {len(image_urls)} images. If you continue, they will be downloaded to the current directory. Do you want to continue? yes/no: ')
    count += 1
    if count > 0:
        print('You must type the entire word "yes" to continue')
    if count > 3:
        print('Sorry, run the program from the start to try agaih. Exiting...')
        exit()




# Performing the downloads

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

for i, url in enumerate(image_urls):
    # do the request
    response = requests.get(url, headers=headers)
    # check if the request worked
    if response.status_code == 200:
        # save the image
        with open(f'{i}.png', 'wb') as file:
            file.write(response.content)
        print(f'Image saved as {i}.png in the current directory')
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        print(f"Response: {response.text}")

