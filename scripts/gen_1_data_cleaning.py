#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的Excel数据处理测试用例 - 数据清洗（15,000行）
"""
import csv
import random
from datetime import datetime, timedelta

# 设置随机种子
random.seed(42)

CHINESE_NAMES = ['张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十',
                  '韦十一', '冯十二', '陈十三', '褚十四', '卫十五', '蒋十六',
                  '沈十七', '韦十八', '江十九', '傅二十']

CITIES = ['北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', '成都', '武汉', '西安',
          '重庆', '天津', '长沙', '沈阳', '青岛', '大连', '宁波', '厦门', '郑州', '济南']

# 生成数据清洗测试数据
rows = 15000
data = []

for i in range(rows):
    name = random.choice(CHINESE_NAMES)
    age = random.randint(18, 65) if random.random() > 0.15 else None
    email = f"{name}{i}@email.com" if random.random() > 0.1 else None
    city = random.choice(CITIES) if random.random() > 0.1 else None
    phone = f"1{random.randint(30, 99)}{random.randint(10000000, 99999999)}" if random.random() > 0.2 else None
    
    # 添加空格不一致
    if random.random() > 0.7:
        name = f" {name} "
        if city: city = f" {city} "
    
    data.append({
        '姓名': name,
        '年龄': age,
        '邮箱': email,
        '城市': city,
        '电话': phone
    })

# 插入一些重复的行（5%）
for _ in range(int(rows * 0.05)):
    data.append(random.choice(data))

# 随机打乱
random.shuffle(data)

# 写入CSV
with open('1_data_cleaning.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['姓名', '年龄', '邮箱', '城市', '电话'])
    writer.writeheader()
    writer.writerows(data)

print(f"✓ 生成 1_data_cleaning.csv ({len(data):,} 行)")
