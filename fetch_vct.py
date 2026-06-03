import requests
import json

def fetch_vct_matches():
    # 这是一个提供最新无畏契约赛事的公开接口
    url = "https://api.vlr.gg/api/v1/matches" 
    
    try:
        response = requests.get(url, timeout=15)
        matches_data = response.json().get('data', [])
        
        s_tier_matches = []
        
        for match in matches_data:
            tournament = match.get('tournament', '').upper()
            # 自动过滤：只保留包含 VCT、Masters(大师赛)、Champions(冠军赛) 的顶级S级比赛
            if any(kw in tournament for kw in ['VCT', 'CHAMPIONS', 'MASTERS', 'INTERNATIONAL']):
                
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
        
        # 保存为本地的 json 数据文件
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(s_tier_matches[:10], f, ensure_ascii=False, indent=2)
            print("高级赛事数据同步成功！")
            
    except Exception as e:
        print(f"抓取失败: {e}")

if __name__ == "__main__":
    fetch_vct_matches()
