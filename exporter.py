import json
import os
from datetime import datetime

class RoFinderExporter:
    def __init__(self):
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def export_json(self, data, filename):
        
        if not filename.endswith('.json'):
            filename += '.json'
        
        final_data = {
            "meta": {
                "generated_at": self.timestamp,
                "tool": "RoFinder v2.2.0"
            },
            "data": data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(final_data, f, indent=4)
        return os.path.abspath(filename)

    def export_txt(self, data, filename):

        if not filename.endswith('.txt'):
            filename += '.txt'

        user = data['profile']
        stats = data['stats']
        
        lines = [
            "============================================",
            f" ROFINDER INTELLIGENCE REPORT",
            f" Generated: {self.timestamp}",
            "============================================",
            "",
            "[ BASIC INFORMATION ]",
            f" Username:     {user.get('name')}",
            f" Display Name: {user.get('displayName')}",
            f" User ID:      {user.get('id')}",
            f" Created:      {user.get('created')}",
            f" Is Banned:    {user.get('isBanned')}",
            "",
            "[ STATISTICS ]",
            f" Friends:      {stats.get('friends')}",
            f" Followers:    {stats.get('followers')}",
            f" Following:    {stats.get('following')}",
            "",
            "[ AVATAR ]",
            f" Headshot URL: {data.get('avatar_url')}",
            ""
        ]

        if 'assets' in data and data['assets']:
            lines.append("[ CURRENTLY WEARING ]")
            for asset in data['assets']:
                lines.append(f" - {asset['name']} ({asset['assetType']['name']})")
                lines.append(f"   Link: https://www.roblox.com/catalog/{asset['id']}")
            lines.append("")

        if 'favorites' in data and data['favorites']:
            lines.append("[ FAVORITE GAMES ]")
            for game in data['favorites']:
                lines.append(f" - {game['name']} (By {game['creatorName']})")
            lines.append("")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        return os.path.abspath(filename)