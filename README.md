# Commaless Note

**File Extension:** `.note`

**Encoding:** UTF-8

**License:** CC0

A comma-less data format designed for human readability and JSON compatibility.

This repository serves as a syntax proposal and specification; it does not include a production-ready parser implementation.

## 1. Why Commaless Note?

* **No Trailing Comma**: It prevents trailing comma errors.

* **Easy to Read & Write**: It allows for data representation as if writing a note.

* **Minimal Shift**: Designed mainly with symbols that do not require the Shift key.

* **JSON Compatible**: Fully compatible with JSON, expressing the same data with a simpler syntax.

* **Compact**: Reduces syntax to decrease file size and AI token usage.

## 2. Syntax & Examples

Note uses spaces and newlines as data delimiters instead of commas (`,`).

### ① Data Structures

Both arrays and objects use `[ ]`, distinguished by whether they contain an assignment symbol (`=`).

Key-value pairs and standalone values cannot be mixed within the same brackets.

```
-- Object
user = [ name='John Doe' occupation='Developer' ]

-- Array
skills = [ 'javascript' 'python' 'rust' ]
```

### ② Key Naming Rules

Object keys must start with a letter or an underscore (`_`) and consist of alphanumeric characters or underscores.

For keys starting with a digit or containing spaces/special characters, or reserved words, quoted keys must be used.

```
-- Bare keys
app_version = '2.4.0'
_internal_id = 101

-- Quoted keys
"1st_tier" = true
"service-node-01" = 'active'
```

### ③ Root Container

The root `[ ]` is omitted. The root type is determined by the format of the internal content.

```
-- Implicit object root
name = 'Project A'
version = 1.0

-- Implicit array root
; id=1 name='First'
; id=2 name='Second'
```

### ④ Path Flattening

Keys within nested objects can be represented in a single line using the dot (`.`).

Missing or non-object keys are automatically created as empty objects.

If already an object, keys are added or overwritten.

```
-- Automatic creation and merging
db.port = 5432                        -- db=[ port=5432 ]
db.host = 'localhost'                 -- db=[ port=5432 host='localhost' ]

-- Overwriting non-object values
timeout = 5000
timeout.connect = 3000                -- timeout=[ connect=3000 ]

-- Path flattening with quoted keys
project.'v1.0-alpha'.status = 'active' -- project=[ 'v1.0-alpha'=[ status='active' ] ]
app."user's choice".theme = 'dark'     -- app=[ "user's choice"=[ theme='dark' ] ]
```

### ⑤ Flattened Objects in Arrays

Multiple objects can be listed within an array without nested brackets by using the semicolon (`;`).

```
-- Array of objects
employees = [
  ; id=101 name='Alice' department='Design'
  ; id=102 name='Bob' department='Engineering'
]

-- Mixed array
mixed_items = [
  'Task List Start'
  ; id=1 title='Initial Design' status='done'
  '--- separator ---'
  ; id=2 title='Feedback Loop' status='pending'
]
```

A tabular pattern can be used as a convention to avoid key repetition.

```
products = [
  [ 'id' 'name' 'price' 'stock' ]
  [ 101 'Wireless Mouse' 24.99 50 ]
  [ 102 'Mechanical Keyboard' 119.99 30 ]
]
```

### ⑥ Empty Structures

Empty arrays and objects are denoted as follows:

```
data.empty = [
  arr = [ ]            -- JSON: []
  obj = [-]            -- JSON: {}

  hyphen_arr = ['-']   -- JSON: ["-"]
  negative_arr = [-1]  -- JSON: [-1]
  obj_arr = [;]        -- JSON: [{}]
]
```

### ⑦ Multi-line Strings

Multi-line text uses `#[ ]#`, allowing variable-length #s (e.g., `##[ ]##`) to prevent delimiter collision.

The first newline (`\n`) immediately after the opening delimiter is ignored.

All newlines are normalized to `\n` during parsing.

Indentation is preserved.

```
server.banner = ##[
  ======================================
  #[ Welcome to Production API Server ]#
  Status: Online (v2.4.0)
  ======================================
]##

database.queries.get_active_users = #[
  SELECT id, name, email
  FROM users
  WHERE status = 'active'
    AND last_login > '2024-01-01'
  ORDER BY created_at DESC;
]#
```

### ⑧ Escape Sequence

Standard string literals (`''` or `""`) support the escape sequences: `\n`, `\t`, `\r`, `\b`, `\f`, `\'`, `\"`, `\\`, and `\u{x...}` (e.g., `\u{41}`, `\u{1F600}`).

Inside multi-line text blocks, escape sequences require a hash prefix that matches the length of the block's delimiters (e.g., `\#n` inside `#[ ]#`, or `\##n` inside `##[ ]##`).

```
example.standard = "Standard text\n\u{1F600}"

example.multiline = ##[
  Path: C:\new_folder\test
  Tag: #[USER_NAME]#
  Done\##u{1F600}
]##
```

### ⑨ Comments

Single-line comments use `--`.

Multi-line comments use `--[ --]`, allowing variable-length hyphens (e.g., `---[ ---]`) to prevent delimiter collision.

```
--[
# API Server Configuration
- Environment: Local & Production
- Updated: 2024-05-20
--]

-- Local development and test server settings (Active)
server.host = 'localhost'
server.port = 8080
server.timeout = 5000  -- Response timeout in ms

-- Production server settings (Inactive)
--[
server.host = 'api.production-site.com'
server.port = 443
server.ssl = true
--]
```

## 3. Data Types

Supports the same data types as JSON.

* **String**: `' '`, `" "`, `#[ ]#`

* **Number**: `1024`, `3.14`, `-5`, `1.2e-3`

* **Boolean**: `true`, `false`

* **Null**: `nil`

* **Array**: `[ val1 val2 ]`

* **Object**: `[ key=val ]`

## 4. Use Cases

### ① Configuration Files

An example of a system configuration that includes nested hierarchies and arrays of objects.

**system_config.json**

```
{
  "project": {
    "name": "Cloud Mesh",
    "environment": "production",
    "version": "2.4.0"
  },
  "database": {
    "main": { "host": "10.0.0.1", "port": 5432 },
    "replicas": [
      { "host": "10.0.0.2", "port": 5432, "active": true },
      { "host": "10.0.0.3", "port": 5432, "active": false }
    ]
  },
  "services": {
    "auth": { "enabled": true, "provider": "oidc" },
    "storage": { "bucket": "assets", "region": "us-east-1" }
  },
  "features": ["caching", "logging", "monitoring"]
}
```

**system_config.note**

```
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
```

### ② Log Data

Note can be used directly as a line-by-line format like JSONL.

To keep the single-line structure, use `\n` instead of multi-line strings (`"""`).

**logs.jsonl**

```
{"id": 1, "level": "info", "msg": "Server started"}
{"id": 2, "level": "warn", "msg": "High memory usage"}
{"id": 3, "level": "error", "msg": "Database connection failed"}
{"id": 4, "level": "info", "msg": "User logout"}
{"id": 5, "level": "debug", "msg": "Cache cleared"}
```

**logs.note**

```
; id=1 level='info' msg='Server started'
; id=2 level='warn' msg='High memory usage'
; id=3 level='error' msg='Database connection failed'
; id=4 level='info' msg='User logout'
; id=5 level='debug' msg='Cache cleared'
```

**Acknowledgments:** The documentation structure and examples were refined with the assistance of AI.

