# generate_report.py 使用说明

## 安装依赖

```bash
pip install reportlab
```

## 基本用法

```bash
python scripts/generate_report.py \
    --topic "世界模型" \
    --timeframe "2026-04-21 ~ 2026-04-28" \
    --input research_data.json \
    --output "文献进展报告_世界模型_20260428.pdf"
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--topic` | 是 | 研究报告主题（中文） |
| `--timeframe` | 是 | 时间范围描述 |
| `--input` | 是 | 输入 JSON 数据文件路径 |
| `--output` | 否 | 输出 PDF 文件路径（默认：`{topic}_{date}.pdf`） |

## 输入 JSON 格式

参见 `templates/report_data_schema.md`。
