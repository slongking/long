import os
import json
import pandas as pd

# 定义文件夹路径和 Excel 文件保存路径
folder_path = r'E:\WindowSystemLocation\Desktop\关税\products'
excel_path = r'E:\WindowSystemLocation\Desktop\products_deepseek.xlsx'

# 存储解析后的数据
data_list = []

def extract_user_id(link):
    """
    从商家链接中提取商家用户 ID
    :param link: 商家链接
    :return: 商家用户 ID，如果未找到则返回空字符串
    """
    if link and 'xhsdiscover://user/' in link:
        parts = link.split('/')
        if len(parts) > 3:
            return parts[3].split('?')[0]
    return ''

# 遍历文件夹中的所有文件
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file:
            file_path = os.path.join(root, file)
            try:
                print(f"正在处理文件: {file_path}")
                # 读取 JSON 文件
                with open(file_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)

                # 检查数据是否存在
                if 'data' in json_data and 'module' in json_data['data'] and 'data' in json_data['data']['module']:
                    for item in json_data['data']['module']['data']:
                        content = item.get('content', {})
                        price_info = content.get('price_info', {})
                        vendor = content.get('vendor', {})
                        tag_strategy_map = content.get('tag_strategy_map', {})

                        # 提取已售信息
                        sold_count = ''
                        after_price_tags = tag_strategy_map.get('after_price', [])
                        for tag in after_price_tags:
                            if tag.get('type') == 'sold':
                                sold_count = tag.get('tag_content', {}).get('content', '')
                                break

                        # 提取退货包运费信息
                        return_freight = ''
                        behavior_tags = tag_strategy_map.get('behavior', [])
                        for tag in behavior_tags:
                            if tag.get('type') == 'carriage_insurance_v2':
                                return_freight = tag.get('tag_content', {}).get('content', '')
                                break

                        # 提取商家用户 ID
                        vendor_link = vendor.get('vendor_link')
                        vendor_user_id = extract_user_id(vendor_link)

                        # 构建数据行
                        row = {
                            '商品ID': content.get('id'),
                            '标题': content.get('title'),
                            '链接': content.get('link'),
                            '图片URL': content.get('image', [{}])[0].get('url'),
                            '商家ID': vendor.get('vendor_id'),
                            '商家名称': vendor.get('vendor_name'),
                            '商家链接': vendor_link,
                            '商家用户ID': vendor_user_id,  # 新增商家用户 ID 列
                            '卖家ID': vendor.get('seller_id'),
                            '价格': price_info.get('price'),
                            '原价': price_info.get('origin_price'),
                            '已售数量': sold_count,
                            '退货包运费': return_freight
                        }
                        data_list.append(row)
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

# 将数据转换为 DataFrame
df = pd.DataFrame(data_list)

# 保存到 Excel 文件
df.to_excel(excel_path, index=False)
print(f"数据已保存到 {excel_path}")