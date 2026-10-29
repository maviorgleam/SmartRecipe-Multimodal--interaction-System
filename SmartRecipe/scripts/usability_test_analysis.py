import csv
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'configs'))
from usability_config import PLOT_CONFIG, METRIC_LABELS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEST_DATA_PATH = os.path.join(BASE_DIR, 'data', 'usability_test_data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_test_data(file_path):
    test_groups = {}
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            group_key = row['group']
            test_groups[group_key] = {
                "label": row['label'],
                "info_retrieval_efficiency": float(row['info_retrieval_efficiency']),
                "noisy_env_success_rate": float(row['noisy_env_success_rate']),
                "user_trust_score": float(row['user_trust_score'])
            }
    return test_groups

def calculate_improvement(baseline, target):
    return round((target - baseline) / baseline * 100, 1)

def generate_test_report(test_groups):
    baseline = test_groups["control_group"]
    exp = test_groups["experiment_group"]
    print("=== SmartRecipe 可用性测试核心结果 ===")
    print(f"关键信息检索效率提升：{calculate_improvement(baseline['info_retrieval_efficiency'], exp['info_retrieval_efficiency'])}%")
    print(f"嘈杂环境操作成功率：{exp['noisy_env_success_rate']}%")
    print(f"用户信任度提升：{calculate_improvement(baseline['user_trust_score'], exp['user_trust_score'])}%")
    print()

def export_result_csv(test_groups, output_path):
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Control Group", "Experiment Group", "Improvement"])
        metrics = ["info_retrieval_efficiency", "noisy_env_success_rate", "user_trust_score"]
        labels = ["Key Info Retrieval Efficiency", "Noisy Env Operation Success Rate", "User Trust Score"]
        baseline = test_groups["control_group"]
        exp = test_groups["experiment_group"]
        for metric, label in zip(metrics, labels):
            base_val = baseline[metric]
            exp_val = exp[metric]
            improve = calculate_improvement(base_val, exp_val)
            writer.writerow([label, base_val, exp_val, f"+{improve}%"])

def plot_comparison(test_groups, output_img_path):
    ctrl = test_groups["control_group"]
    exp = test_groups["experiment_group"]
    width = PLOT_CONFIG["bar_width"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=PLOT_CONFIG["figsize"])
    idx_labels = [METRIC_LABELS["info_retrieval_efficiency"]]
    idx_base = [ctrl["info_retrieval_efficiency"]]
    idx_exp = [exp["info_retrieval_efficiency"]]
    x1 = np.arange(len(idx_labels))
    b1 = ax1.bar(x1 - width/2, idx_base, width, label='Traditional Recipe', color=PLOT_CONFIG["control_color"])
    b2 = ax1.bar(x1 + width/2, idx_exp, width, label='SmartRecipe System', color=PLOT_CONFIG["experiment_color"])
    ax1.set_xticks(x1)
    ax1.set_xticklabels(idx_labels)
    ax1.set_ylabel(PLOT_CONFIG["efficiency_ylabel"])
    ax1.set_ylim(PLOT_CONFIG["efficiency_ylim"])
    ax1.set_title(PLOT_CONFIG["efficiency_title"])
    ax1.grid(axis='y', alpha=0.3)
    for b in (b1, b2):
        for rect in b:
            h = rect.get_height()
            ax1.annotate(f'{h:g}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                         textcoords='offset points', ha='center', va='bottom', fontsize=10)
    rate_labels = [METRIC_LABELS["noisy_env_success_rate"], METRIC_LABELS["user_trust_score"]]
    rate_base = [ctrl["noisy_env_success_rate"], ctrl["user_trust_score"]]
    rate_exp = [exp["noisy_env_success_rate"], exp["user_trust_score"]]
    x2 = np.arange(len(rate_labels))
    b3 = ax2.bar(x2 - width/2, rate_base, width, label='Traditional Recipe', color=PLOT_CONFIG["control_color"])
    b4 = ax2.bar(x2 + width/2, rate_exp, width, label='SmartRecipe System', color=PLOT_CONFIG["experiment_color"])
    ax2.set_xticks(x2)
    ax2.set_xticklabels(rate_labels)
    ax2.set_ylabel(PLOT_CONFIG["rate_ylabel"])
    ax2.set_ylim(PLOT_CONFIG["rate_ylim"])
    ax2.set_title(PLOT_CONFIG["rate_title"])
    ax2.grid(axis='y', alpha=0.3)
    for b in (b3, b4):
        for rect in b:
            h = rect.get_height()
            ax2.annotate(f'{h:g}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                         textcoords='offset points', ha='center', va='bottom', fontsize=10)
    fig.legend(loc='upper center', ncol=2, bbox_to_anchor=(0.5, 0.99), frameon=False)
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig(output_img_path, dpi=PLOT_CONFIG["dpi"], bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    test_groups = load_test_data(TEST_DATA_PATH)
    generate_test_report(test_groups)
    export_result_csv(test_groups, os.path.join(OUTPUT_DIR, 'usability_test_summary.csv'))
    plot_comparison(test_groups, os.path.join(OUTPUT_DIR, 'usability_comparison.png'))
    print("可用性测试分析完成，结果已导出")
