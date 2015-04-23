some tips for using:

client: wget -e "http_proxy=http://127.0.0.1:8080"
http://127.0.0.1/a.txt


proxy: ./proxy.py --hostname 0.0.0.0 --port 8080 --cache-config cache.conf


file server:
python -m SimpleHTTPServer 80
