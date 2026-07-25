# 安装和配置指南

## 详细安装步骤

### 步骤 1：克隆仓库

```bash
git clone https://github.com/fg51g5/Repository-name-quiz-solver-ocr.git
cd Repository-name-quiz-solver-ocr
```

### 步骤 2：创建虚拟环境

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 步骤 3：安装依赖

```bash
pip install -r requirements.txt
```

⚠️ **首次运行会自动下载PaddleOCR模型，约200MB，请耐心等待**

### 步骤 4：运行程序

#### 选项 A：快捷键启动（推荐）

```bash
python hotkey_launcher.py
```

然后按 `Ctrl + Alt + Z` 来触发识别

#### 选项 B：直接运行

```bash
python quiz_solver.py
```

#### 选项 C：使用增强版本

```bash
python quiz_solver_enhanced.py
```

---

## 常见问题排查

### 问题 1：pip install 失败

**症状：** `error: Microsoft Visual C++ 14.0 or greater is required`

**解决方案：**
- Windows 用户需要安装 Visual C++ Build Tools
- 下载：https://visualstudio.microsoft.com/visual-cpp-build-tools/

### 问题 2：import paddleocr 失败

**症状：** `ModuleNotFoundError: No module named 'paddleocr'`

**解决方案：**
```bash
pip install --upgrade paddleocr
```

### 问题 3：快捷键不响应

**症状：** 按 Ctrl+Alt+Z 没反应

**解决方案：**
1. 确保 `hotkey_launcher.py` 正在运行
2. 尝试修改快捷键组合（编辑 `hotkey_launcher.py` 中的 `HOTKEY` 变量）
3. 检查快捷键是否与其他程序冲突

### 问题 4：OCR 识别不准确

**症状：** 识别的文字错误较多

**解决方案：**
1. 使用增强版本：`python quiz_solver_enhanced.py`
2. 调整屏幕分辨率和字体大小
3. 确保题目清晰可见，光线充足

### 问题 5：处理速度太慢

**症状：** 识别耗时超过 5 秒

**解决方案：**
1. 首次运行缓慢是正常的（需要加载模型）
2. 关闭其他占用 CPU 的程序
3. 升级电脑配置（更多 RAM 和 CPU 核心会有帮助）

---

## 自定义配置

### 修改快捷键

编辑 `hotkey_launcher.py`，找到这一行：

```python
HOTKEY = {keyboard.Key.ctrl_l, keyboard.Key.alt_l, keyboard.Key.z}
```

可用的键盘键：
- `keyboard.Key.ctrl_l` - 左 Ctrl
- `keyboard.Key.alt_l` - 左 Alt
- `keyboard.Key.shift_l` - 左 Shift
- `keyboard.Key.cmd` - Command (Mac)
- `keyboard.Key.a`, `keyboard.Key.b`, ... - 字母
- `keyboard.Key.f1`, `keyboard.Key.f2`, ... - 功能键

### 支持其他语言

编辑 `quiz_solver.py`，找到这一行：

```python
ocr = PaddleOCR(use_angle_cls=True, lang='ch')
```

改成：
- `lang='en'` - 英文
- `lang='es'` - 西班牙文
- `lang='fr'` - 法文
- `lang='de'` - 德文
- `lang='ja'` - 日文
- `lang='ko'` - 韩文

---

## 性能优化建议

### 1. 使用 GPU 加速（如果你有 NVIDIA GPU）

```bash
pip install paddlepaddle-gpu
```

### 2. 预加载模型

首次运行任何脚本时会自动下载并缓存模型，后续运行会更快

### 3. 调整 OCR 参数

编辑 `quiz_solver.py`：

```python
# 提高识别准确度（会变慢）
ocr = PaddleOCR(use_angle_cls=True, lang='ch', det_model_dir='...')

# 降低阈值以识别更多文字
# 找到 extract_text_with_confidence 函数，修改 confidence > 0.7
```

---

## 卸载

如果要完全卸载，只需：

```bash
# 停用虚拟环境
deactivate

# 删除项目文件夹
rm -rf Repository-name-quiz-solver-ocr  # Linux/Mac
rmdir /s Repository-name-quiz-solver-ocr  # Windows
```

---

## 获取帮助

如果遇到问题：

1. 查看本文件的"常见问题排查"部分
2. 查看生成的日志：`last_quiz.png`, `preprocessed_quiz.png`
3. 提交 Issue 到 GitHub 仓库

祝你使用愉快！🎉
