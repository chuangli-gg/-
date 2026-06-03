import requests
import json

def fetch_vct_matches():
    # 采用更兼容的直连赛事数据接口
    url = "https://api.vlr.gg/api/v1/matches？status=upcoming”
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("开始向官方数据源发起请求...")
        response = requests.get(url, headers=headers, timeout=20)
        
        # 如果接口返回的不是200成功状态
        if response.status_code != 200:
            print(f"接口请求失败，状态码: {response.status_code}")
            # 兜底：如果网络波动没抓到，生成一个空列表防止报错卡死
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
            return

        matches_data = response.json().get('data', [])
        s_tier_matches = []
        
        for match in matches_data:
            tournament = match.get('tournament', '').upper()
            # 过滤S级联赛和国际赛
            if any(kw in tournament for kw in ['VCT', 'CHAMPIONS', 'MASTERS', 'INTERNATIONAL', 'LONDON', '大师赛']):
                status = match.get('status', '未开始')
                if status == 'live': status = '直播中'
                elif status == 'upcoming': status = '即将开始'
                elif status == 'completed': status = '已结束'

                
                s_tier_matches.append({
                    "时间": match.get('time', '未知时间'),
                    "战队A": match.get('team1', 'TBD'),
                    "战队B": match.get('team2', 'TBD'),
                    "比分A": match.get('score1', '0'),
                    "比分B": match.get('score2', '0'),
                    "状态": status,
                    "赛事名称": match.get('tournament', 'VCT 顶级赛事')
                })
        
        # 无论有没有抓到，必须在本地稳稳地生成 data.json
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(s_tier_matches[:10], f, ensure_ascii=False, indent=2)
        print(f"成功筛选出 {len(s_tier_matches)} 场 S 级比赛并保存！")
            
    except Exception as e:
        print(f"抓取过程中发生未知错误: {e}")
        # 发生意外时同样生成空文件，确保全套流程能顺利跑完
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    fetch_vct_matches()
