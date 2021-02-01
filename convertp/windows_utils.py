from easygui import fileopenbox
import os


def get_pcap_file_windows():
    file_path = fileopenbox(msg="Please choose pcap to convert", default=os.path.join(os.getcwd(), '*.pcapng'))
    if not (file_path.endswith('.pcap') or file_path.endswith('.pcapng')):
        print("Bad file type was selected.\nPlease choose a valid pcap or pcapng file.")
        return get_pcap_file_windows()
    return file_path
