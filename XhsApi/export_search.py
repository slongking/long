import json
import re
from typing import Dict, Any

def flatten_note(item: Dict[str, Any]) -> Dict[str, Any]:
    def clean(url: Any) -> str:
        if not isinstance(url, str):
            return str(url or "")
        m = re.search(r'>(https?://[^<]+)', url)
        return m.group(1) if m else url.strip()

    nc = item.get("note_card", {})
    user = nc.get("user", {})
    interact = nc.get("interact_info", {})
    cover = nc.get("cover", {})
    corner = nc.get("corner_tag_info", [])
    pub = next((t["text"] for t in corner if t.get("type") == "publish_time"), "")

    imgs = nc.get("image_list", [])
    flat = {
        "id": item.get("id"),
        "model_type": item.get("model_type"),
        "xsec_token": item.get("xsec_token"),

        "type": nc.get("type"),
        "display_title": nc.get("display_title"),

        "user_id": user.get("user_id"),
        "nickname": user.get("nickname") or user.get("nick_name"),
        "user_xsec_token": user.get("xsec_token"),
        "avatar_url": clean(user.get("avatar")),

        "liked": interact.get("liked"),
        "liked_count": int(str(interact.get("liked_count", 0)).replace(",", "")),
        "collected": interact.get("collected"),
        "collected_count": int(str(interact.get("collected_count", 0)).replace(",", "")),
        "comment_count": int(str(interact.get("comment_count", 0)).replace(",", "")),
        "shared_count": int(str(interact.get("shared_count", 0)).replace(",", "")),

        "cover_url_default": clean(cover.get("url_default")),
        "cover_url_pre": clean(cover.get("url_pre")),
        "cover_height": cover.get("height"),
        "cover_width": cover.get("width"),

        "publish_time_text": pub,
        "publish_time_type": "publish_time"
    }

    for idx, img in enumerate(imgs):
        flat[f"img_{idx}_height"] = img.get("height")
        flat[f"img_{idx}_width"] = img.get("width")
        flat[f"img_{idx}_url_dft"] = clean(next((u["url"] for u in img.get("info_list", []) if u.get("image_scene") == "WB_DFT"), ""))
        flat[f"img_{idx}_url_prv"] = clean(next((u["url"] for u in img.get("info_list", []) if u.get("image_scene") == "WB_PRV"), ""))

    return flat
result = []
with open('c','r',encoding='utf-8') as f:
    for line in f.readlines():
        result.append(json.loads(line))
import pandas as pd
df = pd.DataFrame(result)
df.to_excel('c.xlsx',index=False)