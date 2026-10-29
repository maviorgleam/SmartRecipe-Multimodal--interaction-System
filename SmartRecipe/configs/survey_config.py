SCALE_QUESTIONS = {
    "Q1": "Hands dirty/oily makes phone operation troublesome",
    "Q2": "Dense recipe text makes key info hard to find while cooking",
    "Q3": "Kitchen noise makes timer reminders hard to hear",
    "Q4": "Cross-app search for unknown ingredients is cumbersome",
    "Q5": "Need to see AI confidence and correct recognition errors",
    "Q6": "Unwilling to leave the stove frequently to operate phone"
}

PAIN_KEYWORDS = {
    "hands_occupied_operation": ["手脏", "油污", "碰手机", "擦手", "离开灶台", "来回跑", "屏幕沾油", "手上有水", "手上有水不敢点屏幕"],
    "information_overload": ["文字太多", "难找", "密密麻麻", "信息多", "找关键信息费力", "步骤混杂", "大段文字", "信息过载"],
    "noisy_environment": ["噪音", "听不清", "语音失效", "计时器听不到", "语音听不清", "语音容易出错", "语音识别不稳定"],
    "ingredient_recognition_trouble": ["搜食材", "识别食材麻烦", "跨软件", "陌生食材", "切换App", "识别食材", "切换 App"],
    "ai_trust_issue": ["不信任AI", "识别出错", "怕识别错", "语音容易出错", "不信任 AI", "AI 结果"]
}

MOSCOW_MAPPING = {
    "must_have": {
        "keywords": ["语音控制", "免手操作", "分步导航", "双模式", "步骤导航", "语音导航", "不用频繁点屏幕", "语音", "看简要步骤", "显示简要步骤", "只展示当前烹饪步骤", "简要步骤", "当前烹饪步骤"],
        "label": "Must Have"
    },
    "should_have": {
        "keywords": ["食材识别", "拍照", "置信度", "修正AI", "一键修改", "计时器", "震动提醒", "AI 告诉我", "识别把握", "可以修正", "识别不认识食材", "拍照识别"],
        "label": "Should Have"
    },
    "could_have": {
        "keywords": ["推荐", "分享", "食材提醒"],
        "label": "Could Have"
    },
    "won_t_have": {
        "keywords": ["视频上传", "网购"],
        "label": "Won't Have"
    }
}
