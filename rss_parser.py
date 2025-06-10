import xml.etree.ElementTree as ET

class RSSParser:
    """Simple RSS feed parser for extracting audio URLs."""

    def extract_audio_urls(self, xml_content: str) -> list[str]:
        """Return a list of audio file URLs from enclosure tags."""
        try:
            root = ET.fromstring(xml_content)
        except ET.ParseError as exc:
            raise ValueError("Invalid XML") from exc

        urls = []
        for enclosure in root.findall(".//enclosure"):
            url = enclosure.attrib.get("url")
            if url:
                urls.append(url)
        return urls
