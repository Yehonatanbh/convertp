import click

from convertp import ConveRTP


@click.command()
@click.option('-d', '--dst-file', help='The destination file', required=True)
@click.option('-p', '--pcap-file', help='The source file')
@click.option('-v', '--from-video', type=click.BOOL, help='Weather the pcap is a video pcap')
def convert(dst_file, pcap_file, from_video):
    convertor = ConveRTP(dst_file=dst_file, pcap_path=pcap_file, from_video=from_video)
    convertor.convert()


if __name__ == '__main__':
    convert()
