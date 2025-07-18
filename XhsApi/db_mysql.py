import pymysql
from pymysql.cursors import DictCursor
import logging
from datetime import datetime
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'Aa123Aa',
    'db': 'self_other_project'
}
# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',filename='db_mysql.log')

def create_or_insert_data(table_name, data, check=False):
    if not isinstance(data, (dict, list)):
        raise TypeError("数据必须是字典或字典列表类型")
    
    if isinstance(data, dict):
        data_list = [data]
    else:  # list类型
        if not data or not all(isinstance(item, dict) for item in data):
            raise ValueError("列表必须包含字典类型的数据")
        data_list = data

    connection = pymysql.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        charset='utf8mb4',
        cursorclass=DictCursor
    )
    cursor = connection.cursor()

    try:
        if check:
        # 检查表是否存在
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            table_exists = cursor.fetchone()

            if not table_exists:
                # 创建表
                columns = []
                for key, value in data.items():
                    column_type = "INT" if isinstance(value, int) else "VARCHAR(255)"
                    if isinstance(value, float):
                        column_type = "FLOAT"
                    if isinstance(value, datetime):
                        column_type = "DATETIME"
                    columns.append(f"`{key}` {column_type}")
                create_table_sql = f"CREATE TABLE {table_name} ({', '.join(columns)});"
                cursor.execute(create_table_sql)
                logging.info(f"表 {table_name} 创建成功。")

            # 检查并添加缺失的列
            cursor.execute(f"DESCRIBE {table_name}")
            existing_columns = [col['Field'] for col in cursor.fetchall()]
            for key in data.keys():
                if key not in existing_columns:
                    column_type = "VARCHAR(255)" if isinstance(data[key], int) else "INT"
                    if isinstance(data[key], float):
                        column_type = "FLOAT"
                    if isinstance(data[key], datetime):
                        column_type = "DATETIME"
                    alter_sql = f"ALTER TABLE {table_name} ADD COLUMN `{key}` {column_type};"
                    cursor.execute(alter_sql)
                    logging.info(f"列 `{key}` 添加到表 {table_name}。")

        # 插入数据
        if data_list:
            # 获取第一条数据的键作为列名
            columns = list(data_list[0].keys())
            columns_str = ', '.join([f"`{key}`" for key in columns])
            placeholders = ', '.join(['%s'] * len(columns))  # 使用参数化查询
            insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            # 准备批量插入的数据
            values = []
            for data_item in data_list:
                formatted_data = data_item.copy()
                for key, value in formatted_data.items():
                    if isinstance(value, datetime):
                        formatted_data[key] = value.strftime("%Y-%m-%d %H:%M:%S")  # 格式化时间
                values.append([formatted_data[key] for key in columns])
            
            # 执行批量插入
            cursor.executemany(insert_sql, values)
            connection.commit()
            logging.info(f"数据插入成功：共{len(data_list)}条数据，每条{len(columns)}项")

    except Exception as e:
        logging.error(f"发生错误：{e}")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()
