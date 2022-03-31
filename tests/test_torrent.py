"""Tests for torrent.py"""
import pytest

import bencode


def test_decode_encode_torrent(datadir):
    """Try to decode a torrent file"""
    torrent_data = datadir["big-buck-bunny.torrent"].read("rb")
    decoded_torrent = bencode.decode_torrent(torrent_data)
    encoded_torrent = bencode.encode_torrent(decoded_torrent)

    assert torrent_data == encoded_torrent

    assert decoded_torrent["info"]["pieces"].startswith("d8b13133f3")
    decoded_torrent["info"]["pieces"] = []
    decoded_torrent["piece layers"] = []
    for file in "Big Buck Bunny.en.srt", "Big Buck Bunny.mp4", "poster.jpg":
        decoded_torrent["info"]["file tree"][file][""]["pieces root"] = ""

    assert decoded_torrent == {
        "announce": "udp://tracker.leechers-paradise.org:6969",
        "announce-list": [
            [
                "udp://tracker.leechers-paradise.org:6969",
                "udp://tracker.coppersurfer.tk:6969",
                "udp://tracker.opentrackr.org:1337",
                "udp://explodie.org:6969",
                "udp://tracker.empire-js.us:1337",
                "wss://tracker.btorrent.xyz",
                "wss://tracker.openwebtorrent.com",
                "wss://tracker.fastcast.nz",
            ]
        ],
        "creation date": 1648693526,
        "info": {
            "file tree": {
                "Big Buck Bunny.en.srt": {
                    "": {
                        "length": 140,
                        "pieces root": "",
                    }
                },
                "Big Buck Bunny.mp4": {
                    "": {
                        "length": 276134947,
                        "pieces root": "",
                    }
                },
                "poster.jpg": {
                    "": {
                        "length": 310380,
                        "pieces root": "",
                    }
                },
            },
            "files": [
                {"length": 140, "path": ["Big Buck Bunny.en.srt"]},
                {
                    "attr": "p",
                    "length": 262004,
                    "path": [".pad", "262004"],
                },
                {"length": 276134947, "path": ["Big Buck Bunny.mp4"]},
                {
                    "attr": "p",
                    "length": 164829,
                    "path": [".pad", "164829"],
                },
                {"length": 310380, "path": ["poster.jpg"]},
            ],
            "meta version": 2,
            "name": "Big Buck Bunny",
            "piece length": 262144,
            "pieces": [],
        },
        "url-list": "https://webtorrent.io/torrents/",
        "piece layers": [],
    }


def test_decode_encode_torrent_utf8_suffix():
    """Dictionary keys, which have ".utf-8" suffix, should be decoded and
    encoded using this encoding, even if another encoding is specified in
    the function call
    """
    special_string = "日本語"
    special_string_as_bytes = special_string.encode("utf8")

    data = {b"path.utf-8": special_string_as_bytes}
    torrent_b = bencode.encode(data)
    torrent_p = {"path.utf-8": "日本語"}

    assert bencode.decode_torrent(torrent_b, "ascii") == torrent_p
    assert bencode.encode_torrent(torrent_p, "ascii") == torrent_b


def test_decode_torrent_unsupported_data_type():
    """Try to decode unsupported object (a text string)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.decode_torrent("abcd")

    assert str(excinfo.value) == (
        "Cannot decode data, expected bytes, got <class 'str'> instead."
    )


def test_encode_torrent_unsupported_data_type():
    """Try to decode unsupported object (a text string)"""
    with pytest.raises(ValueError) as excinfo:
        bencode.encode_torrent("abcd")

    assert str(excinfo.value) == (
        "Cannot encode data, expected dict, got <class 'str'> instead."
    )
