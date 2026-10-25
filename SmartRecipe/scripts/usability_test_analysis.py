# Usability test quantitative analysis for SmartRecipe system
import csv
import numpy as np
import matplotlib.pyplot as plt

# 测试核心数据
TEST_GROUPS = {
    "control_group": {
        "label": "Traditional Text Recipe",
        "info_retrieval_efficiency": 100,
        "noisy_env_success_rate": 65.0,
        "user_trust_score": 60.5
    },
    "experiment_group": {
        "label": "SmartRecipe Multimodal System",
        "info_retrieval_efficiency": 140.0,
        "noisy_env_success_rate": 92.0,
        "user_trust_score": 92.1
    }
}

# 指标计算
def calculate_improvement(baseline, target):
    """计算实验组相对对照组的提升幅度"""
    return round((target - baseline) / baseline * 100, 1)

def generate_test_report():
    """生成可用性测试报告"""
    baseline = TEST_GROUPS["control_group"]
    exp = TEST_GROUPS["experiment_group"]
    
    print("=== SmartRecipe 可用性测试核心结果 ===")
    print(f"关键信息检索效率提升：{calculate_improvement(baseline['info_retrieval_efficiency'], exp['info_retrieval_efficiency'])}%")
    print(f"嘈杂环境操作成功率：{exp['noisy_env_success_rate']}%")
    print(f"用户信任度提升：{calculate_improvement(baseline['user_trust_score'], exp['user_trust_score'])}%")
    print()

def export_result_csv(output_path):
    """导出测试结果汇总表"""
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Control Group", "Experiment Group", "Improvement"])
        
        metrics = ["info_retrieval_efficiency", "noisy_env_success_rate", "user_trust_score"]
        labels = ["Key Info Retrieval Efficiency", "Noisy Env Operation Success Rate", "User Trust Score"]
        
        for metric, label in zip(metrics, labels):
            base = TEST_GROUPS["control_group"][metric]
            exp = TEST_GROUPS["experiment_group"][metric]
            improve = calculate_improvement(base, exp)
            writer.writerow([label, base, exp, f"+{improve}%"])

def plot_comparison(output_img_path):
    """绘制三组指标对比柱状图"""
    labels = ["Info Retrieval\nEfficiency", "Noisy Env\nSuccess Rate", "User Trust\nScore"]
    base_vals = [
        TEST_GROUPS["control_group"]["info_retrieval_efficiency"],
        TEST_GROUPS["control_group"]["noisy_env_success_rate"],
        TEST_GROUPS["control_group"]["user_trust_score"]
    ]
    exp_vals = [
        TEST_GROUPS["experiment_group"]["info_retrieval_efficiency"],
        TEST_GROUPS["experiment_group"]["noisy_env_success_rate"],
        TEST_GROUPS["experiment_group"]["user_trust_score"]
    ]
    
    x = np.arange(len(labels))
    width = 0.35
    
    plt.figure(figsize=(8, 5))
    plt.bar(x - width/2, base_vals, width, label='Traditional Recipe', color='#c4c4c4')
    plt.bar(x + width/2, exp_vals, width, label='SmartRecipe System', color='#7fb3d5')
    
    plt.xticks(x, labels)
    plt.ylabel('Score / Rate (%)')
    plt.title('Usability Test Result Comparison')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_img_path, dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    generate_test_report()
    export_result_csv("../results/usability_test_summary.csv")
    plot_comparison("../results/usability_comparison.png")
    print("可用性测试分析完成，结果已导出")
