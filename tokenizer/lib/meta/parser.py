import re

class Parser():
    """ Parses Alpheios Metadata from Text """

    METADATA_FIELDS = [
        {
            'name': 'TB_SENT',
            'default': '',
        },
        {
            'name': 'TB_WORD',
            'default': '',
        },
        {
            'name': 'CITE',
            'default': '',
        }

    ]

    METADATA_FIELD_RE = '|'.join(list(map(lambda i: i['name'], METADATA_FIELDS )))

    @staticmethod
    def metadata_field_name(name) :
        """ get the name of the metadata field for inclusion in a token's public interface

            :param name: the field name
            :type name: string

            :return: the public field name
            :rtype: string
        """
        return f"alpheios_data_{name.lower()}"

    def parseLine(self,line="",extra="",replace=False):
        """ parse metadata from a line of text

            :param line: the text of the line
            :type line: string
            :param extra: extra text to add to the line
            :type extra: string
            :param replace: whether or not the metadata should be removed from the text after parsing
            :type replace: boolean

            :return: tuple of the parsed metadata and the potentially updated text
            :rtype: dict, string
        """
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
        """ parse metadata from a single token

            :param token: the token text
            :type token: string

            :return: the parsed metdata
            :rtype: dict
        """

        r_meta = re.compile(r'^META\|.*')
        r_item = re.compile(rf"^({Parser.METADATA_FIELD_RE})_(.+)$")
        metadata = {}
        if r_meta.match(token):
            data = token.split('|')
            for item in data:
                item_match = r_item.match(item)
                if item_match:
                    metadata[item_match.group(1)] = item_match.group(2)
        return metadata





