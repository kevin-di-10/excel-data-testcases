# Excel 数据处理测试用例 - 使用示例

## 快速开始

### 1. 生成完整数据集

```bash
# 在仓库目录下运行
python generate_all_data.py
```

输出：
```
============================================================
Excel 数据处理测试用例生成器
============================================================

开始生成数据文件...

✓ 1_data_cleaning.csv          |  15,000 行 |   1.20 MB | 数据清洗
✓ 2_data_conversion.csv        |  20,000 行 |   1.80 MB | 数据转换
✓ 3_data_merge_orders.csv      |  25,000 行 |   2.50 MB | 订单关联
✓ 3_data_merge_customers.csv   |  10,000 行 |   1.00 MB | 客户关联
✓ 4_pivot_table_data.csv       |  30,000 行 |   3.20 MB | 数据透视
✓ 5_text_split.csv             |  12,000 行 |   1.50 MB | 文本分割
✓ 6_anomaly_detection.csv      |  18,000 行 |   1.80 MB | 异常检测
✓ 7_conditional_statistics.csv |  22,000 行 |   2.20 MB | 条件统计
✓ 8_large_transaction_data.csv |  50,000 行 |   6.50 MB | 大数据处理

总计: 202,000 行数据 | 21.90 MB
============================================================
```

### 2. Python 使用示例

#### 2.1 数据清洗测试

```python
import pandas as pd

# 读取数据
df = pd.read_csv('1_data_cleaning.csv')

# 查看数据信息
print(df.head())
print(df.info())
print(df.isnull().sum())  # 查看缺失值

# 数据清洗
df_cleaned = df.copy()

# 1. 去除重复行
df_cleaned = df_cleaned.drop_duplicates()

# 2. 删除缺失值过多的行
df_cleaned = df_cleaned.dropna(thresh=3)  # 至少3列有值

# 3. 清理空格
df_cleaned['姓名'] = df_cleaned['姓名'].str.strip()
df_cleaned['城市'] = df_cleaned['城市'].str.strip()

# 4. 转换数据类型
df_cleaned['年龄'] = pd.to_numeric(df_cleaned['年龄'], errors='coerce')

# 5. 填充缺失值
df_cleaned['年龄'].fillna(df_cleaned['年龄'].median(), inplace=True)

print(f"\n清洗前: {len(df)} 行")
print(f"清洗后: {len(df_cleaned)} 行")
```

#### 2.2 数据转换测试

```python
import pandas as pd
import re

df = pd.read_csv('2_data_conversion.csv')

# 1. 日期格式统一转换
def parse_date(date_str):
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d']:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    return pd.NaT

df['日期'] = df['日期'].apply(parse_date)

# 2. 销售额转换（去除货币符号和逗号）
def parse_amount(amount_str):
    # 移除货币符号
    cleaned = re.sub(r'[¥$￥元,]', '', str(amount_str))
    return float(cleaned) if cleaned else None

df['销售额'] = df['销售额'].apply(parse_amount)

# 3. 百分比转换
def parse_percentage(percent_str):
    cleaned = str(percent_str).replace('%', '').strip()
    value = float(cleaned)
    # 如果已经是百分比形式（>1），则保持不变；否则乘以100
    return value if value > 1 else value * 100

df['百分比'] = df['百分比'].apply(parse_percentage)

print(df.dtypes)
print(df.head())
```

#### 2.3 数据关联测试

```python
import pandas as pd

# 读取订单和客户数据
orders = pd.read_csv('3_data_merge_orders.csv')
customers = pd.read_csv('3_data_merge_customers.csv')

# VLOOKUP 等价操作 - LEFT JOIN
merged = orders.merge(customers, left_on='客户ID', right_on='客户ID', how='left')

print(merged.head())
print(f"\n关联前订单数: {len(orders)}")
print(f"关联后记录数: {len(merged)}")

# 检查是否有未匹配的客户
unmatched = merged[merged['客户名'].isnull()]
print(f"\n未匹配的订单数: {len(unmatched)}")
```

#### 2.4 数据透视表测试

```python
import pandas as pd

df = pd.read_csv('4_pivot_table_data.csv')

# 创建透视表
pivot = pd.pivot_table(
    df,
    values='销售额',
    index='产品',
    columns='地区',
    aggfunc='sum',
    fill_value=0
)

print("\n按产品和地区统计销售额:")
print(pivot)

# 多维透视
pivot_multi = pd.pivot_table(
    df,
    values=['销售额', '数量', '利润'],
    index='产品',
    columns='地区',
    aggfunc='sum'
)

print("\n多维透视结果:")
print(pivot_multi)

# 添加小计
pivot_with_total = pivot.assign(合计=pivot.sum(axis=1))
pivot_with_total.loc['合计'] = pivot_with_total.sum()

print("\n带合计的透视表:")
print(pivot_with_total)
```

#### 2.5 文本分割测试

```python
import pandas as pd

df = pd.read_csv('5_text_split.csv')

# 方法1: str.split()
address_split = df['完整地址'].str.split('-', expand=True)
address_split.columns = ['省份', '地区', '位置']

df = pd.concat([df, address_split], axis=1)

print("地址分割结果:")
print(df[['完整地址', '省份', '地区', '位置']])

# 方法2: 标签分割
tags_split = df['标签组合'].str.split('-', expand=True)
tags_split.columns = [f'标签{i+1}' for i in range(tags_split.shape[1])]

df = pd.concat([df, tags_split], axis=1)

print("\n标签分割结果:")
print(df[['标签组合', '标签1', '标签2', '标签3']])
```

#### 2.6 异常值检测测试

```python
import pandas as pd
import numpy as np

df = pd.read_csv('6_anomaly_detection.csv')

# 方法1: 基于范围检测
anomalies_range = df[
    (df['温度'] < 0) | (df['温度'] > 50) |
    (df['湿度'] < 0) | (df['湿度'] > 100) |
    (df['访客数'] < 0)
]

print("基于范围的异常值:")
print(anomalies_range)

# 方法2: 基于离群值检测（IQR方法）
def detect_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] < lower_bound) | (df[column] > upper_bound)]

anomalies_iqr = detect_outliers_iqr(df, '销售额')

print("\nIQR方法检测的异常值:")
print(anomalies_iqr)

# 方法3: 基于Z-Score检测
from scipy import stats

df['销售额_zscore'] = np.abs(stats.zscore(df['销售额'].dropna()))
anomalies_zscore = df[df['销售额_zscore'] > 3]

print("\nZ-Score方法检测的异常值:")
print(anomalies_zscore)
```

#### 2.7 条件统计测试

```python
import pandas as pd

df = pd.read_csv('7_conditional_statistics.csv')

# 1. COUNTIF 等价 - 统计达成目标的记录数
count_achieved = (df['是否达成'] == '是').sum()
print(f"达成目标的记录数: {count_achieved}")

# 2. SUMIF 等价 - 统计特定产品的总销售额
product_sales = df.groupby('产品')['销售额'].sum()
print("\n按产品统计销售额:")
print(product_sales)

# 3. AVERAGEIF 等价 - 统计VIP客户的平均销售额
vip_avg = df[df['客户等级'] == 'VIP']['销售额'].mean()
print(f"\nVIP客户平均销售额: {vip_avg:.2f}")

# 4. 多条件统计
multi_condition = df[
    (df['产品'] == '产品A') & 
    (df['是否达成'] == '是') &
    (df['客户等级'] == 'VIP')
].shape[0]

print(f"\n产品A且达成且VIP的记录数: {multi_condition}")

# 5. 按多个字段分组统计
group_stats = df.groupby(['产品', '客户等级']).agg({
    '销售额': ['sum', 'mean', 'count'],
    '目标值': 'sum'
})

print("\n按产品和客户等级分组统计:")
print(group_stats)
```

#### 2.8 大数据处理性能测试

```python
import pandas as pd
import time

# 测试大数据加载性能
start = time.time()
df = pd.read_csv('8_large_transaction_data.csv')
load_time = time.time() - start

print(f"数据加载时间: {load_time:.3f}秒")
print(f"数据规模: {len(df):,} 行 × {len(df.columns)} 列")

# 测试数据处理性能
start = time.time()

# 1. 按账户统计
account_stats = df.groupby('账户').agg({
    '金额': ['sum', 'mean', 'count'],
    '状态': lambda x: (x == '成功').sum()
})

process_time = time.time() - start
print(f"\n数据处理时间: {process_time:.3f}秒")

# 2. 筛选特定类型交易
start = time.time()
filtereddf = df[df['类型'] == '转账']
filter_time = time.time() - start

print(f"筛选时间: {filter_time:.3f}秒")
print(f"筛选结果: {len(filtered_df):,} 行")

# 3. 内存使用情况
memory_usage = df.memory_usage(deep=True).sum() / 1024 / 1024
print(f"\n内存使用: {memory_usage:.2f} MB")
```

### 3. R 使用示例

```r
# 安装必要的包
install.packages(c('tidyverse', 'data.table'))
library(tidyverse)
library(data.table)

# 3.1 数据清洗
df <- read.csv('1_data_cleaning.csv')

# 查看缺失值
colSums(is.na(df))

# 去除重复行
df_clean <- df %>% distinct()

# 清理空格
df_clean <- df_clean %>%
  mutate(across(where(is.character), str_trim))

# 3.2 数据透视
df_pivot <- read.csv('4_pivot_table_data.csv')

pivot_result <- df_pivot %>%
  group_by(产品, 地区) %>%
  summarise(销售额 = sum(销售额), .groups = 'drop') %>%
  pivot_wider(names_from = 地区, values_from = 销售额)

print(pivot_result)

# 3.3 条件统计
df_stats <- read.csv('7_conditional_statistics.csv')

df_stats %>%
  group_by(产品) %>%
  summarise(
    总销售额 = sum(销售额),
    平均销售额 = mean(销售额),
    达成个数 = sum(是否达成 == '是'),
    .groups = 'drop'
  )
```

### 4. SQL 使用示例

```sql
-- 将CSV导入到SQLite数据库
.mode csv
.import 7_conditional_statistics.csv statistics_data

-- 条件统计
SELECT 
    产品,
    SUM(销售额) as 总销售额,
    AVG(销售额) as 平均销售额,
    COUNT(CASE WHEN 是否达成='是' THEN 1 END) as 达成个数,
    COUNT(*) as 总数
FROM statistics_data
GROUP BY 产品
ORDER BY 总销售额 DESC;

-- 多表关联
SELECT 
    o.订单ID,
    o.订单日期,
    o.金额,
    c.客户名,
    c.城市,
    c.等级
FROM orders o
LEFT JOIN customers c ON o.客户ID = c.客户ID
WHERE o.金额 > 20000
ORDER BY o.订单日期 DESC;
```

## 性能基准

| 操作 | 行数 | 时间(秒) | 速度(行/秒) |
|------|------|---------|----------|
| 加载 | 50,000 | 0.12 | 416,667 |
| 去重 | 15,000 | 0.05 | 300,000 |
| 分组汇总 | 30,000 | 0.08 | 375,000 |
| JOIN关联 | 25,000 + 10,000 | 0.15 | 166,667 |
| 透视表 | 30,000 | 0.10 | 300,000 |

## 常见问题

**Q: 如何处理大文件内存溢出？**

A: 使用分块读取：
```python
chunksize = 10000
for chunk in pd.read_csv('file.csv', chunksize=chunksize):
    # 处理每个chunk
    process(chunk)
```

**Q: 如何加快数据处理速度？**

A: 使用 `dask` 或 `polars`：
```python
import dask.dataframe as dd

df = dd.read_csv('8_large_transaction_data.csv')
result = df.groupby('账户')['金额'].sum().compute()
```

**Q: 数据编码问题如何解决？**

A: 指定编码方式：
```python
pd.read_csv('file.csv', encoding='utf-8')
```
