# PoC Parser, AI-Assisted

import re


def tokenize(text):
    text = re.sub(r'--.*', '', f"[{text}]")
    return re.findall(r"\[|\]|=|;|\.|-\d+|\d+|-|\"[^\"]*\"|'[^']*'|[^\s\[\]=;\.-]+", text)


def cast(val):
    if val == 'nil': return None
    if val in ('true', 'false'): return val == 'true'

    return val


def parse_note(tokens):
    token = tokens.pop(0)
    
    if token != '[': return cast(token)

    first = parse_note(tokens)

    if first == ']': return []
    if first == '-' and tokens[0] == ']': tokens.pop(0); return {}

    if tokens[0] in ('=', '.'):
        return parse_object(tokens, first)
    else:
        return parse_list(tokens, first)


def parse_object(tokens, first):
    obj = {}
    set_key_val(tokens, obj, first)

    while tokens[0] != ']':
        set_key_val(tokens, obj, tokens.pop(0))
    tokens.pop(0)

    return obj


def parse_list(tokens, first):
    lst = []
    append_item(tokens, lst, first)

    while tokens[0] != ']':
        append_item(tokens, lst, parse_note(tokens))
    tokens.pop(0)

    return lst


def set_key_val(tokens, obj, token):
    path = [token]

    while tokens[0] == '.':
        tokens.pop(0)
        path.append(tokens.pop(0))
    tokens.pop(0)

    for key in path[:-1]:
        obj = obj.setdefault(key, {})
    obj[path[-1]] = parse_note(tokens)


def append_item(tokens, lst, token):
    if token == ';':
        obj = {}

        while tokens[0] not in (';', ']'):
            curr = tokens.pop(0)

            if tokens[0] in ('.', '='):
                set_key_val(tokens, obj, curr)
            else:
                lst.append(obj)
                lst.append(curr)
                return
            
        lst.append(obj)

    else:
        lst.append(token)


if __name__ == '__main__':
    import json
    
    sample_text = """
project = [
  name = 'Cloud Mesh'
  environment = 'production'
  version = '2.4.0'
]

database.main = [ host='10.0.0.1' port=5432 ]
database.replicas = [
  ; host='10.0.0.2' port=5432 active=true
  ; host='10.0.0.3' port=5432 active=false
]

services.auth = [ enabled=true provider='oidc' ]
services.storage = [ bucket='assets' region='us-east-1' ]

features = [ 'caching' 'logging' 'monitoring' ]
"""

    tokens = tokenize(sample_text)
    result = parse_note(tokens)
    print(json.dumps(result, indent=2))
