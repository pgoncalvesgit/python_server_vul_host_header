from flask import Flask, request
import subprocess
import logging

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)


@app.before_request
def log_headers():
    app.logger.debug('- Host header: %s', request.headers.get('host', request.headers.get('Host', "unknown")))
    app.logger.debug('- Referer header: %s', request.headers.get('referer', request.headers.get('Referer', "unknown")))


@app.route("/")
def index():
    return '''
        <html><body>
            <a href="/safe">safe</a>
            <a href="/vul_query?test=localhost">vulnerable on query</a>
            <a href="/vul_host_header">vulnerable on host header</a>
        </body></html>
    '''


@app.route("/safe")
def safe():
    return '''
        <html><body>
        <a>Nothing here</a>
        </body></html>
    '''


@app.route("/vul_query")
def vul_query():
    test = request.args.get("test")
    cmd = 'ping -c 1 ' + test

    try:
        subprocess.check_output(cmd, shell=True)
    # Windows
    except subprocess.CalledProcessError:
        cmd = 'ping -n 1 ' + test
        subprocess.check_output(cmd, shell=True)

    return '''
        <html><body>
            <p>Current host is: ''' + test + '''</a>
        </body></html>
    '''


# command injection


@app.route("/vul_host_header")
def vul_host_header():
    host = request.headers.get('host', request.headers.get('Host', "unknown"))
    cmd = 'ping -c 1 ' + host

    try:
        subprocess.check_output(cmd, shell=True)
    # Windows
    except subprocess.CalledProcessError:
        cmd = 'ping -n 1 ' + host
        subprocess.check_output(cmd, shell=True)

    return '''
        <html><body>
            <p>Current host is: ''' + host + '''</a>
        </body></html>
    '''


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
