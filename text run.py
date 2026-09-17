import urllib.request
import json
from datetime import datetime

# 1. 叫小幫手去抓比特幣最近 30 天的價格
url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=30"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())

dates = []
prices = []
ranges = []

for day in data:
    # 整理日期（月-日）
    date_str = datetime.fromtimestamp(day[0] / 1000).strftime('%m-%d')
    open_p = float(day[1])
    high_p = float(day[2])
    low_p = float(day[3])
    close_p = float(day[4])
    
    dates.append(date_str)
    prices.append(close_p)
    # 計算當天波動幅度（最高價與最低價的差距百分比）
    range_pct = round(((high_p - low_p) / open_p) * 100, 2)
    ranges.append(range_pct)

latest_price = prices[-1]
avg_vol = round(sum(ranges) / len(ranges), 2)

# 2. 把數據包裝成一個乾淨漂亮的網頁
html_code = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>比特幣每日走勢與波動</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    body {{ font-family: sans-serif; background: #1a1a2e; color: #fff; padding: 20px; max-width: 800px; margin: auto; }}
    .card {{ background: #16213e; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
  </style>
</head>
<body>
  <h2>📊 比特幣每日行情與波動分析</h2>
  <div class="card">
    <p>最新收盤價格：<b>${latest_price:,.2f} 美元</b></p>
    <p>近 30 天平均每日震幅：<b>{avg_vol}%</b></p>
  </div>
  <div class="card">
    <h3>近 30 天價格走勢</h3>
    <canvas id="chartPrice"></canvas>
  </div>
  <div class="card">
    <h3>每日高低震幅 (%)</h3>
    <canvas id="chartVol"></canvas>
  </div>
  <script>
    new Chart(document.getElementById('chartPrice'), {{
      type: 'line',
      data: {{ labels: {json.dumps(dates)}, datasets: [{{ label: '價格 (USD)', data: {json.dumps(prices)}, borderColor: '#4ecca3' }}] }}
    }});
    new Chart(document.getElementById('chartVol'), {{
      type: 'bar',
      data: {{ labels: {json.dumps(dates)}, datasets: [{{ label: '當日震幅 %', data: {json.dumps(ranges)}, backgroundColor: '#e94560' }}] }}
    }});
  </script>
</body>
</html>"""

# 存檔成 index.html（這就是網頁首頁）
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("完成網頁製作！")
