


class CleanHtmlHandler:
    def __init__(self):
        pass

    def just_do_it(self,data):
        return list(map(self.clean_fields, data))

    def clean_html(self,escaped_html):
        inline = ['b', 'big', 'i', 'small', 'ttabbr', 'acronym',
                  'cite', 'code', 'dfn', 'em', 'kbd', 'strong',
                  'samp', 'vara', 'bdo', 'br', 'img', 'map',
                  'object', 'q', 'span', 'sub', 'supbutton',
                  'input', 'label', 'select', 'textarea']
        hide_regex = '<script[^<]*</script>'
        inline_regex = '</?(?:'+'|'.join(inline) + ')[^>]*>'
        block_regex = '</?[^>]*>'
        raw_html = html.unescape(escaped_html)
        scriptless_html = re.sub(hide_regex, '', raw_html)
        inline_html = re.sub(inline_regex, '', scriptless_html)
        blocked_html = re.sub(block_regex, '\n', inline_html)
        blocked_html = blocked_html.replace('\\xa0', ' ')
        blocked_html = blocked_html.replace(u'\xa0', ' ')
        blocked_html = re.sub('[ ]+', ' ', blocked_html)
        clean_ = re.sub('\n[ \n]+', '\n', blocked_html)
        return clean_

    def clean_fields(self,dict):
        for k,v in dict.items():
            if type(v) is str:
                dict[k] = clean_html(v)
        return dict
