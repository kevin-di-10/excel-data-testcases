#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel数据处理测试用例生成脚本
生成8个大规模CSV文件用于测试数据处理程序
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string

# 设置随机种子保证可重复性
random.seed(42)
np.random.seed(42)

CHINESE_NAMES = ['张三', '李四', '王五', '赵六', '孙七', '周八', '吴九', '郑十',
                  '韩十一', '冯十二', '陈十三', '褚十四', '卫十五', '蒋十六',
                  '沈十七', '韦十八', '江十九', '傅二十']

CITIES = ['北京', '上海', '广州', '深圳', '杭州', '南京', '苏州', '成都', '武汉', '西安',
          '重庆', '天津', '长沙', '沈阳', '青岛', '大连', '宁波', '厦门', '郑州', '济南']

PRODUCTS = ['产品A', '产品B', '产品C', '产品D', '产品E', '产品F', '产品G', '产品H']

INDUSTRIES = ['IT', '金融', '制造', '零售', '医疗', '教育', '物流', '房产']

CUSTOMER_LEVELS = ['VIP', '普通', '新客']

def generate_data_cleaning(rows=15000):
    """生成数据清洗测试数据 - 包含重复、缺失、格式混乱"""
    data = []
    for i in range(rows):
        name = random.choice(CHINESE_NAMES)
        age = random.randint(18, 65) if random.random() > 0.15 else None  # 15%缺失
        email = f"{name}@email.com" if random.random() > 0.1 else None  # 10%缺失
        city = random.choice(CITIES) if random.random() > 0.1 else None  # 10%缺失
        phone = f"1{random.randint(30, 99)}{random.randint(10000000, 99999999)}" if random.random() > 0.2 else None
        
        # 添加空格不一致
        if random.random() > 0.7:
            name = f" {name} "
            city = f" {city} " if city else city
        
        # 添加重复（5%的概率）
        data.append({
            '姓名': name,
            '年龄': age,
            '邮箱': email,
            '城市': city,
            '电话': phone
        })
    
    # 插入一些完全重复的行
    for _ in range(int(rows * 0.05)):
        data.append(random.choice(data))
    
    df = pd.DataFrame(data)
    return df.sample(frac=1).reset_index(drop=True)  # 随机排序

def generate_data_conversion(rows=20000):
    """生成数据类型转换测试数据 - 包含格式混乱的数据"""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(rows):
        # 日期格式混乱
        date_offset = random.randint(0, 365)
        date = base_date + timedelta(days=date_offset)
        if random.random() > 0.7:
            date_str = date.strftime('%d/%m/%Y')
        else:
            date_str = date.strftime('%Y-%m-%d')
        
        # 销售额格式混乱
        amount = random.randint(1000, 100000)
        if random.random() > 0.6:
            amount_str = f"¥{amount:,}"
        elif random.random() > 0.3:
            amount_str = f"${amount}"
        else:
            amount_str = str(amount)
        
        # 数量
        quantity = random.randint(1, 1000)
        
        # 百分比格式混乱
        percentage = random.uniform(50, 100)
        if random.random() > 0.5:
            percentage_str = f"{percentage:.1f}%"
        else:
            percentage_str = str(round(percentage / 100, 3))
        
        # 状态
        status = random.choice(['已完成', '进行中', '待审核'])
        
        data.append({
            '日期': date_str,
            '销售额': amount_str,
            '数量': quantity,
            '百分比': percentage_str,
            '状态': status
        })
    
    return pd.DataFrame(data)

def generate_data_merge_orders(rows=25000):
    """生成订单数据 - 用于关联测试"""
    data = []
    for i in range(rows):
        order_id = f"O{i+1:06d}"
        customer_id = f"C{random.randint(1, 12000):05d}"
        date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        amount = random.randint(100, 50000)
        product = random.choice(PRODUCTS)
        
        data.append({
            '订单ID': order_id,
            '客户ID': customer_id,
            '订单日期': date.strftime('%Y-%m-%d'),
            '金额': amount,
            '产品类别': product
        })
    
    return pd.DataFrame(data)

def generate_data_merge_customers(rows=10000):
    """生成客户数据 - 用于关联测试"""
    data = []
    for i in range(rows):
        customer_id = f"C{i+1:05d}"
        name = random.choice(CHINESE_NAMES) + str(random.randint(100, 999))
        city = random.choice(CITIES)
        industry = random.choice(INDUSTRIES)
        level = random.choice(CUSTOMER_LEVELS)
        
        data.append({
            '客户ID': customer_id,
            '客户名': name,
            '城市': city,
            '行业': industry,
            '等级': level
        })
    
    return pd.DataFrame(data)

def generate_pivot_table_data(rows=30000):
    """生成数据透视表测试数据"""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(rows):
        date = (base_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        product = random.choice(PRODUCTS)
        city = random.choice(CITIES)
        amount = random.randint(1000, 100000)
        quantity = random.randint(1, 500)
        profit = int(amount * random.uniform(0.1, 0.5))
        
        data.append({
            '日期': date,
            '产品': product,
            '地区': city,
            '销售额': amount,
            '数量': quantity,
            '利润': profit
        })
    
    return pd.DataFrame(data)

def generate_text_split_data(rows=12000):
    """生成文本分割测试数据"""
    data = []
    for i in range(rows):
        province = random.choice(['北京', '上海', '广东', '浙江', '江苏'])
        city = random.choice(['朝阳', '浦东', '南山', '滨江', '玄武'])
        area = random.choice(['望京', '陆家嘴', '华侨城', '西湖', '新街口'])
        address = f"{province}-{city}-{area}"
        
        # 产品编码
        code = f"PRD-{random.randint(100, 999)}-{random.choice(string.ascii_uppercase)}{random.randint(1000, 9999)}"
        
        # 标签组合
        tags = '-'.join(random.sample(['热销', '新品', '促销', '热评', '质优', '推荐'], k=random.randint(2, 4)))
        
        data.append({
            '完整地址': address,
            '产品编码': code,
            '标签组合': tags
        })
    
    return pd.DataFrame(data)

def generate_anomaly_detection_data(rows=18000):
    """生成异常值检测测试数据"""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(rows):
        date = (base_date + timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
        
        # 温度 - 大部分在20-30°C，5%异常值
        if random.random() > 0.95:
            temperature = random.choice([-50, 150, 200])
        else:
            temperature = round(random.uniform(20, 30), 1)
        
        # 湿度 - 大部分在40-80%，5%异常值
        if random.random() > 0.95:
            humidity = random.choice([-20, 150, 200])
        else:
            humidity = random.randint(40, 80)
        
        # 销售额 - 大部分在1000-50000，3%异常值
        if random.random() > 0.97:
            amount = random.choice([999999, 0, -5000])
        else:
            amount = random.randint(1000, 50000)
        
        # 访客数 - 大部分在100-1000，5%异常值
        if random.random() > 0.95:
            visitors = random.choice([-100, 99999, 500000])
        else:
            visitors = random.randint(100, 1000)
        
        data.append({
            '日期': date,
            '温度': temperature,
            '湿度': humidity,
            '销售额': amount,
            '访客数': visitors
        })
    
    return pd.DataFrame(data)

def generate_conditional_statistics_data(rows=22000):
    """生成条件统计测试数据"""
    data = []
    months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
    
    for i in range(rows):
        product = random.choice(PRODUCTS)
        month = random.choice(months)
        amount = random.randint(5000, 100000)
        target = random.randint(30000, 80000)
        achieved = '是' if amount >= target else '否'
        level = random.choice(CUSTOMER_LEVELS)
        
        data.append({
            '产品': product,
            '月份': month,
            '销售额': amount,
            '目标值': target,
            '是否达成': achieved,
            '客户等级': level
        })
    
    return pd.DataFrame(data)

def generate_large_transaction_data(rows=50000):
    """生成大规模交易数据"""
    data = []
    base_date = datetime(2023, 1, 1)
    
    for i in range(rows):
        transaction_id = f"TXN{i+1:08d}"
        account = f"ACC{random.randint(100000, 999999)}"
        amount = round(random.uniform(100, 1000000), 2)
        tx_type = random.choice(['转账', '支付', '提现', '充值', '退款'])
        timestamp = (base_date + timedelta(days=random.randint(0, 365), 
                                          hours=random.randint(0, 23),
                                          minutes=random.randint(0, 59))).isoformat()
        status = random.choice(['成功', '失败', '待确认'])
        remark = random.choice(['正常', '异常', '冻结', '审查中', '已解冻'])
        
        data.append({
            '交易ID': transaction_id,
            '账户': account,
            '金额': amount,
            '类型': tx_type,
            '时间戳': timestamp,
            '状态': status,
            '备注': remark
        })
    
    return pd.DataFrame(data)

def main():
    """主函数 - 生成所有测试数据"""
    print("开始生成Excel数据处理测试用例...\n")
    
    datasets = [
        ('1_data_cleaning.csv', generate_data_cleaning(15000), '数据清洗'),
        ('2_data_conversion.csv', generate_data_conversion(20000), '数据类型转换'),
        ('3_data_merge_orders.csv', generate_data_merge_orders(25000), '订单数据'),
        ('3_data_merge_customers.csv', generate_data_merge_customers(10000), '客户数据'),
        ('4_pivot_table_data.csv', generate_pivot_table_data(30000), '数据透视'),
        ('5_text_split.csv', generate_text_split_data(12000), '文本分割'),
        ('6_anomaly_detection.csv', generate_anomaly_detection_data(18000), '异常值检测'),
        ('7_conditional_statistics.csv', generate_conditional_statistics_data(22000), '条件统计'),
        ('8_large_transaction_data.csv', generate_large_transaction_data(50000), '大数据处理')
    ]
    
    total_rows = 0
    for filename, df, description in datasets:
        df.to_csv(filename, index=False, encoding='utf-8')
        rows = len(df)
        size = df.memory_usage(deep=True).sum() / 1024 / 1024  # MB
        total_rows += rows
        print(f"✓ {filename}: {rows:>6,} 行 | {size:>6.2f} MB | {description}")
    
    print(f"\n总计：{total_rows:,} 行数据")
    print("✓ 所有测试数据生成完成！")

if __name__ == '__main__':
    main()
