import csv
import sys
import os
from collections import defaultdict, Counter
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configs'))
from survey_config import SCALE_QUESTIONS, PAIN_KEYWORDS, MOSCOW_MAPPING

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SURVEY_DATA_PATH = os.path.join(BASE_DIR, 'data', 'user_survey_data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_survey_data(file_path):
    user_data = []
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k.strip()}
            user_data.append(cleaned_row)
    return user_data

def scale_analysis(user_data):
    scale_results = {}
    for q_key, q_desc in SCALE_QUESTIONS.items():
        scores = [int(user[q_key]) for user in user_data if user.get(q_key)]
        scale_results[q_key] = {
            "desc": q_desc,
            "mean": round(np.mean(scores), 2),
            "std": round(np.std(scores), 2),
            "n": len(scores)
        }
    return sorted(scale_results.items(), key=lambda x: x[1]["mean"], reverse=True)

def pain_point_analysis(user_data):
    pain_counter = Counter()
    for user in user_data:
        q7_text = user.get("Q7（摘要）", "")
        items = [item.strip() for item in q7_text.split("；") if item.strip()]
        for item in items:
            matched = False
            for pain_type, keywords in PAIN_KEYWORDS.items():
                if any(kw in item for kw in keywords):
                    pain_counter[pain_type] += 1
                    matched = True
                    break
            if not matched:
                pain_counter["other"] += 1
    return pain_counter.most_common()

def moscow_analysis(user_data):
    moscow_counter = {level: 0 for level in MOSCOW_MAPPING.keys()}
    total_users = len(user_data)
    for user in user_data:
        q8_text = user.get("Q8（摘要）", "")
        items = [item.strip() for item in q8_text.split("；") if item.strip()]
        matched_levels = set()
        for item in items:
            for level, info in MOSCOW_MAPPING.items():
                if any(kw in item for kw in info["keywords"]):
                    matched_levels.add(level)
        for level in matched_levels:
            moscow_counter[level] += 1
    return {
        level: {
            "label": info["label"],
            "count": moscow_counter[level],
            "ratio": round(moscow_counter[level] / total_users * 100, 1)
        }
        for level, info in MOSCOW_MAPPING.items()
    }

def build_user_profiles(user_data):
    profiles = defaultdict(lambda: {
        "count": 0,
        "pain_counter": Counter(),
        "need_counter": Counter()
    })
    for user in user_data:
        freq = user.get("每周下厨", "未知").strip()
        profiles[freq]["count"] += 1
        q7_items = [item.strip() for item in user.get("Q7（摘要）", "").split("；") if item.strip()]
        profiles[freq]["pain_counter"].update(q7_items)
        q8_items = [item.strip() for item in user.get("Q8（摘要）", "").split("；") if item.strip()]
        profiles[freq]["need_counter"].update(q8_items)
    return profiles

def export_all_results(scale_results, pain_results, moscow_results, profiles):
    with open(os.path.join(OUTPUT_DIR, 'scale_stats.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["排名", "题号", "问题描述", "均值", "标准差", "样本量"])
        for idx, (q_key, info) in enumerate(scale_results, 1):
            writer.writerow([idx, q_key, info["desc"], info["mean"], info["std"], info["n"]])

    with open(os.path.join(OUTPUT_DIR, 'pain_point_frequency.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["痛点类型", "提及人次"])
        for pain_type, count in pain_results:
            writer.writerow([pain_type, count])

    with open(os.path.join(OUTPUT_DIR, 'moscow_priority.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["优先级", "提及人数", "提及率"])
        for level, info in moscow_results.items():
            writer.writerow([info["label"], info["count"], f"{info['ratio']}%"])

    with open(os.path.join(OUTPUT_DIR, 'user_profile_segment.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["烹饪频率", "人数", "占比", "Top2痛点", "Top2需求"])
        total = sum(p["count"] for p in profiles.values())
        for freq, info in profiles.items():
            ratio = round(info["count"] / total * 100, 1)
            top_pains = "；".join([p for p, _ in info["pain_counter"].most_common(2)])
            top_needs = "；".join([n for n, _ in info["need_counter"].most_common(2)])
            writer.writerow([freq, info["count"], f"{ratio}%", top_pains, top_needs])

def print_summary(scale_results, pain_results, moscow_results, profiles):
    total_n = sum(p["count"] for p in profiles.values())
    print("="*60)
    print(f"SmartRecipe 用户调研分析报告（样本量 N={total_n}）")
    print("="*60)
    print("\n【量表题痛点认同度排名】")
    for idx, (q_key, info) in enumerate(scale_results, 1):
        print(f"{idx}. {info['desc']} — 均值 {info['mean']}")
    print("\n【开放题痛点提及人次排名】")
    for pain_type, count in pain_results:
        print(f"- {pain_type}: {count} 人次")
    print("\n【MoSCoW 需求优先级提及率】")
    for level, info in moscow_results.items():
        print(f"- {info['label']}: {info['ratio']}%")
    print("\n【用户分层画像概览】")
    total = sum(p["count"] for p in profiles.values())
    for freq, info in profiles.items():
        print(f"- 每周下厨{freq}：{info['count']}人（{round(info['count']/total*100,1)}%）")

if __name__ == "__main__":
    user_data = load_survey_data(SURVEY_DATA_PATH)
    scale_results = scale_analysis(user_data)
    pain_results = pain_point_analysis(user_data)
    moscow_results = moscow_analysis(user_data)
    profiles = build_user_profiles(user_data)
    print_summary(scale_results, pain_results, moscow_results, profiles)
    export_all_results(scale_results, pain_results, moscow_results, profiles)
    print(f"\n分析完成，结果已导出至 {OUTPUT_DIR} 文件夹")
