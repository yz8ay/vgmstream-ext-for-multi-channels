import subprocess
import re
import os

#Change here if needed
FILE_EXTENSION = ''
MULTI_CHANNELS_NUMBER = 4

def get_metadata(ext):
    cmd_test = r'for /r %a in (*.' + ext + r') do test.exe -m %a'
    output = subprocess.getoutput(cmd_test)
    return output

def get_channels_number(metadata):
    channel_number = int(re.search(r'(?<=channels: )\d', metadata).group())
    return channel_number

def get_filepath(metadata):
    filepath = re.search(r'(?<=metadata for ).+', metadata).group()
    return filepath

def get_filename(metadata):
    return get_filepath(metadata).split('\\')[-1].split('.')[0]

def make_TXTP(filepath, filename):
    #Change here if needed
    with open(filepath.split('.')[0] + '_TRACK1.txtp', 'w') as txtp:
        txtp.write(filename + '.' + FILE_EXTENSION + ' #C1,2')
    with open(filepath.split('.')[0] + '_TRACK2.txtp', 'w') as txtp:
        txtp.write(filename + '.' + FILE_EXTENSION + ' #C3,4')

def convert(filepath, is_TXTP=False):
    first_cmd = r'test.exe -l 3.0 -o ?f.wav '   # Change here if needed
    if is_TXTP:
        subprocess.call(first_cmd + filepath.split('.')[0] + '_TRACK1.txtp')
        subprocess.call(first_cmd + filepath.split('.')[0] + '_TRACK2.txtp')
    else:
        subprocess.call(first_cmd + filepath)


output = get_metadata(FILE_EXTENSION)
metadata_list = re.findall(r'metadata for.+?play duration.+?\)', output, flags=re.DOTALL)
for metadata in metadata_list:
    filepath = get_filepath(metadata)
    filename = get_filename(metadata)
    channel_number = get_channels_number(metadata)
    print(filename +  ' has ' + str(channel_number) + ' channels')
    if channel_number == MULTI_CHANNELS_NUMBER:
        make_TXTP(filepath, filename)
        convert(filepath, is_TXTP=True)
        os.rename(filepath.split('.')[0] + '_TRACK1.txtp.wav', filepath.split('.')[0] + '_TRACK1.wav')
        os.rename(filepath.split('.')[0] + '_TRACK2.txtp.wav', filepath.split('.')[0] + '_TRACK2.wav')
    else:
        convert(filepath)
        os.rename(filepath.split('.')[0] + '.' + FILE_EXTENSION + '.wav', filepath.split('.')[0] + '.wav')
    print()
