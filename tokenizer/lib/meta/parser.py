import re

class Parser():

    def parseLine(self,line=None,replace=False):
        metadata = {}
        r_meta = re.compile(r'^(META\|\S+)')
        matched = r_meta.match(line)
        if matched:
            metadata = self.parseToken(matched.group(0))
            if replace:
                line = re.sub(r'^META\|\S+\s+','',line)
        return metadata, line

    def parseToken(self,token):
        r_meta = re.compile(r'^META\|.*')
        r_item = re.compile(r'^(TB_WORD|TB_SENT|CITE)_(.+)$')
        metadata = {}
        if r_meta.match(token):
            data = token.split('|')
            for item in data:
                item_match = r_item.match(item)
                if item_match:
                    metadata[item_match.group(1)] = item_match.group(2)
        return metadata





