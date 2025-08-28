import requests
import random
import time
from datetime import datetime, timedelta
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class KeepAliveService:
    def __init__(self):
        # 目标网站列表
        self.targets = [
            "https://b2.qklm.xyz",
            "https://qklm.xyz",
            "https://wyb.qklm.xyz"
        ]
        # 时间配置（确保12分钟内必访问）
        self.max_interval = 12 * 60  # 最大间隔12分钟（秒）
        self.check_threshold = 10 * 60  # 提前2分钟检查（秒）
        self.min_wait = 1 * 60  # 访问间隔：1-6分钟（秒）
        self.max_wait = 6 * 60
        # 用实例属性记录最后访问时间（替代全局变量）
        self.last_visited = {url: datetime.now() - timedelta(seconds=self.max_interval) for url in self.targets}
        # 初始化UserAgent生成器
        self.ua = UserAgent()

    def get_random_headers(self):
        """生成随机请求头，模拟不同设备和浏览器"""
        return {
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": random.choice(["zh-CN,zh;q=0.9", "en-US,en;q=0.9,zh-CN;q=0.8", "ja-JP,ja;q=0.9"]),
            "Referer": random.choice([
                "https://www.google.com/", 
                "https://www.baidu.com/", 
                "https://bing.com/",
                "https://b1.qklm.xyz/"  # 模拟从b1跳转
            ]),
            "Cache-Control": random.choice(["max-age=0", "no-cache"]),
            "Connection": "keep-alive"
        }

    def simulate_visit(self, target_url):
        """模拟用户访问目标网站，加载静态资源，更新最后访问时间"""
        try:
            session = requests.Session()
            session.headers = self.get_random_headers()
            
            # 1. 访问主页（模拟首次加载）
            response = session.get(target_url, timeout=10)
            if response.status_code != 200:
                return False
            
            # 2. 解析并加载静态资源（数量随机波动，避免固定模式）
            soup = BeautifulSoup(response.text, "html.parser")
            assets = []
            # 提取CSS/JS/图片（优先加载关键资源）
            for tag in soup.find_all(["link", "script", "img"]):
                url = tag.get("href") or tag.get("src")
                if url and (url.endswith((".css", ".js", ".png", ".jpg", ".svg"))):
                    assets.append(urljoin(target_url, url))
            
            if assets:
                # 资源加载数量随机（2-4个，每次波动）
                num_assets = random.randint(2, min(4, len(assets)))
                for asset in random.sample(assets, num_assets):
                    # 加载延迟随机（0.2-1.2秒，更贴近真实网络波动）
                    time.sleep(random.uniform(0.2, 1.2))
                    session.get(asset, timeout=5)
            
            # 3. 随机模拟用户交互（概率波动，避免固定行为）
            interaction_prob = random.uniform(0.05, 0.15)  # 5%-15%概率点击
            if random.random() < interaction_prob:
                links = soup.find_all("a", href=True)
                if links and len(links) > 3:  # 确保有足够链接再点击
                    link_url = urljoin(target_url, random.choice(links)["href"])
                    # 点击前等待随机时间（1-3秒，模拟浏览后操作）
                    time.sleep(random.uniform(1, 3))
                    session.get(link_url, timeout=10)
            
            # 更新最后访问时间（核心：确保间隔不超12分钟）
            self.last_visited[target_url] = datetime.now()
            return True
        
        except Exception as e:
            return False

    def select_target(self):
        """选择下一个目标：优先处理即将超时的网站，否则随机选择"""
        now = datetime.now()
        # 检查是否有网站即将超时（超过10分钟未访问）
        for url in self.targets:
            elapsed = (now - self.last_visited[url]).total_seconds()
            if elapsed >= self.check_threshold:
                return url  # 优先访问即将超时的
        # 所有网站均在安全间隔内，随机选择（增加随机性）
        return random.choice(self.targets)

    def run(self):
        """主循环：持续运行保活逻辑"""
        while True:
            target = self.select_target()
            self.simulate_visit(target)
            # 下次访问等待时间（1-6分钟，随机分布更自然）
            wait_time = random.randint(self.min_wait, self.max_wait)
            time.sleep(wait_time)

if __name__ == "__main__":
    # 实例化服务并运行（无全局变量，避免状态污染）
    service = KeepAliveService()
    service.run()