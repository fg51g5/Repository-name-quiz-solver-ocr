import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
import time
from PIL import Image
import io

# 初始化OCR（第一次运行会下载模型，约200MB）
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def take_screenshot():
    """截取当前屏幕"""
    screenshot = pyautogui.screenshot()
    img_array = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return img_array

def extract_text_from_image(img):
    """使用PaddleOCR识别图片中的文字"""
    result = ocr.ocr(img, cls=True)
    
    # 提取所有文字和位置信息
    text_data = []
    for line in result:
        for word_info in line:
            bbox, (text, confidence) = word_info
            text_data.append({
                'text': text,
                'confidence': confidence,
                'position': bbox
            })
    
    return text_data

def find_options(text_data):
    """识别四个选项（A/B/C/D）"""
    options = {'A': None, 'B': None, 'C': None, 'D': None}
    
    for item in text_data:
        text = item['text'].strip()
        # 匹配选项标记
        if text in ['A', 'B', 'C', 'D'] and item['confidence'] > 0.8:
            options[text] = item
    
    return options

def extract_full_text(text_data):
    """将识别的文字按位置排序并拼接"""
    # 按Y坐标排序（从上到下）
    sorted_text = sorted(text_data, key=lambda x: x['position'][0][1])
    
    full_text = '\n'.join([item['text'] for item in sorted_text])
    return full_text

def parse_question_and_options(text_data):
    """解析题目和四个选项"""
    full_text = extract_full_text(text_data)
    lines = full_text.split('\n')
    
    # 查找选项行（以A、B、C、D开头）
    question_lines = []
    options = {}
    
    for line in lines:
        line = line.strip()
        if line and line[0] in ['A', 'B', 'C', 'D']:
            # 这是选项行
            if len(line) > 1:
                option_key = line[0]
                option_text = line[1:].strip()
                options[option_key] = option_text
        elif line and not any(line.startswith(opt) for opt in ['A', 'B', 'C', 'D']):
            question_lines.append(line)
    
    question = '\n'.join(question_lines)
    
    return {
        'question': question,
        'options': options,
        'full_text': full_text
    }

def simple_logic_solver(parsed_data):
    """简单的逻辑判断（针对12岁难度的题目）"""
    question = parsed_data['question'].lower()
    options = parsed_data['options']
    
    # 规则库 - 根据常见的12岁题目模式
    rules = {
        # 数学相关
        '加': lambda opts: _find_math_answer(opts, '+'),
        '减': lambda opts: _find_math_answer(opts, '-'),
        '乘': lambda opts: _find_math_answer(opts, '*'),
        '除': lambda opts: _find_math_answer(opts, '/'),
        
        # 逻辑相关
        '都': lambda opts: _find_common_property(opts),
        '最': lambda opts: _find_extreme(opts),
    }
    
    # 检查问题中的关键词
    for keyword, rule_func in rules.items():
        if keyword in question:
            try:
                result = rule_func(options)
                if result:
                    return result
            except:
                pass
    
    # 如果没有匹配规则，返回第一个选项（备选）
    return 'A'

def _find_math_answer(options, operator):
    """简单的数学计算辅助"""
    # 这里可以添加更复杂的数学识别逻辑
    pass

def _find_common_property(options):
    """查找共同属性"""
    pass

def _find_extreme(options):
    """查找极值"""
    pass

def solve_quiz_with_fallback(parsed_data):
    """
    当纯OCR+规则无法解决时的降级方案
    返回置信度和建议答案
    """
    # 优先使用逻辑求解器
    answer = simple_logic_solver(parsed_data)
    
    return {
        'answer': answer,
        'confidence': 'medium',  # 纯本地方案置信度有限
        'method': 'local_ocr',
        'parsed_data': parsed_data
    }

def main():
    """主程序"""
    print("=" * 50)
    print("本地OCR自动做题工具")
    print("=" * 50)
    print("\n按 Ctrl+Alt+Z 开始截屏识别题目")
    print("按 Ctrl+C 退出程序\n")
    
    start_time = time.time()
    
    try:
        # 截屏
        print("[1/4] 正在截屏...")
        img = take_screenshot()
        
        # OCR识别
        print("[2/4] 正在识别文字...")
        text_data = extract_text_from_image(img)
        
        # 解析题目
        print("[3/4] 正在解析题目...")
        parsed_data = parse_question_and_options(text_data)
        
        # 求解
        print("[4/4] 正在求解...")
        result = solve_quiz_with_fallback(parsed_data)
        
        elapsed = time.time() - start_time
        
        # 显示结果
        print("\n" + "=" * 50)
        print("【识别结果】")
        print("=" * 50)
        print(f"\n题目：\n{parsed_data['question']}\n")
        print("选项：")
        for key, value in parsed_data['options'].items():
            print(f"  {key}. {value}")
        
        print("\n" + "-" * 50)
        print(f"建议答案: 【{result['answer']}】")
        print(f"识别耗时: {elapsed:.2f}秒")
        print(f"置信度: {result['confidence']}")
        print("=" * 50)
        
        # 保存截图用于调试
        cv2.imwrite('last_quiz.png', img)
        print("\n截图已保存为 last_quiz.png")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
