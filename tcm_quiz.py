import json
import random
import time
import os

class TCMQuiz:
    def __init__(self, data_path):
        self.data_path = data_path
        self.questions = []
        self.load_data()
        self.score = 0
        self.total_questions = 0
        
    def load_data(self):
        """加载中医问答数据集"""
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.questions = json.load(f)
            print(f"成功加载 {len(self.questions)} 个中医问题")
        except Exception as e:
            print(f"加载数据时出错: {e}")
            
    def get_random_question(self):
        """随机获取一个问题"""
        if not self.questions:
            return None
        return random.choice(self.questions)
    
    def get_questions_batch(self, batch_size=10):
        """获取一批问题"""
        if not self.questions:
            return []
        return random.sample(self.questions, min(batch_size, len(self.questions)))
    
    def display_question(self, question):
        """显示问题和选项"""
        print("\n" + "="*80)
        print(f"问题: {question['question']}")
        print("-"*80)
        print(f"A. {question['A']}")
        print(f"B. {question['B']}")
        print(f"C. {question['C']}")
        print(f"D. {question['D']}")
        print("="*80)
        
    def check_answer(self, question, user_answer):
        """检查答案是否正确"""
        correct_answer = question['label']
        is_correct = user_answer.upper() == correct_answer
        
        self.total_questions += 1
        if is_correct:
            self.score += 1
            print("\n✓ 回答正确!")
        else:
            print(f"\n✗ 回答错误! 正确答案是: {correct_answer}")
        
        print(f"当前分数: {self.score}/{self.total_questions} ({self.score/self.total_questions*100:.1f}%)")
        return is_correct
    
    def run_quiz(self, num_questions=10):
        """运行测验"""
        if not self.questions:
            print("没有可用的问题，请检查数据文件")
            return
        
        batch = self.get_questions_batch(num_questions)
        
        print(f"\n== 中医传统医学知识测验 ==")
        print(f"将随机抽取 {len(batch)} 个问题进行测试")
        print("输入选项(A/B/C/D)回答问题，输入Q退出")
        
        for i, question in enumerate(batch):
            print(f"\n问题 {i+1}/{len(batch)}")
            self.display_question(question)
            
            while True:
                user_input = input("你的答案是: ").strip().upper()
                if user_input == 'Q':
                    print("退出测验")
                    return
                if user_input in ['A', 'B', 'C', 'D']:
                    self.check_answer(question, user_input)
                    time.sleep(1)  # 给用户时间查看结果
                    break
                else:
                    print("请输入有效选项: A, B, C, D 或 Q(退出)")
        
        print(f"\n测验结束! 最终分数: {self.score}/{self.total_questions} ({self.score/self.total_questions*100:.1f}%)")

    def practice_mode(self):
        """练习模式 - 持续提问，直到用户退出"""
        if not self.questions:
            print("没有可用的问题，请检查数据文件")
            return
        
        print("\n== 中医传统医学知识练习模式 ==")
        print("输入选项(A/B/C/D)回答问题，输入Q退出")
        
        question_count = 0
        while True:
            question = self.get_random_question()
            question_count += 1
            print(f"\n问题 #{question_count}")
            self.display_question(question)
            
            while True:
                user_input = input("你的答案是: ").strip().upper()
                if user_input == 'Q':
                    print("退出练习模式")
                    return
                if user_input in ['A', 'B', 'C', 'D']:
                    self.check_answer(question, user_input)
                    time.sleep(1)  # 给用户时间查看结果
                    break
                else:
                    print("请输入有效选项: A, B, C, D 或 Q(退出)")

def main():
    data_path = "dataset/CMMLU-Traditional-Chinese-Medicine-Benchmark/traditional_chinese_medicine.json"
    
    # 如果文件不存在，尝试使用相对路径
    if not os.path.exists(data_path):
        data_path = "traditional_chinese_medicine.json"
    
    quiz = TCMQuiz(data_path)
    
    while True:
        print("\n请选择模式:")
        print("1. 测验模式 (10题)")
        print("2. 练习模式 (无限题)")
        print("3. 退出")
        
        choice = input("输入选择 (1/2/3): ").strip()
        
        if choice == '1':
            quiz.run_quiz(10)
        elif choice == '2':
            quiz.practice_mode()
        elif choice == '3':
            print("感谢使用! 再见!")
            break
        else:
            print("无效选择，请重试")

if __name__ == "__main__":
    main() 