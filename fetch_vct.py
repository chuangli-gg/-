import requests
import json

def fetch_vct_matches():
    # 稳稳加上了 ?status=upcoming 尾巴！
    url = "https://api.vlr.gg/api/v1/matches?status=upcoming"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("开始向官方数据源发起请求...")
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code != 200:
            print(f"接口请求失败，状态码: {response.status_code}")
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump([], f)
            return

        matches_data = response.json().get('data', [])
        s_tier_matches = []
        
        for match in matches_data:
            tournament = match.get('tournament', '').upper()
            # 过滤伦敦大师赛等顶级S级赛事
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
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(s_tier_matches[:10], f, ensure_ascii=False, indent=2)
        print(f"成功筛选出 {len(s_tier_matches)} 场比赛！")
            
    except Exception as e:
        print(f"抓取过程中发生未知错误: {e}")
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

if __name__ == "__main__":
    fetch_vct_matches()
