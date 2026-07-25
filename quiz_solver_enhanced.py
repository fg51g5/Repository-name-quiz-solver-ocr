import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
import time

# 初始化OCR
ocr = PaddleOCR(use_angle_cls=True, lang='ch')

def preprocess_image(img):
    """预处理图像以提高OCR准确度"""
    # 转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 增强对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    
    # 二值化
    _, binary = cv2.threshold(enhanced, 150, 255, cv2.THRESH_BINARY)
    
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)

def extract_text_with_confidence(img):
    """提取文字并过滤低置信度结果"""
    result = ocr.ocr(img, cls=True)
    
    text_data = []
    for line in result:
        for word_info in line:
            bbox, (text, confidence) = word_info
            if confidence > 0.7:  # 只保留置信度>70%的结果
                text_data.append({
                    'text': text,
                    'confidence': confidence,
                    'bbox': bbox
                })
    
    return text_data

def smart_option_detection(text_data):
    """智能检测选项"""
    lines_by_y = {}
    
    for item in text_data:
        y_coord = int(item['bbox'][0][1])
        if y_coord not in lines_by_y:
            lines_by_y[y_coord] = []
        lines_by_y[y_coord].append(item)
    
    # 按Y坐标排序并查找选项行
    options = {}
    for y in sorted(lines_by_y.keys()):
        line_items = sorted(lines_by_y[y], key=lambda x: x['bbox'][0][0])
        first_text = line_items[0]['text'].strip()
        
        if first_text in ['A', 'B', 'C', 'D']:
            # 合并这一行的所有文字
            line_text = ' '.join([item['text'] for item in line_items])
            options[first_text] = line_text.replace(first_text, '', 1).strip()
    
    return options

def main():
    print("=" * 50)
    print("增强版OCR识别工具")
    print("=" * 50)
    print("\n启动识别...\n")
    
    start = time.time()
    
    try:
        # 截屏
        print("[1/4] 正在截屏...")
        img = pyautogui.screenshot()
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        
        # 预处理
        print("[2/4] 正在预处理图像...")
        preprocessed = preprocess_image(img_cv)
        
        # OCR识别
        print("[3/4] 正在识别文字...")
        text_data = extract_text_with_confidence(preprocessed)
        
        # 检测选项
        print("[4/4] 正在检测选项...")
        options = smart_option_detection(text_data)
        
        elapsed = time.time() - start
        
        print("\n" + "=" * 50)
        print("【识别结果】")
        print("=" * 50)
        print(f"\n识别耗时: {elapsed:.2f}秒\n")
        print("识别到的选项:")
        for key, value in options.items():
            print(f"  {key}. {value}")
        
        # 保存预处理后的图像用于调试
        cv2.imwrite('preprocessed_quiz.png', preprocessed)
        cv2.imwrite('original_quiz.png', img_cv)
        print("\n已保存原始图像: original_quiz.png")
        print("已保存预处理图像: preprocessed_quiz.png")
        
    except Exception as e:
        print(f"\n❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
