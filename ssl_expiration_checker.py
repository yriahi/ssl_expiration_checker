import datetime
import socket
import ssl


hosts = ["www.youssefriahi.com",
         "prod.youssefriahi.com"]


def get_ssl_expiry_datetime(host):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'

    # context with secure default settings
    # support for server name indication (SNI) and hostname matching
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=host)

    # 3 second timeout
    conn.settimeout(3.0)

    # connect and get ssl_info
    conn.connect((host, 443))
    ssl_info = conn.getpeercert()

    # parse string into datetime object
    return datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)


for host in hosts:
    # get current time
    now = datetime.datetime.now()

    # get expiration date (e.g. 2020-07-04 12:00:00)
    expirationDate = get_ssl_expiry_datetime(host)
    delta = expirationDate - now

    if delta.days < 30:
        delta = str(delta).split(",")[0].split(" ")[0]
        print(f'{host},{delta}')
