host = '127.0.0.1'
port = 8080
work_dir = '../'
branch = 'master'

nodes = [
    'http://example.com'
]

actions = [
    'echo {branch}',
    'ls -la {work_dir}'
]