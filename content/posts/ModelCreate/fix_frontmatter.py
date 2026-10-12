#!/usr/bin/env python3
"""
批量修复 ModelCreate 目录下所有 .md 文件的 front matter。

修复内容：
  1. 变体 A（扁平 image）→ 转为 cover 对象格式
  2. 变体 B（cover 对象）→ 补全 alt/caption、统一 URL 参数
  3. 变体 C（有 front matter 无 image/cover）→ 补 cover 占位
  4. 变体 D（完全无 front matter）→ 从文件名和首行标题生成完整 front matter
  5. 所有 _index.md → 补 description（如缺失）
  6. 统一 image URL 参数为 ?w=1200&q=80
  7. 统一字段顺序

用法：
  python3 fix_frontmatter.py            # 干跑模式（默认，只打印不修改）
  python3 fix_frontmatter.py --apply    # 实际执行修改
"""

import os
import re
import sys
import unicodedata
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ============================================================
# 工具函数
# ============================================================

def normalize_image_url(url: str) -> str:
    """统一 Unsplash URL 参数为 ?w=1200&q=80"""
    if not url:
        return url
    # 移除所有现有 query 参数
    url = re.sub(r'\?[^"\s]*$', '', url)
    # 添加标准参数
    return f'{url}?w=1200&q=80'


def extract_front_matter(content: str):
    """解析 front matter，返回 (front_matter_dict, body)。无 front matter 则返回 (None, content)"""
    if not content.startswith('---'):
        return None, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content

    fm_text = parts[1]
    body = parts[2]

    # 简易 YAML 解析（足够处理这些文件的简单结构）
    fm = {}
    current_key = None
    current_sub = None

    for line in fm_text.strip().split('\n'):
        # 顶层 key: value
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m and not line.startswith(' '):
            key, val = m.group(1), m.group(2).strip()
            if val:
                fm[key] = val.strip('"')
            else:
                fm[key] = {}  # 可能是嵌套对象
            current_key = key
            current_sub = None
            continue

        # 子级 key: value（如 cover 下的字段）
        m = re.match(r'^\s+(\w+):\s*(.*)', line)
        if m and current_key:
            sub_key, sub_val = m.group(1), m.group(2).strip()
            if not isinstance(fm[current_key], dict):
                fm[current_key] = {}
            fm[current_key][sub_key] = sub_val.strip('"')
            current_sub = sub_key
            continue

    return fm, body


def build_front_matter(fm: dict, is_index: bool = False) -> str:
    """从 dict 生成标准格式的 front matter YAML 文本"""
    lines = ['---']

    if is_index:
        # _index.md: title, date, draft, description
        for key in ['title', 'date', 'draft', 'description']:
            if key in fm:
                val = fm[key]
                if isinstance(val, str) and not val.startswith('"') and not val.startswith("'"):
                    # 含特殊字符的加引号
                    if any(c in val for c in ':#{}[],&*?|>!%@`'):
                        val = f'"{val}"'
                lines.append(f'{key}: {val}')
    else:
        # 文章: title, date, weight, draft, cover
        for key in ['title', 'date', 'weight', 'draft']:
            if key in fm:
                val = fm[key]
                if isinstance(val, str) and not val.startswith('"') and not val.startswith("'"):
                    if any(c in val for c in ':#{}[],&*?|>!%@`'):
                        val = f'"{val}"'
                lines.append(f'{key}: {val}')

        if 'cover' in fm and isinstance(fm['cover'], dict):
            cover = fm['cover']
            lines.append('cover:')
            for sub_key in ['image', 'alt', 'caption']:
                if sub_key in cover:
                    val = cover[sub_key]
                    lines.append(f'  {sub_key}: "{val}"')

    lines.append('---')
    return '\n'.join(lines)


def generate_alt_from_title(title: str) -> str:
    """从标题生成 alt 文本（去掉副标题、特殊符号）"""
    # 去掉冒号后面的内容、破折号后面的内容
    alt = re.split(r'[：:—–]', title)[0].strip()
    # 去掉书名号
    alt = alt.replace('《', '').replace('》', '')
    return alt if alt else title


def generate_caption_from_title(title: str) -> str:
    """从标题生成 caption"""
    return f'「{title}」相关主题配图'


def extract_weight_from_filename(filename: str):
    """从文件名提取 weight 数字"""
    m = re.match(r'^(\d+)-', filename)
    return int(m.group(1)) if m else None


def extract_title_from_filename(filename: str) -> str:
    """从文件名提取标题（去掉数字前缀和 .md 后缀）"""
    name = filename.replace('.md', '')
    m = re.match(r'^\d+-(.+)$', name)
    return m.group(1) if m else name


def get_first_heading(content: str) -> str:
    """从正文提取第一个 # 标题"""
    m = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return m.group(1).strip() if m else ''


def get_category_name(filepath: Path) -> str:
    """获取文件所属分类名"""
    return filepath.parent.name


# ============================================================
# 修复逻辑
# ============================================================

def fix_article(filepath: Path, dry_run: bool = True) -> dict:
    """修复单篇文章，返回修复报告"""
    report = {
        'file': str(filepath.relative_to(BASE_DIR)),
        'variant': '',
        'changes': [],
    }

    content = filepath.read_text(encoding='utf-8')
    filename = filepath.name

    fm, body = extract_front_matter(content)

    if fm is None:
        # 变体 D：完全无 front matter
        report['variant'] = 'D (无front matter)'
        title = get_first_heading(content) or extract_title_from_filename(filename)
        weight = extract_weight_from_filename(filename)
        # 从正文找第一个配图 URL
        img_match = re.search(r'!\[.*?\]\((https://images\.unsplash\.com/[^)]+)\)', content)
        img_url = normalize_image_url(img_match.group(1)) if img_match else 'TODO_REPLACE_WITH_REAL_URL'

        fm = {
            'title': title,
            'date': '2026-08-25',  # 默认日期
            'weight': weight,
            'draft': 'false',
            'cover': {
                'image': img_url,
                'alt': generate_alt_from_title(title),
                'caption': generate_caption_from_title(title),
            }
        }
        report['changes'].append('生成完整 front matter')
        report['changes'].append(f'  title: {title}')
        report['changes'].append(f'  weight: {weight}')
        report['changes'].append(f'  cover.image: {img_url[:60]}...')

    elif isinstance(fm.get('cover'), dict):
        # 变体 B：cover 对象已存在，检查是否需要补全
        report['variant'] = 'B (cover对象)'
        cover = fm['cover']

        if 'image' in cover:
            old_url = cover['image']
            new_url = normalize_image_url(old_url)
            if old_url != new_url:
                report['changes'].append(f'URL 参数标准化: ...{old_url[-30:]} -> ...{new_url[-30:]}')
                cover['image'] = new_url

        if 'alt' not in cover or not cover['alt']:
            cover['alt'] = generate_alt_from_title(fm.get('title', ''))
            report['changes'].append(f'补充 alt: {cover["alt"]}')

        if 'caption' not in cover or not cover['caption']:
            cover['caption'] = generate_caption_from_title(fm.get('title', ''))
            report['changes'].append(f'补充 caption: {cover["caption"]}')

    elif 'image' in fm and isinstance(fm.get('image'), str):
        # 变体 A：扁平 image，转为 cover 对象
        report['variant'] = 'A (扁平image)'
        old_url = fm['image']
        new_url = normalize_image_url(old_url)
        title = fm.get('title', '')

        fm['cover'] = {
            'image': new_url,
            'alt': generate_alt_from_title(title),
            'caption': generate_caption_from_title(title),
        }
        del fm['image']

        report['changes'].append(f'扁平 image -> cover 对象')
        report['changes'].append(f'  cover.image: {new_url[:60]}...')
        report['changes'].append(f'  cover.alt: {fm["cover"]["alt"]}')
        report['changes'].append(f'  cover.caption: {fm["cover"]["caption"]}')

        if old_url != new_url:
            report['changes'].append(f'URL 参数标准化')

    else:
        # 变体 C：有 front matter 但无 image/cover
        report['variant'] = 'C (无image/cover)'
        title = fm.get('title', '')

        # 尝试从正文找配图
        img_match = re.search(r'!\[.*?\]\((https://images\.unsplash\.com/[^)]+)\)', body)
        if img_match:
            img_url = normalize_image_url(img_match.group(1))
        else:
            img_url = 'TODO_REPLACE_WITH_REAL_URL'

        fm['cover'] = {
            'image': img_url,
            'alt': generate_alt_from_title(title),
            'caption': generate_caption_from_title(title),
        }
        report['changes'].append(f'补充 cover 对象')
        report['changes'].append(f'  cover.image: {img_url[:60]}...')
        report['changes'].append(f'  cover.alt: {fm["cover"]["alt"]}')
        report['changes'].append(f'  cover.caption: {fm["cover"]["caption"]}')

    # 生成新内容
    new_fm = build_front_matter(fm, is_index=False)
    new_content = new_fm + body

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return report


def fix_index(filepath: Path, dry_run: bool = True) -> dict:
    """修复 _index.md，返回修复报告"""
    report = {
        'file': str(filepath.relative_to(BASE_DIR)),
        'variant': '_index.md',
        'changes': [],
    }

    content = filepath.read_text(encoding='utf-8')
    fm, body = extract_front_matter(content)

    if fm is None:
        report['changes'].append('无 front matter，跳过')
        return report

    # 补 description
    if 'description' not in fm or not fm.get('description'):
        cat_name = filepath.parent.name if filepath.parent != BASE_DIR else 'ModelCreate'
        fm['description'] = f'{cat_name}相关文章合集'
        report['changes'].append(f'补充 description: {fm["description"]}')

    new_fm = build_front_matter(fm, is_index=True)
    new_content = new_fm + body

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return report


# ============================================================
# 主流程
# ============================================================

def main():
    dry_run = '--apply' not in sys.argv

    if dry_run:
        print('=' * 60)
        print('  干跑模式（DRY RUN）— 不会修改任何文件')
        print('  添加 --apply 参数执行实际修改')
        print('=' * 60)
    else:
        print('=' * 60)
        print('  实际执行模式（APPLY）— 将修改文件')
        print('=' * 60)

    print()

    stats = {
        'total': 0,
        'A': 0, 'B': 0, 'C': 0, 'D': 0,
        'index': 0,
        'skipped': 0,
        'changed': 0,
    }

    reports = []

    for filepath in sorted(BASE_DIR.rglob('*.md')):
        stats['total'] += 1

        # 跳过非文章文件
        if filepath.name == '博客分析报告.md':
            stats['skipped'] += 1
            continue

        if filepath.name == '_index.md':
            report = fix_index(filepath, dry_run=dry_run)
            stats['index'] += 1
        else:
            report = fix_article(filepath, dry_run=dry_run)
            v = report['variant']
            if 'A' in v: stats['A'] += 1
            elif 'B' in v: stats['B'] += 1
            elif 'C' in v: stats['C'] += 1
            elif 'D' in v: stats['D'] += 1

        if report['changes']:
            stats['changed'] += 1
            reports.append(report)

    # 打印报告
    print(f'扫描文件总数: {stats["total"]}')
    print(f'  文章变体 A (扁平image): {stats["A"]}')
    print(f'  文章变体 B (cover对象): {stats["B"]}')
    print(f'  文章变体 C (无image):   {stats["C"]}')
    print(f'  文章变体 D (无front matter): {stats["D"]}')
    print(f'  _index.md:              {stats["index"]}')
    print(f'  跳过:                   {stats["skipped"]}')
    print(f'需要修复: {stats["changed"]} 个文件')
    print()

    # 打印详细变更
    for report in reports:
        print(f'[{report["variant"]}] {report["file"]}')
        for change in report['changes']:
            print(f'  - {change}')
        print()

    if dry_run:
        print('提示：添加 --apply 参数执行实际修改')
    else:
        print(f'完成！已修改 {stats["changed"]} 个文件')


if __name__ == '__main__':
    main()