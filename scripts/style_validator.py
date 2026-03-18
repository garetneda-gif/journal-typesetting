#!/usr/bin/env python3
"""
样式验证工具 - MedBA Medicine期刊排版
用于验证生成的HTML是否与模板样式一致
"""

import re
import os
import sys
from pathlib import Path


class StyleValidator:
    """HTML样式一致性验证器"""

    def __init__(self, template_type="single-column"):
        """
        初始化验证器

        Args:
            template_type: "single-column" 或 "two-column"
        """
        self.template_type = template_type
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0

        # 模板路径
        skill_dir = Path(__file__).parent.parent
        if template_type == "single-column":
            self.template_path = skill_dir / "assets" / "template-single-column.html"
        else:
            self.template_path = skill_dir / "assets" / "template-two-column.html"

    def validate_file(self, html_file_path):
        """
        验证HTML文件的样式一致性

        Args:
            html_file_path: 要验证的HTML文件路径

        Returns:
            dict: 验证结果
        """
        print(f"\n🔍 验证文件: {html_file_path}")
        print(f"📋 模板类型: {self.template_type}")
        print(f"📄 参考模板: {self.template_path}\n")

        # 读取文件
        with open(html_file_path, 'r', encoding='utf-8') as f:
            generated_html = f.read()

        with open(self.template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()

        # 执行验证
        self._validate_theme_color(generated_html)
        self._validate_font_family(generated_html)
        self._validate_css_variables(generated_html, template_html)
        self._validate_critical_styles(generated_html)
        self._validate_figure_styles(generated_html)
        self._validate_table_styles(generated_html)
        self._validate_reference_styles(generated_html)
        self._validate_title_case(generated_html)

        # 生成报告
        return self._generate_report()

    def _check(self, name, condition, error_msg=None, warning_msg=None):
        """
        执行单项检查

        Args:
            name: 检查项名称
            condition: 检查条件（True表示通过）
            error_msg: 错误信息（严重问题）
            warning_msg: 警告信息（可接受但不理想）
        """
        self.checks_total += 1

        if condition:
            self.checks_passed += 1
            print(f"  ✅ {name}")
        elif error_msg:
            self.errors.append(f"{name}: {error_msg}")
            print(f"  ❌ {name} - {error_msg}")
        elif warning_msg:
            self.warnings.append(f"{name}: {warning_msg}")
            print(f"  ⚠️  {name} - {warning_msg}")
        else:
            self.errors.append(f"{name}: 未通过")
            print(f"  ❌ {name}")

    def _validate_theme_color(self, html):
        """验证主题色 #005a8c"""
        print("## 主题色检查")

        # 检查主题色存在
        has_theme_color = "#005a8c" in html.lower()
        self._check(
            "主题色 #005a8c",
            has_theme_color,
            error_msg="缺少主题色 #005a8c"
        )

        # 检查是否误用了RGB格式
        has_rgb_theme = "rgb(0, 90, 140)" in html or "rgb(0,90,140)" in html
        self._check(
            "禁用RGB格式主题色",
            not has_rgb_theme,
            warning_msg="建议使用十六进制 #005a8c 而非 RGB 格式"
        )

        # 检查近似颜色
        similar_colors = ["#0059ab", "#005b8c", "#005a8b", "#005a8d"]
        has_similar = any(color in html.lower() for color in similar_colors)
        self._check(
            "避免近似颜色值",
            not has_similar,
            error_msg="检测到近似颜色值，应使用精确的 #005a8c"
        )

    def _validate_font_family(self, html):
        """验证字体family"""
        print("\n## 字体检查")

        # 检查Times New Roman
        has_times = "'Times New Roman', Times, serif" in html or \
                    "'Times New Roman',Times,serif" in html
        self._check(
            "Times New Roman字体",
            has_times,
            error_msg="缺少 'Times New Roman', Times, serif"
        )

        # 检查Arial (标题字体)
        has_arial = "Arial, Helvetica, sans-serif" in html or \
                    "Arial,Helvetica,sans-serif" in html
        self._check(
            "Arial标题字体",
            has_arial,
            error_msg="标题应使用 Arial, Helvetica, sans-serif"
        )

    def _validate_css_variables(self, html, template):
        """验证CSS变量（仅双栏版）"""
        if self.template_type != "two-column":
            return

        print("\n## CSS变量检查 (双栏版)")

        css_vars = [
            "--page-width: 210mm",
            "--page-height: 297mm",
            "--margin-top: 25mm",
            "--margin-bottom: 20mm",
            "--margin-left: 20mm",
            "--margin-right: 20mm",
            "--column-gap: 7.48mm"
        ]

        for var in css_vars:
            # 允许空格变化
            var_pattern = var.replace(" ", r"\s*")
            has_var = re.search(var_pattern, html)
            self._check(
                f"CSS变量 {var}",
                has_var is not None,
                error_msg=f"缺少CSS变量定义"
            )

    def _validate_critical_styles(self, html):
        """验证关键样式"""
        print("\n## 关键样式检查")

        if self.template_type == "two-column":
            # 双栏布局
            self._check(
                "双栏布局 column-count: 2",
                "column-count: 2" in html or "column-count:2" in html,
                error_msg="缺少双栏布局设置"
            )

            self._check(
                "双栏间距 column-gap",
                "column-gap" in html,
                error_msg="缺少双栏间距设置"
            )

            self._check(
                "跨栏样式 column-span: all",
                "column-span: all" in html or "column-span:all" in html,
                error_msg="缺少跨栏样式设置"
            )

        # 单位检查 (mm)
        has_mm_units = "mm" in html
        self._check(
            "使用mm单位",
            has_mm_units,
            error_msg="应使用mm作为主要单位"
        )

        # 检查是否误用了px单位 (少量px用于阴影等是可以的)
        px_count = html.count("px")
        self._check(
            "避免过度使用px单位",
            px_count < 20,
            warning_msg=f"检测到{px_count}处px单位，建议优先使用mm"
        )

    def _validate_figure_styles(self, html):
        """验证图片样式"""
        print("\n## 图片样式检查")

        # 检查figcaption字体大小
        has_figcaption_size = "font-size:8.5pt" in html or "font-size: 8.5pt" in html
        self._check(
            "图片标题字体大小 8.5pt",
            has_figcaption_size,
            error_msg="图片标题应使用 font-size: 8.5pt"
        )

        # 检查图号样式 (粗体 + 主题色)
        fig_label_pattern = r'font-weight:\s*bold.*?color:\s*#005a8c|color:\s*#005a8c.*?font-weight:\s*bold'
        has_fig_label_style = re.search(fig_label_pattern, html, re.IGNORECASE)
        self._check(
            "图号样式 (bold + #005a8c)",
            has_fig_label_style is not None,
            warning_msg="图号应使用粗体+主题色样式"
        )

        # 检查并排图片布局
        if "side-by-side-figures" in html:
            if self.template_type == "two-column":
                has_grid = ".side-by-side-figures" in html and (
                    "display: grid" in html or "display:grid" in html
                )
                self._check(
                    "双栏并排图片使用 Grid",
                    has_grid,
                    error_msg="双栏并排图片必须使用 display:grid"
                )

                has_display_contents = "display: contents" in html or "display:contents" in html
                self._check(
                    "双栏 figure 使用 display: contents",
                    has_display_contents,
                    error_msg="双栏并排图片的 figure 必须使用 display: contents"
                )

                has_align_end = "align-self: end" in html or "align-self:end" in html
                self._check(
                    "双栏图片/图注底部对齐样式",
                    has_align_end,
                    error_msg="双栏并排图片必须为 img/figcaption 设置 align-self:end"
                )
            else:
                has_flex_figures = "display:flex" in html or "display: flex" in html
                self._check(
                    "单栏并排图片使用 flex",
                    has_flex_figures,
                    warning_msg="单栏并排图片通常应使用 flex 容器"
                )

                has_flex_end = "align-items:flex-end" in html or "align-items: flex-end" in html
                self._check(
                    "单栏并排图片底部对齐样式",
                    has_flex_end,
                    warning_msg="单栏并排图片建议使用 align-items:flex-end 保持底部对齐"
                )

            has_gap = "gap:5mm" in html or "gap: 5mm" in html or "gap:4mm" in html or "gap: 4mm" in html
            self._check(
                "并排图片gap间距",
                has_gap,
                warning_msg="并排图片应使用 gap: 5mm (单栏) 或 gap: 4mm (双栏)"
            )

    def _validate_table_styles(self, html):
        """验证表格样式"""
        print("\n## 表格样式检查")

        if "<table" not in html:
            print("  ℹ️  未检测到表格，跳过表格样式检查")
            return

        # 检查表格边框
        has_table_border = "border-top: 1.5pt solid #000" in html or \
                          "border-top:1.5pt solid #000" in html
        self._check(
            "表格顶部边框 1.5pt",
            has_table_border,
            error_msg="表格应使用 border-top: 1.5pt solid #000"
        )

        # 检查表格字体大小
        has_table_size = "font-size:8.5pt" in html or "font-size: 8.5pt" in html
        self._check(
            "表格字体大小 8.5pt",
            has_table_size,
            warning_msg="表格内容应使用 font-size: 8.5pt"
        )

    def _validate_reference_styles(self, html):
        """验证参考文献样式"""
        print("\n## 参考文献样式检查")

        if "REFERENCES" not in html and "References" not in html:
            print("  ℹ️  未检测到参考文献，跳过样式检查")
            return

        # 检查参考文献字体大小
        has_ref_size = "font-size:8pt" in html or "font-size: 8pt" in html
        self._check(
            "参考文献字体大小 8pt",
            has_ref_size,
            error_msg="参考文献应使用 font-size: 8pt"
        )

        # 检查悬挂缩进
        has_hanging_indent = ("padding-left:1.5em" in html or "padding-left: 1.5em" in html) and \
                            ("text-indent:-1.5em" in html or "text-indent: -1.5em" in html)
        self._check(
            "参考文献悬挂缩进",
            has_hanging_indent,
            warning_msg="参考文献应使用悬挂缩进 (padding-left: 1.5em; text-indent: -1.5em)"
        )

        # 检查链接颜色
        if "<a href" in html:
            has_link_color = "color:#005a8c" in html or "color: #005a8c" in html
            self._check(
                "参考文献链接颜色",
                has_link_color,
                warning_msg="链接颜色应使用 #005a8c"
            )

    def _validate_title_case(self, html):
        """验证文章主标题是否为 sentence case"""
        print("\n## 标题大小写检查")

        # 提取 #article-title 内容
        title_match = re.search(
            r'id=["\']article-title["\'][^>]*>(.*?)</div>',
            html, re.DOTALL | re.IGNORECASE
        )
        if not title_match:
            print("  ℹ️  未检测到 #article-title，跳过标题大小写检查")
            return

        title_text = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        if not title_text:
            return

        words = title_text.split()
        # 检查是否全大写（ALL CAPS）
        all_caps = all(w.isupper() or not w.isalpha() for w in words)
        self._check(
            "标题非全大写",
            not all_caps,
            error_msg="标题为全大写，必须转换为 sentence case"
        )

        # 检查非首词是否存在不必要的大写（排除专有名词）
        if len(words) > 1 and not all_caps:
            suspicious = []
            for w in words[1:]:
                clean = w.rstrip(".,;:!?")
                if clean and clean[0].isupper() and clean.lower() == clean.lower() and not clean.isupper():
                    suspicious.append(clean)
            if suspicious:
                self._check(
                    "标题 sentence case 格式",
                    False,
                    warning_msg=f"疑似 Title Case 词: {', '.join(suspicious[:5])}（若为专有名词可忽略）"
                )
            else:
                self._check("标题 sentence case 格式", True)

    def _generate_report(self):
        """生成验证报告"""
        print("\n" + "="*60)
        print("📊 验证报告")
        print("="*60)

        # 统计
        pass_rate = (self.checks_passed / self.checks_total * 100) if self.checks_total > 0 else 0
        print(f"\n总检查项: {self.checks_total}")
        print(f"通过: {self.checks_passed} ✅")
        print(f"错误: {len(self.errors)} ❌")
        print(f"警告: {len(self.warnings)} ⚠️")
        print(f"通过率: {pass_rate:.1f}%")

        # 错误列表
        if self.errors:
            print("\n❌ 严重错误（必须修复）:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")

        # 警告列表
        if self.warnings:
            print("\n⚠️  警告（建议修复）:")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")

        # 最终判定
        print("\n" + "="*60)
        if len(self.errors) == 0:
            print("✅ 样式验证通过！可以交付。")
            status = "PASS"
        else:
            print("❌ 样式验证失败！请修复错误后重新验证。")
            status = "FAIL"
        print("="*60)

        return {
            "status": status,
            "total": self.checks_total,
            "passed": self.checks_passed,
            "errors": len(self.errors),
            "warnings": len(self.warnings),
            "pass_rate": pass_rate,
            "error_list": self.errors,
            "warning_list": self.warnings
        }


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="MedBA Medicine HTML样式验证工具")
    parser.add_argument("html_file", help="要验证的HTML文件路径")
    parser.add_argument(
        "--type",
        choices=["single-column", "two-column"],
        default="single-column",
        help="模板类型 (默认: single-column)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以JSON格式输出结果"
    )

    args = parser.parse_args()

    # 检查文件是否存在
    if not os.path.exists(args.html_file):
        print(f"❌ 错误: 文件不存在 - {args.html_file}")
        sys.exit(1)

    # 执行验证
    validator = StyleValidator(template_type=args.type)
    result = validator.validate_file(args.html_file)

    # JSON输出
    if args.json:
        import json
        print("\n" + json.dumps(result, indent=2, ensure_ascii=False))

    # 返回状态码
    sys.exit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
