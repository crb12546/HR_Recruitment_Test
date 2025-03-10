"""
创建测试数据脚本
"""
import os
import sys
import json
from datetime import datetime

# 创建测试职位需求数据
def create_test_job_requirements():
    """创建测试职位需求数据"""
    print("创建测试职位需求数据...")
    job_requirements = [
        {
            "position_name": "Python后端开发工程师",
            "department": "技术部",
            "location": "北京",
            "salary_range": "20k-30k",
            "experience": "3-5年",
            "education": "本科及以上",
            "description": "负责公司核心业务系统的开发和维护",
            "requirements": "熟练掌握Python编程语言，熟悉FastAPI或Flask框架",
            "created_at": datetime.now().isoformat()
        },
        {
            "position_name": "前端开发工程师",
            "department": "技术部",
            "location": "上海",
            "salary_range": "15k-25k",
            "experience": "2-4年",
            "education": "本科及以上",
            "description": "负责公司Web前端开发和维护",
            "requirements": "熟练掌握HTML、CSS、JavaScript，熟悉Vue.js或React框架",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # 保存到文件
    with open("test_data/job_requirements.json", "w", encoding="utf-8") as f:
        json.dump(job_requirements, f, ensure_ascii=False, indent=2)
    
    print(f"已创建{len(job_requirements)}条测试职位需求数据")
    return job_requirements

# 创建测试简历数据
def create_test_resumes():
    """创建测试简历数据"""
    print("创建测试简历数据...")
    resumes = [
        {
            "name": "张三",
            "gender": "男",
            "age": 28,
            "phone": "13800138001",
            "email": "zhangsan@example.com",
            "education": "本科",
            "university": "北京大学",
            "major": "计算机科学与技术",
            "experience": "5年",
            "skills": ["Python", "FastAPI", "MySQL", "Redis", "Docker"],
            "self_evaluation": "有丰富的后端开发经验，熟悉分布式系统设计",
            "created_at": datetime.now().isoformat()
        },
        {
            "name": "李四",
            "gender": "女",
            "age": 26,
            "phone": "13800138002",
            "email": "lisi@example.com",
            "education": "硕士",
            "university": "清华大学",
            "major": "软件工程",
            "experience": "3年",
            "skills": ["JavaScript", "Vue.js", "React", "HTML", "CSS"],
            "self_evaluation": "有良好的前端开发经验，熟悉现代前端框架",
            "created_at": datetime.now().isoformat()
        }
    ]
    
    # 保存到文件
    with open("test_data/resumes.json", "w", encoding="utf-8") as f:
        json.dump(resumes, f, ensure_ascii=False, indent=2)
    
    print(f"已创建{len(resumes)}条测试简历数据")
    return resumes

# 创建测试匹配结果数据
def create_test_matches(job_requirements, resumes):
    """创建测试匹配结果数据"""
    print("创建测试匹配结果数据...")
    matches = []
    
    # 简单匹配逻辑
    for job in job_requirements:
        for resume in resumes:
            # 后端职位与后端简历匹配
            if "Python" in job["position_name"] and "Python" in resume["skills"]:
                score = 85
                explanation = "候选人技能与职位要求高度匹配"
            # 前端职位与前端简历匹配
            elif "前端" in job["position_name"] and ("Vue.js" in resume["skills"] or "React" in resume["skills"]):
                score = 80
                explanation = "候选人技能与职位要求匹配度较高"
            # 其他情况
            else:
                score = 60
                explanation = "候选人基本符合职位要求，但匹配度一般"
            
            matches.append({
                "job_id": job_requirements.index(job) + 1,
                "resume_id": resumes.index(resume) + 1,
                "position_name": job["position_name"],
                "candidate_name": resume["name"],
                "match_score": score,
                "match_explanation": explanation,
                "created_at": datetime.now().isoformat()
            })
    
    # 保存到文件
    with open("test_data/matches.json", "w", encoding="utf-8") as f:
        json.dump(matches, f, ensure_ascii=False, indent=2)
    
    print(f"已创建{len(matches)}条测试匹配结果数据")
    return matches

# 创建测试招聘方案数据
def create_test_plans(job_requirements, matches):
    """创建测试招聘方案数据"""
    print("创建测试招聘方案数据...")
    plans = []
    
    # 按职位分组
    job_matches = {}
    for match in matches:
        job_id = match["job_id"]
        if job_id not in job_matches:
            job_matches[job_id] = []
        job_matches[job_id].append(match)
    
    # 为每个职位创建招聘方案
    for job_id, job_matches_list in job_matches.items():
        job = job_requirements[job_id - 1]
        
        # 按匹配分数排序
        sorted_matches = sorted(job_matches_list, key=lambda x: x["match_score"], reverse=True)
        
        # 选择前3名候选人
        top_candidates = sorted_matches[:min(3, len(sorted_matches))]
        
        plan = {
            "job_id": job_id,
            "position_name": job["position_name"],
            "department": job["department"],
            "candidates": top_candidates,
            "recruitment_strategy": f"针对{job['position_name']}职位的招聘策略",
            "interview_questions": [
                "请介绍一下你的工作经历",
                "你认为自己最大的优势是什么",
                "你对我们公司了解多少"
            ],
            "timeline": {
                "resume_screening": "1周",
                "first_interview": "2周",
                "second_interview": "3周",
                "offer": "4周"
            },
            "created_at": datetime.now().isoformat()
        }
        
        plans.append(plan)
    
    # 保存到文件
    with open("test_data/plans.json", "w", encoding="utf-8") as f:
        json.dump(plans, f, ensure_ascii=False, indent=2)
    
    print(f"已创建{len(plans)}条测试招聘方案数据")
    return plans

# 主函数
def main():
    """主函数"""
    # 创建测试数据目录
    os.makedirs("test_data", exist_ok=True)
    
    # 创建测试数据
    job_requirements = create_test_job_requirements()
    resumes = create_test_resumes()
    matches = create_test_matches(job_requirements, resumes)
    plans = create_test_plans(job_requirements, matches)
    
    print("测试数据创建完成")

if __name__ == "__main__":
    main()
