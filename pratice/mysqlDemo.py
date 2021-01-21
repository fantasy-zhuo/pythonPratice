# 数据库连接demo
import pymysql

# 连接数据库，创建连接对象connection
# 连接对象作用是：连接数据库、发送数据库信息、处理回滚操作（查询中断时，数据库回到最初状态）、创建新的光标对象
connection = pymysql.connect(host='localhost',  # host属性
                             user='root',  # 用户名
                             password='root',  # 此处填登录数据库的密码
                             db='mysql'  # 数据库名
                             )
