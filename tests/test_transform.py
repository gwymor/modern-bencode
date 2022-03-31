"""Tests for transform.py"""
import os

import bencode


def test_transform_bencode_data_1():
    """Try to transform some bencoded data"""
    source_data = """ \x00 \t \r \n \\ " [ ] """.encode("ascii")
    data_as_string = bencode.be_to_str(source_data)
    assert data_as_string == " [00] [09] [0d] [0a] [5c] [22] [5b] [5d] "


def test_transform_bencode_data_2(datadir):
    """Try to transform some bencoded data"""
    torrent_data = datadir["big-buck-bunny.torrent"].read("rb")
    torrent_data_dec = bencode.decode(torrent_data)
    torrent_data_dec[b"info"].pop(b"pieces")
    torrent_data_dec.pop(b"piece layers")
    for file in b"Big Buck Bunny.en.srt", b"Big Buck Bunny.mp4", b"poster.jpg":
        torrent_data_dec[b"info"][b"file tree"][file][b""].pop(b"pieces root")
    data_as_string = bencode.be_to_str(bencode.encode(torrent_data_dec))
    assert data_as_string == (
        "d8:announce40:udp://tracker.leechers-paradise.org:696913:"
        "announce-listll40:udp://tracker.leechers-paradise.org:696934:udp://"
        "tracker.coppersurfer.tk:696933:udp://tracker.opentrackr.org:133723:"
        "udp://explodie.org:696931:udp://tracker.empire-js.us:133726:wss://"
        "tracker.btorrent.xyz32:wss://tracker.openwebtorrent.com25:wss://"
        "tracker.fastcast.nzee13:creation datei1648693526e4:infod9:"
        "file treed21:Big Buck Bunny.en.srtd0:d6:lengthi140eee18:"
        "Big Buck Bunny.mp4d0:d6:lengthi276134947eee10:poster.jpgd0:d6:"
        "lengthi310380eeee5:filesld6:lengthi140e4:pathl21:"
        "Big Buck Bunny.en.srteed4:attr1:p6:lengthi262004e4:pathl4:.pad6:"
        "262004eed6:lengthi276134947e4:pathl18:Big Buck Bunny.mp4eed4:attr1:"
        "p6:lengthi164829e4:pathl4:.pad6:164829eed6:lengthi310380e4:pathl10:"
        "poster.jpgeee12:meta versioni2e4:name14:Big Buck Bunny12:"
        "piece lengthi262144ee8:url-list31:https://webtorrent.io/torrents/e"
    )


def test_transform_torrent_file(datadir):
    """Try to transform a torrent file"""
    torrent_data = datadir["big-buck-bunny.torrent"].read("rb")
    data_as_string = bencode.be_to_str(torrent_data)
    data_as_bytes = bencode.str_to_be(data_as_string)
    assert torrent_data == data_as_bytes


def test_transform_random_data():
    """Try to transform a random sequence of bytes"""
    source_data = os.urandom(10 ** 5)
    data_as_string = bencode.be_to_str(source_data)
    data_as_bytes = bencode.str_to_be(data_as_string)
    assert source_data == data_as_bytes
