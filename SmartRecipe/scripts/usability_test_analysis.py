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
            if metric == "noisy_env_success_rate":
                writer.writerow([label, base_val, exp_val, "-"])
            else:
                improve = calculate_improvement(base_val, exp_val)
                writer.writerow([label, base_val, exp_val, f"+{improve}%"])

def plot_comparison(test_groups, output_img_path):
    ctrl = test_groups["control_group"]
    exp = test_groups["experiment_group"]
    width = PLOT_CONFIG["bar_width"]
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=PLOT_CONFIG["figsize"])
    panels = [
        (ax1, "info_retrieval_efficiency", METRIC_LABELS["info_retrieval_efficiency"],
         PLOT_CONFIG["efficiency_title"], PLOT_CONFIG["efficiency_ylabel"], PLOT_CONFIG["efficiency_ylim"]),
        (ax2, "noisy_env_success_rate", METRIC_LABELS["noisy_env_success_rate"],
         PLOT_CONFIG["success_title"], PLOT_CONFIG["success_ylabel"], PLOT_CONFIG["success_ylim"]),
        (ax3, "user_trust_score", METRIC_LABELS["user_trust_score"],
         PLOT_CONFIG["trust_title"], PLOT_CONFIG["trust_ylabel"], PLOT_CONFIG["trust_ylim"])
    ]
    for ax, metric, label, title, ylabel, ylim in panels:
        x = np.arange(1)
        b1 = ax.bar(x - width/2, [ctrl[metric]], width, label='Traditional Recipe', color=PLOT_CONFIG["control_color"])
        b2 = ax.bar(x + width/2, [exp[metric]], width, label='SmartRecipe System', color=PLOT_CONFIG["experiment_color"])
        ax.set_xticks(x)
        ax.set_xticklabels([label])
        ax.set_ylabel(ylabel)
        ax.set_ylim(ylim)
        ax.set_title(title)
        ax.grid(axis='y', alpha=0.3)
        for b in (b1, b2):
            for rect in b:
                h = rect.get_height()
                ax.annotate(f'{h:g}', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3),
                            textcoords='offset points', ha='center', va='bottom', fontsize=10)
    fig.legend(loc='lower center', ncol=2, bbox_to_anchor=(0.5, -0.05), frameon=False)
    plt.tight_layout(rect=[0, 0, 1, 1])
    plt.savefig(output_img_path, dpi=PLOT_CONFIG["dpi"], bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    test_groups = load_test_data(TEST_DATA_PATH)
    generate_test_report(test_groups)
    export_result_csv(test_groups, os.path.join(OUTPUT_DIR, 'usability_test_summary.csv'))
    plot_comparison(test_groups, os.path.join(OUTPUT_DIR, 'usability_comparison.png'))
    print("可用性测试分析完成，结果已导出")
