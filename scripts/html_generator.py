#!/usr/bin/env python3
"""
HTML生成器模块 - MedBA Medicine期刊排版
用于生成双栏分页和单栏连续HTML
"""

class JournalHTMLGenerator:
    """期刊HTML生成器"""

    def __init__(self, data, image_urls, short_title):
        """
        初始化生成器

        Args:
            data: 解析后的Word文档数据（标题、作者、摘要、正文等）
            image_urls: 图片URL字典 {"Figure 1": "https://...", ...}
            short_title: 简短标题（用于文件名）
        """
        self.data = data
        self.image_urls = image_urls
        self.short_title = short_title

        # 标题 sentence case 规范化
        if 'title' in self.data:
            self.data['title'] = self._to_sentence_case(self.data['title'])

        # 期刊配置
        self.journal_config = {
            "name": "MedBA Medicine",
            "logo_url": "https://medbam.org/assets/logo.png",
            "website": "https://medbam.org",
            "color": "#005a8c",
            "doi_prefix": "10.65079"
        }

    def generate_two_column_html(self, output_path):
        """
        生成双栏分页HTML

        Args:
            output_path: 输出文件路径

        Returns:
            文件大小（bytes）
        """
        print(f"📋 生成双栏分页HTML...")

        # 加载模板
        template = self._load_template("two-column")

        # 生成各部分
        cover_page = self._generate_cover_page()
        content_pages = self._generate_content_pages(layout="two-column")

        # 组装HTML
        html = template.format(
            title=self.data['title'],
            cover=cover_page,
            content=content_pages
        )

        # 写入文件
        return self._write_html_file(output_path, html)

    def generate_single_column_html(self, output_path, include_ref_links=True):
        """
        生成单栏连续HTML

        Args:
            output_path: 输出文件路径
            include_ref_links: 是否包含参考文献验证链接

        Returns:
            文件大小（bytes）
        """
        print(f"📋 生成单栏连续HTML...")

        # 加载模板
        template = self._load_template("single-column")

        # 生成各部分
        header = self._generate_header()
        abstract = self._generate_abstract()
        content = self._generate_content_pages(layout="single-column")
        references = self._generate_references(include_links=include_ref_links)

        # 组装HTML
        html = template.format(
            title=self.data['title'],
            header=header,
            abstract=abstract,
            content=content,
            references=references
        )

        # 写入文件
        return self._write_html_file(output_path, html)

    # 医学/生物学专有名词白名单（大小写敏感，保留原样）
    PROPER_NOUNS = {
        # 基因/蛋白符号
        "TP53", "BRCA1", "BRCA2", "EGFR", "TGFB1", "TIMP1", "VEGF", "HER2",
        "KRAS", "BRAF", "ALK", "ROS1", "MET", "PTEN", "PIK3CA", "AKT",
        "mTOR", "HIF-1", "HIF-1α", "PD-L1", "PD-1", "CTLA-4", "JAK2",
        # 数据库/工具
        "TCGA", "GEO", "KEGG", "FAERS", "STRING", "GEPIA", "TIMER",
        "UALCAN", "cBioPortal", "DAVID", "GSEA", "ssGSEA", "WGCNA",
        # 学术缩写
        "miRNA", "lncRNA", "ceRNA", "circRNA", "siRNA", "mRNA", "DNA", "RNA",
        "LASSO", "ROC", "AUC", "OS", "DFS", "PFS", "HR", "CI", "OR",
        "PCR", "qRT-PCR", "ELISA", "IHC", "WB", "IF",
        # 疾病缩写
        "ccRCC", "NSCLC", "HCC", "CRC", "GBM", "AML", "ALL", "NHL",
        "LUAD", "LUSC", "KIRC", "KIRP", "BRCA", "PRAD", "STAD",
        # 药物/治疗
        "TKI", "ICB", "CAR-T", "FOLFOX", "FOLFIRI",
    }

    def _to_sentence_case(self, title: str) -> str:
        """
        将标题转换为 sentence case：仅大写首词和专有名词。
        冒号后首词大写（AMA 风格），破折号后不大写。
        """
        if not title or not title.strip():
            return title

        words = title.split()
        result = []
        capitalize_next = True  # 首词大写

        for word in words:
            # 检查是否为白名单专有名词（精确匹配去标点后的词）
            clean_word = word.rstrip(".,;:!?")
            if clean_word in self.PROPER_NOUNS:
                result.append(word)
            elif capitalize_next:
                result.append(word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper())
                capitalize_next = False
            else:
                result.append(word.lower())

            # 冒号后首词大写
            if word.endswith(":"):
                capitalize_next = True

        return " ".join(result)

    def _load_template(self, template_type):
        """加载HTML模板"""
        # TODO: 从assets/目录读取模板文件
        pass

    def _generate_cover_page(self):
        """生成封面页"""
        # TODO: 生成封面页HTML
        pass

    def _generate_header(self):
        """生成页眉"""
        # TODO: 生成页眉HTML
        pass

    def _generate_abstract(self):
        """生成摘要部分"""
        # TODO: 生成摘要HTML
        pass

    def _generate_content_pages(self, layout="two-column"):
        """
        生成正文页面

        Args:
            layout: "two-column" 或 "single-column"
        """
        # TODO: 生成正文HTML
        pass

    def _generate_references(self, include_links=True):
        """
        生成参考文献部分

        Args:
            include_links: 是否包含验证链接
        """
        # TODO: 生成参考文献HTML
        pass

    def _write_html_file(self, path, content):
        """
        写入HTML文件（支持大文件分段写入）

        Args:
            path: 文件路径
            content: HTML内容

        Returns:
            文件大小（bytes）
        """
        import os

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        file_size = os.path.getsize(path)
        print(f"   └─ 文件写入: ✅ ({file_size / 1024:.1f} KB)")

        return file_size


def main():
    """测试函数"""
    # 示例数据
    sample_data = {
        "title": "Test Article",
        "authors": ["Author One", "Author Two"],
        "abstract": "This is a test abstract.",
        "references": []
    }

    sample_urls = {
        "Figure 1": "https://example.com/fig1.png"
    }

    generator = JournalHTMLGenerator(sample_data, sample_urls, "Test-Article")

    # 测试生成
    # generator.generate_two_column_html("/tmp/test-two-col.html")
    # generator.generate_single_column_html("/tmp/test-single-col.html")

    print("✅ HTML生成器模块已加载")


if __name__ == "__main__":
    main()
