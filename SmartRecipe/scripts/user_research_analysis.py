# User research data analysis for SmartRecipe multimodal interaction system
import csv
import numpy as np
from collections import defaultdict

SURVEY_DATA_PATH = "../data/user_survey_data.csv"
OUTPUT_PROFILE_PATH = "../results/user_profile_summary.csv"

MOSCOW_CATEGORIES = {
    "must_have": ["step-by-step guidance", "hands-free control"],
    "should_have": ["ingredient reminder", "cooking timer"],
    "could_have": ["recipe recommendation", "social sharing"],
    "won_t_have": ["video upload", "online purchase"]
}

#核心分析函数
def load_survey_data(file_path):
    """加载用户调研问卷数据"""
    user_data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_data.append(row)
    return user_data

def build_user_profiles(user_data):
    """基于调研数据构建典型用户画像"""
    profiles = defaultdict(lambda: {"count": 0, "core_needs": [], "pain_points": []})
    
    for user in user_data:
        cooking_freq = user["cooking_frequency"]
        profiles[cooking_freq]["count"] += 1
        profiles[cooking_freq]["core_needs"].append(user["top_need"])
        profiles[cooking_freq]["pain_points"].append(user["main_pain_point"])
    
    return profiles

def moscow_priority_analysis(user_data):
    """基于用户反馈统计 MoSCoW 需求优先级分布"""
    priority_stats = {k: 0 for k in MOSCOW_CATEGORIES.keys()}
    
    for user in user_data:
        user_need = user["top_need"]
        for level, needs in MOSCOW_CATEGORIES.items():
            if user_need in needs:
                priority_stats[level] += 1
                break
    
    total = len(user_data)
    priority_ratios = {k: round(v/total*100, 1) for k, v in priority_stats.items()}
    return priority_ratios

def export_summary(profiles, priorities, output_path):
    """导出分析结果汇总"""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Dimension", "Category", "Value"])
        writer.writerow(["MoSCoW Priority", "Must Have", f"{priorities['must_have']}%"])
        writer.writerow(["MoSCoW Priority", "Should Have", f"{priorities['should_have']}%"])
        writer.writerow(["MoSCoW Priority", "Could Have", f"{priorities['could_have']}%"])
        writer.writerow(["MoSCoW Priority", "Won't Have", f"{priorities['won_t_have']}%"])

if __name__ == "__main__":
    # 样本数据
    sample_users = [
        {"cooking_frequency": "frequent", "top_need": "step-by-step guidance", "main_pain_point": "hands busy while cooking"},
        {"cooking_frequency": "occasional", "top_need": "hands-free control", "main_pain_point": "too much information at once"},
        {"cooking_frequency": "beginner", "top_need": "ingredient reminder", "main_pain_point": "unclear operation steps"}
    ]
    
    profiles = build_user_profiles(sample_users)
    priorities = moscow_priority_analysis(sample_users)
    export_summary(profiles, priorities, OUTPUT_PROFILE_PATH)
    print("用户研究分析完成，结果已导出")
