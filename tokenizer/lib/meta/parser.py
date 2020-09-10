import re

class Parser():

    METADATA_EXTENSIONS = [
        {
            'name': 'TB_SENT',
            'segment_level': True,
            'default': '',
            'forward': True
        },
        {
            'name': 'TB_WORD',
            'segment_level': False,
            'default': '',
            'forward': True
        },
        {
            'name': 'CITE',
            'segment_level': True,
            'default': '',
            'forward': True
        }

    ]

    METADATA_FIELDS = '|'.join(list(map(lambda i: i['name'], METADATA_EXTENSIONS )))

    def parseLine(self,line="",extra="",replace=False):
        metadata = {}
        r_meta = re.compile(r'^(META\|\S+)')
        matched = r_meta.match(line)
        if matched:
            metadata = self.parseToken(matched.group(0))
            if replace:
                line = re.sub(r'^META\|\S+\s+','',line)
        matched_extra = r_meta.match(extra)
        if matched_extra:
            extra_meta = self.parseToken(matched_extra.group(0))
            for item in extra_meta:
                metadata[item] = extra_meta[item]
        return metadata, line

    def parseToken(self,token):
        r_meta = re.compile(r'^META\|.*')
        r_item = re.compile(rf"^({Parser.METADATA_FIELDS})_(.+)$")
        metadata = {}
        if r_meta.match(token):
            data = token.split('|')
            for item in data:
                item_match = r_item.match(item)
                if item_match:
                    metadata[item_match.group(1)] = item_match.group(2)
        return metadata





