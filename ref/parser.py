# PoC Parser, AI-Assisted

import re


def tokenize(text):
    text = re.sub(r'--.*', '', f"[{text}]")
    return re.findall(r"\[|\]|=|;|\.|-\d+|\d+|-|\"[^\"]*\"|'[^']*'|[^\s\[\]=;\.-]+", text)


def parse_note(tokens):
    if tokens[0] != '[': return parse_atom(tokens)
    tokens.pop(0)

    if tokens[0] == ']': tokens.pop(0); return []
    if tokens[0] == '-':
        tokens.pop(0)
        if tokens[0] == ']': tokens.pop(0); return {}
    if tokens[0] == ';': return parse_list(tokens)
    
    val = parse_note(tokens)

    if tokens[0] in ('=', '.'):
        return parse_object_tail(tokens, val)
    else:
        return parse_list_tail(tokens, val)


def parse_object_tail(tokens, atom):
    obj = {}
    set_key_val(tokens, obj, atom)

    while tokens[0] != ']':
        set_key_val(tokens, obj, parse_atom(tokens))
    tokens.pop(0)

    return obj


def parse_list_tail(tokens, val):
    lst = [val]

    while tokens[0] != ']':
        append_item(tokens, lst)
    tokens.pop(0)

    return lst


def parse_list(tokens):
    lst = []

    while tokens[0] != ']':
        append_item(tokens, lst)
    tokens.pop(0)

    return lst


def set_key_val(tokens, obj, atom):
    path = [atom]

    while tokens[0] == '.':
        tokens.pop(0)
        path.append(parse_atom(tokens))
    tokens.pop(0)

    for key in path[:-1]:
        obj = obj.setdefault(key, {})
    obj[path[-1]] = parse_note(tokens)


def append_item(tokens, lst):
    if tokens[0] == ';':
        tokens.pop(0)
        obj = {}

        while tokens[0] not in (';', ']'):
            val = parse_note(tokens)

            if tokens[0] in ('.', '='):
                set_key_val(tokens, obj, val)
            else:
                lst.append(obj)
                lst.append(val)
                return
            
        lst.append(obj)

    else:
        lst.append(parse_note(tokens))


def parse_atom(tokens):
    token = tokens.pop(0)
    if token == 'nil': return None
    if token in ('true', 'false'): return token == 'true'

    return token


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
