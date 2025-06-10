from rss_parser import RSSParser


def test_rss_parser_extracts_audio_urls():
    xml_content = """<rss><channel>\n" + \
        "<item><enclosure url='a.mp3'/></item>\n" + \
        "<item><enclosure url='b.mp3'/></item>\n" + \
        "</channel></rss>"""

    parser = RSSParser()
    urls = parser.extract_audio_urls(xml_content)

    assert urls == ["a.mp3", "b.mp3"]
