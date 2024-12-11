file_path = "/home2/wzc/gnss_logger/my_log/gnss_log_2024_11_28_20_17_44.txt"
output_path = "/home2/wzc/gnss_logger/my_log/location.txt"

# 打开输入文件并读取内容
with open(file_path, 'r') as infile:
    lines = infile.readlines()

# 筛选以 "Fix,GPS" 开头的行
filtered_lines = []
for line in lines:
    if line.startswith("Fix,GPS"):
        cleaned_line = line.split(',')  # 按逗号分割
        cleaned_line = cleaned_line[:12]  # 只取前12个数据
        # 将清理后的行重新拼接成字符串，并添加换行符
        filtered_lines.append(','.join(cleaned_line) + '\n')

# # 筛选以 "Fix,GPS" 开头的行
# filtered_lines = [line for line in lines if line.startswith("Fix,GPS")]


# 将筛选后的行写入输出文件
with open(output_path, 'w') as outfile:
    outfile.writelines(filtered_lines)

print(f"已成功提取行到 {output_path}")