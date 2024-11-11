import requests
from bs4 import BeautifulSoup
import json
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import random
import multiprocessing
# Load article IDs from JSON file
with open('/home/customer/North_Calirona/data_detail/data_id.json', 'r') as file:
    data = json.load(file)

# Define the URL and headers for the POST request
url = "https://www.sosnc.gov/online_services/search/_Business_Registration_profile"

headers = {
    "accept": "*/*",
    "accept-language": "en,vi;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://www.sosnc.gov",
    "referer": "https://www.sosnc.gov/online_services/search/Business_Registration_Results",
    "sec-ch-ua": '"Microsoft Edge";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": '"Android"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36 Edg/129.0.0.0",
    "x-requested-with": "XMLHttpRequest"
}

# List of proxies
proxies_list = [
"http://omhtgnsq:qfe8tzm99qyn@104.250.207.168:6566"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.126.30:6322"
    ,"http://omhtgnsq:qfe8tzm99qyn@166.88.64.8:6391"
    ,"http://omhtgnsq:qfe8tzm99qyn@102.212.88.217:6214"
    ,"http://omhtgnsq:qfe8tzm99qyn@172.98.178.238:6311"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.29.232.61:6721"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.152.125:5162"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.172.156.160:5808"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.226.27:5630"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.161.2.152:6575"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.37.182.209:6260"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.53.219.201:6294"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.41.171:6526"
    ,"http://omhtgnsq:qfe8tzm99qyn@167.160.180.31:6582"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.146.30.65:6569"
    ,"http://omhtgnsq:qfe8tzm99qyn@166.88.58.139:5864"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.41.88:6443"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.127.248.244:5245"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.75.228.103:6182"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.179.51.121:5764"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.36.110.64:6718"
    ,"http://omhtgnsq:qfe8tzm99qyn@209.99.129.86:6074"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.185.84:6090"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.173.99.168:6510"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.131.102.203:5855"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.87.69.15:6020"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.171.147:6438"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.28.234:5249"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.167.94:6276"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.238.49.14:5668"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.238.9.24:6477"
    ,"http://omhtgnsq:qfe8tzm99qyn@188.215.5.106:5136"
    ,"http://omhtgnsq:qfe8tzm99qyn@207.244.219.45:6301"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.143.163:6294"
    ,"http://omhtgnsq:qfe8tzm99qyn@150.107.202.116:6733"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.161.2.254:6677"
    ,"http://omhtgnsq:qfe8tzm99qyn@217.69.121.14:5679"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.37.27:5679"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.173.75.236:6537"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.101.121:5435"
    ,"http://omhtgnsq:qfe8tzm99qyn@102.212.88.52:6049"
    ,"http://omhtgnsq:qfe8tzm99qyn@102.212.88.110:6107"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.233.16.84:6348"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.30.242.209:9603"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.251.214:6476"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.30.242.230:9624"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.239.219.107:6016"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.97.179:6705"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.214.176.220:6191"
    ,"http://omhtgnsq:qfe8tzm99qyn@168.199.141.5:5757"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.118.7:5704"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.47.52.58:8100"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.125.217:6228"
    ,"http://omhtgnsq:qfe8tzm99qyn@85.198.45.234:6158"
    ,"http://omhtgnsq:qfe8tzm99qyn@109.196.163.72:6170"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.228.83.147:5843"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.64.127.214:6167"
    ,"http://omhtgnsq:qfe8tzm99qyn@89.40.222.69:6445"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.3.6:5966"
    ,"http://omhtgnsq:qfe8tzm99qyn@138.128.153.67:5101"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.118.7.245:6271"
    ,"http://omhtgnsq:qfe8tzm99qyn@217.69.121.73:5738"
    ,"http://omhtgnsq:qfe8tzm99qyn@162.245.188.152:6111"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.179.51.214:5857"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.118.7.76:6102"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.90.15:5635"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.96.98:6665"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.170.159.4:6595"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.93.43:6500"
    ,"http://omhtgnsq:qfe8tzm99qyn@88.218.105.31:5795"
    ,"http://omhtgnsq:qfe8tzm99qyn@31.223.188.175:5852"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.103.158:6746"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.249.104.86:6381"
    ,"http://omhtgnsq:qfe8tzm99qyn@161.123.151.156:6140"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.103.98:5782"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.180.171:6810"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.37.182:6772"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.143.125:6256"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.73.250.56:5957"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.211.8.41:6153"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.23.128.15:5643"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.228.83.20:5716"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.56.175.58:5732"
    ,"http://omhtgnsq:qfe8tzm99qyn@91.123.8.145:6685"
    ,"http://omhtgnsq:qfe8tzm99qyn@142.147.240.10:6532"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.124.96:6308"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.172.156.42:5690"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.58.64:5626"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.148.92.49:5976"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.104.60:6284"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.39.8.136:5793"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.10.196:5867"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.229.126.208:7737"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.19.79:6756"
    ,"http://omhtgnsq:qfe8tzm99qyn@91.223.126.154:6766"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.252.37:5651"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.106.107:5752"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.161.3.128:6232"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.12.179.231:6762"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.41.179.102:6637"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.233.26.208:6046"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.247.7.110:5783"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.73.88:5176"
    ,"http://omhtgnsq:qfe8tzm99qyn@178.159.34.36:5983"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.104.46:5656"
    ,"http://omhtgnsq:qfe8tzm99qyn@102.212.88.100:6097"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.250.203.138:5828"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.177.238.146:6323"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.249.61.200:6855"
    ,"http://omhtgnsq:qfe8tzm99qyn@206.206.69.46:6310"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.236.170.126:9159"
    ,"http://omhtgnsq:qfe8tzm99qyn@161.123.93.14:5744"
    ,"http://omhtgnsq:qfe8tzm99qyn@89.116.78.194:5805"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.246.60:6015"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.118.6.180:5896"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.173.76.56:6683"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.39.8.186:5843"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.254.155:5744"
    ,"http://omhtgnsq:qfe8tzm99qyn@194.113.119.250:6924"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.129.254.12:5994"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.35.6:5688"
    ,"http://omhtgnsq:qfe8tzm99qyn@147.136.64.165:5928"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.191.154:6115"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.73.249.250:6829"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.80.10.111:6389"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.91.254:5978"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.188.139:5229"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.31.93:6707"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.48.219:6426"
    ,"http://omhtgnsq:qfe8tzm99qyn@172.84.183.119:5679"
    ,"http://omhtgnsq:qfe8tzm99qyn@207.244.218.75:5683"
    ,"http://omhtgnsq:qfe8tzm99qyn@217.69.126.97:5967"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.84.207:6832"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.124.158:6370"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.118.179:5876"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.37.182.247:6298"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.160.237.96:5775"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.125.87:6098"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.46.161.27:5077"
    ,"http://omhtgnsq:qfe8tzm99qyn@81.21.234.147:6536"
    ,"http://omhtgnsq:qfe8tzm99qyn@89.35.80.158:6813"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.52.211:6871"
    ,"http://omhtgnsq:qfe8tzm99qyn@161.123.101.75:6701"
    ,"http://omhtgnsq:qfe8tzm99qyn@172.98.178.39:6112"
    ,"http://omhtgnsq:qfe8tzm99qyn@89.116.78.9:5620"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.125.131:6142"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.248.254:6864"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.64.219:6477"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.214.176.32:6003"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.94.136.4:6780"
    ,"http://omhtgnsq:qfe8tzm99qyn@84.33.224.153:6177"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.71.44:6642"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.152.198:5235"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.150.21.156:5772"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.127.248.189:5190"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.30.241.159:9870"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.126.137:6429"
    ,"http://omhtgnsq:qfe8tzm99qyn@138.128.148.35:6595"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.84.140:6765"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.114.58.105:6526"
    ,"http://omhtgnsq:qfe8tzm99qyn@207.244.218.228:5836"
    ,"http://omhtgnsq:qfe8tzm99qyn@202.155.187.105:6872"
    ,"http://omhtgnsq:qfe8tzm99qyn@155.254.49.188:6748"
    ,"http://omhtgnsq:qfe8tzm99qyn@202.155.186.61:6472"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.246.105:6060"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.175.47:6083"
    ,"http://omhtgnsq:qfe8tzm99qyn@91.123.11.237:6503"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.10.3:5674"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.170.159.43:6634"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.8.140:6822"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.62.19:5664"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.7.42:6446"
    ,"http://omhtgnsq:qfe8tzm99qyn@161.123.152.207:6452"
    ,"http://omhtgnsq:qfe8tzm99qyn@192.186.151.163:8664"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.226.169:5772"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.107.67:5719"
    ,"http://omhtgnsq:qfe8tzm99qyn@185.118.6.230:5946"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.180.143:6782"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.57.221:6230"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.92.168:6367"
    ,"http://omhtgnsq:qfe8tzm99qyn@207.244.217.189:6736"
    ,"http://omhtgnsq:qfe8tzm99qyn@193.42.225.74:6565"
    ,"http://omhtgnsq:qfe8tzm99qyn@91.223.102.133:6455"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.154.200.22:5723"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.66.17:5602"
    ,"http://omhtgnsq:qfe8tzm99qyn@81.21.234.223:6612"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.114.58.17:6438"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.46.148.151:5839"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.105.111.77:6755"
    ,"http://omhtgnsq:qfe8tzm99qyn@209.35.5.143:6834"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.141.81.144:6204"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.222.38:6635"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.52.188:7350"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.131.94.112:6099"
    ,"http://omhtgnsq:qfe8tzm99qyn@206.41.179.147:5823"
    ,"http://omhtgnsq:qfe8tzm99qyn@178.159.34.182:6129"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.105.111.194:6872"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.58.206:5768"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.124.38:6250"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.73.249.68:6647"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.214.177.174:5865"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.74.118.38:6193"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.246.101:6056"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.175.119.39:6567"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.141.36:6433"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.69.164:6154"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.143.245.105:6345"
    ,"http://omhtgnsq:qfe8tzm99qyn@168.199.225.200:6968"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.125.92:6103"
    ,"http://omhtgnsq:qfe8tzm99qyn@86.38.234.182:6636"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.103.2:5686"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.173.104.248:6385"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.73.249.3:6582"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.41.177.42:5692"
    ,"http://omhtgnsq:qfe8tzm99qyn@142.147.240.228:6750"
    ,"http://omhtgnsq:qfe8tzm99qyn@23.247.101.179:6918"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.132.62:6040"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.158.205.166:6394"
    ,"http://omhtgnsq:qfe8tzm99qyn@84.33.243.234:5925"
    ,"http://omhtgnsq:qfe8tzm99qyn@89.35.80.251:6906"
    ,"http://omhtgnsq:qfe8tzm99qyn@107.181.154.116:5794"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.233.26.49:5887"
    ,"http://omhtgnsq:qfe8tzm99qyn@154.73.249.10:6589"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.99.33.172:6167"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.233.16.250:6514"
    ,"http://omhtgnsq:qfe8tzm99qyn@134.73.64.200:6485"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.43.179.107:6114"
    ,"http://omhtgnsq:qfe8tzm99qyn@198.105.100.195:6446"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.149.207:5835"
    ,"http://omhtgnsq:qfe8tzm99qyn@136.0.109.148:6434"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.117.55.82:6728"
    ,"http://omhtgnsq:qfe8tzm99qyn@184.174.56.241:5253"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.19.216.100:5775"
    ,"http://omhtgnsq:qfe8tzm99qyn@84.247.60.240:6210"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.10.241:5912"
    ,"http://omhtgnsq:qfe8tzm99qyn@136.0.88.75:5133"
    ,"http://omhtgnsq:qfe8tzm99qyn@168.199.186.155:6578"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.154.200.215:5916"
    ,"http://omhtgnsq:qfe8tzm99qyn@216.19.217.159:6399"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.154.224.83:6624"
    ,"http://omhtgnsq:qfe8tzm99qyn@85.198.45.25:5949"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.223.171.207:6498"
    ,"http://omhtgnsq:qfe8tzm99qyn@45.61.100.137:6405"
    ,"http://omhtgnsq:qfe8tzm99qyn@64.137.88.22:6261"
    ,"http://omhtgnsq:qfe8tzm99qyn@147.136.64.97:5860"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.52.175:7337"
    ,"http://omhtgnsq:qfe8tzm99qyn@103.114.59.30:6807"
    ,"http://omhtgnsq:qfe8tzm99qyn@38.153.140.176:9054"
    ,"http://omhtgnsq:qfe8tzm99qyn@173.0.9.147:5730"
    ,"http://omhtgnsq:qfe8tzm99qyn@104.239.86.177:6087"
]

def fetch_data(article_id):
    max_retries = len(proxies_list)
    
    for attempt in range(max_retries):
        proxy = random.choice(proxies_list)
        proxies = {
            "http": proxy,
            "https": proxy
        }

        data_payload = {
            "Id": article_id
        }

        try:
            response = requests.post(url, headers=headers, data=data_payload, proxies=proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            entity_details = {
                "Legal Name": extract_text_after_label(soup, "Legal Name"),
                "Previous Legal Name": extract_text_after_label(soup, "Prev Legal Name"),
                "SosId": extract_text_after_label(soup, "SosId:"),
                "Status": extract_text_after_label(soup, "Status:"),
                "Date Formed": extract_text_after_label(soup, "Date Formed:"),
                "Citizenship": extract_text_after_label(soup, "Citizenship:"),
                "Fiscal Month": extract_text_after_label(soup, "Fiscal Month:"),
                "Annual Report Due Date": extract_text_after_label(soup, "Annual Report Due Date:")
            }

            registered_agent = extract_text_after_label(soup, "Registered Agent:")

            addresses = {}
            for label in ["Mailing", "Principal Office", "Reg Office", "Reg Mailing"]:
                addresses[label] = extract_address(soup, label)

            officers = extract_officers(soup)
            stock_info = extract_stock(soup)

            final_data = {
                "Article ID": article_id,
                "Entity Details": entity_details,
                "Registered Agent": registered_agent,
                "Addresses": addresses,
                "Officers": officers,
                "Stock": stock_info
            }

            # Append data to file immediately
            with open('/home/customer/North_Calirona/data/data.json', 'a') as outfile:
                json.dump(final_data, outfile, indent=4)
                outfile.write(',\n')
    
            print(f"Data for article_id {article_id} saved to output_data.json")
            break  # Exit the loop if successful

        except requests.RequestException as e:
            print(f"Request failed for article_id {article_id} with proxy {proxy}: {e}")
            # Optionally, wait before retrying
            time.sleep(1)

def extract_text_after_label(soup, label_text):
    label_element = soup.find(string=lambda text: text and label_text in text)
    if label_element:
        span_element = label_element.find_next('span')
        if span_element:
            return span_element.get_text(strip=True)
    return "Not Found"

def extract_address(soup, label):
    address_element = soup.find(string=lambda text: text and label in text)
    if address_element:
        address_parts = []
        next_elements = address_element.find_all_next(['span', 'br'])
        for elem in next_elements:
            if elem.name == 'span' and elem.get_text(strip=True):
                address_parts.append(elem.get_text(strip=True))
            elif elem.name == 'br':
                continue
            if elem.find_next_sibling(name='p') is None:
                break
        return ', '.join(address_parts)
    return "Not Found"

def extract_officers(soup):
    officers = []
    for officer in soup.find_all('p'):
        title_element = officer.find('span', class_='greenLabel')
        name_element = officer.find('a')
        if title_element and name_element:
            title = title_element.get_text(strip=True)
            name = ' '.join(name_element.get_text(strip=True).split())
            address = ', '.join(officer.get_text(strip=True).split('\n')[-4:])
            officers.append({
                "Title": title,
                "Name": name,
                "Address": address
            })
    return officers

def extract_stock(soup):
    stock_info = {}
    for stock_class in ['COMMON', 'PREFERRED']:
        stock_section = soup.find(string=lambda text: text and stock_class in text)
        if stock_section:
            shares_element = stock_section.find_next(string=lambda text: text and "Shares:" in text)
            no_par_value_element = stock_section.find_next(string=lambda text: text and "No Par Value:" in text)
            if shares_element and no_par_value_element:
                shares = shares_element.find_next('span').get_text(strip=True)
                no_par_value = no_par_value_element.find_next('span').get_text(strip=True) == "Yes"
                stock_info[f"{stock_class.capitalize()} Stock"] = {
                    "Shares": int(shares.replace(',', '')),
                    "No Par Value": no_par_value
                }
    return stock_info

# Use ThreadPoolExecutor within a ProcessPoolExecutor to parallelize the fetching
def process_article_ids(article_ids):
    with ThreadPoolExecutor(max_workers=25) as executor:
        executor.map(fetch_data, article_ids)

def main():
    num_workers = multiprocessing.cpu_count()
    chunk_size = len(data) // num_workers
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        executor.map(process_article_ids((item.get("article_id") for item in data)), chunks)

if __name__ == "__main__":
    main()