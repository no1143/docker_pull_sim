import time
import random
import sys

# ANSI color codes / ANSI 颜色代码
YELLOW = "\033[93m"  # Yellow for progress bar / 黄色用于进度条
GREEN = "\033[92m"   # Green for completion checkmark / 绿色用于完成对勾
RESET = "\033[0m"    # Reset color / 重置颜色

# Spinner frames / 动态旋转符号序列
SPINNER = ['⠋', '⠙', '⠸', '⠴', '⠦', '⠇']

# Braille fill order (bottom→top, left→right) / Braille 点位填充顺序（下→上，左→右）
FILL_ORDER = [7, 3, 2, 1, 8, 6, 5, 4]

# Braille dot masks / Braille 点位掩码
DOT_MASKS = {i: 1 << (i - 1) for i in range(1, 9)}
BRAILLE_BASE = 0x2800  # Unicode Braille base / Unicode Braille 起始码点

def braille_char(filled):
    """
    Construct a Braille character / 构造一个 Braille 字符
    filled: number of subcells filled (0~8) / 填充的小方块数量（0~8）
    """
    if filled <= 0:
        return chr(BRAILLE_BASE)
    if filled >= 8:
        return chr(BRAILLE_BASE | 0xFF)
    mask = sum(DOT_MASKS[FILL_ORDER[i]] for i in range(filled))
    return chr(BRAILLE_BASE | mask)

def braille_bar(ratio, cells=10):
    """
    Build a progress bar using Braille characters / 构造进度条（由多个 Braille 字符组成）
    ratio: progress ratio (0.0~1.0) / 当前进度（0.0~1.0）
    cells: number of Braille characters / 进度条长度（字符数）
    """
    total_subcells = cells * 8
    filled = int(ratio * total_subcells)
    full = filled // 8
    partial = filled % 8
    bar = [braille_char(8)] * full
    if full < cells:
        bar.append(braille_char(partial))
    bar += [braille_char(0)] * (cells - len(bar))
    return f"{YELLOW}{''.join(bar)}{RESET}"

def render_line(name, current, total, spin_index):
    """
    Render one line of progress info / 渲染一行进度信息
    name: component name / 组件名称
    current: current MB downloaded / 当前下载量（MB）
    total: total MB size / 总下载量（MB）
    spin_index: spinner frame index / 动画帧索引
    """
    ratio = min(current / total, 1.0)
    bar = braille_bar(ratio)
    size_text = f"{current:.1f}MB / {total:.1f}MB"
    if current < total:
        spin = SPINNER[spin_index % len(SPINNER)]
        return f"{spin} {name.ljust(15)} [{bar}] {size_text} Pulling"
    else:
        return f"{GREEN}✓{RESET} {name.ljust(15)} [{bar}] {size_text} Done"

def simulate_pull(name, total_mb):
    """
    Simulate Docker image pulling / 模拟 Docker 镜像拉取过程
    name: image name / 镜像名称
    total_mb: image size in MB / 镜像大小（MB）
    """
    current = 0.0
    spin_index = 0
    while current < total_mb:
        current = min(total_mb, current + random.uniform(5, 12))
        line = render_line(name, current, total_mb, spin_index)
        sys.stdout.write("\r" + line)
        sys.stdout.flush()
        spin_index += 1
        time.sleep(0.08)
    print("\r" + render_line(name, total_mb, total_mb, spin_index))

# Example usage / 示例调用
if __name__ == "__main__":
    simulate_pull("elasticsearch", 723.4)
