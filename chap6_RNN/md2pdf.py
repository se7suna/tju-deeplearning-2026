import os
import markdown
from weasyprint import HTML

def md_to_pdf(md_path, pdf_path):
    # 获取 markdown 文件所在目录（用于解析本地图片）
    base_dir = os.path.dirname(os.path.abspath(md_path))

    # 读取 markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    # 转 HTML
    html_text = markdown.markdown(md_text, extensions=['extra'])

    # 加一个简单 HTML 模板（支持图片缩放）
    html_template = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                padding: 20px;
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            pre {{
                background: #f4f4f4;
                padding: 10px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        {html_text}
    </body>
    </html>
    """

    # 转 PDF（关键：base_url 让本地图片生效）
    HTML(string=html_template, base_url=base_dir).write_pdf(pdf_path)

    print(f"✅ 转换完成: {pdf_path}")


if __name__ == "__main__":
    md_to_pdf("report.md", "output.pdf")