# 导入requests包
import requests, sys, datetime, time, threadpool
import oss2

# # 1. 组装请求
# url = "http://httpbin.org/get"  # 这里只有url，字符串格式
# # 2. 发送请求，获取响应
# res = requests.get(url) # res即返回的响应对象
# # 3. 解析响应
# print(res.text)  # 输出响应的文本求
# url = "http://httpbin.org/get"  # 这里只有url，字符串格式
# # 2. 发送请求，获取响应
# res = requests.get(url) # res即返回的响应对象
# # 3. 解析响应
# print(res.text)  # 输出响应的文本

access_key_id = 'LTAI4G1XrVLA43nDnEsC9ay4'
access_key_secret = 'Ggi0CQ5XMXVsstAITypQptRESrDFhh'
bucket_name = 'instai-wh'
endpoint = 'http://oss-cn-chengdu.aliyuncs.com'
# 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
auth = oss2.Auth(access_key_id, access_key_secret)
# Endpoint以杭州为例，其它Region请按实际情况填写。
bucket = oss2.Bucket(auth, endpoint, bucket_name)


# 判断文件是否存在
def dose_file_exist_in_oss(file_name):
    exist = bucket.object_exists(file_name)

    # 返回值为true表示文件存在，false表示文件不存在。
    return exist


# 进度条
def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()


exist_list = []


# 上传文件到oss
def upload_file(file_name):
    prefix = 'http://dl.wdcloud.cc/'
    start = time.time()
    # 已存在的文件名称
    exist_file = ''

    # 文件地址
    url = prefix + file_name

    # 先判断文件是否已存在 ，存在不上传
    exist = dose_file_exist_in_oss(file_name)
    if exist:
        exist_file = file_name
        exist_list.append(exist_file)
    else:
        reRequest = True
        while reRequest:
            try:
                # 获取文件流
                input = requests.get(url)
                # 上传
                bucket.put_object(file_name, input, progress_callback=percentage)
                bucket.put_object_acl(file_name, oss2.OBJECT_ACL_PUBLIC_READ_WRITE)
                end = time.time()
                run = end - start
                print(file_name, ' 上传成功', '用时 : %.5f s' % run)
                reRequest = False
            except Exception as e:
                reRequest = True

    return exist_file


# 批量删除文件
def batch_del_file(file_name_list):
    result = bucket.batch_delete_objects(file_name_list)
    # 打印成功删除的文件名。
    print('\n'.join(result.deleted_keys))


# 读取文件
def read_file(file_name):
    try:
        f = open(file_name, 'r', encoding="utf-8");
        lines = f.readlines()
        content = ''
        for line in lines:
            content += line

        file_name_list = []
        if content != '':
            for c in content.split(","):
                file_name_list.append(c)

        return file_name_list
    except Exception as result:
        print("读错误:", result)
    finally:
        f.close()


#         ************************** 文件删除 *******************************

# del_file_list = ["wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg","wh3/M07/B1/13/poYBAF43LOaASPV6ABN0JLXxsgE643.jpg","wh1/M03/6A/69/oYYBAF43LOiARci9ACqH-xHWJvI290.jpg","wh2/M06/3B/1D/pIYBAF43LOmAYOkTADE9baf5RnI206.jpg"]
#
# batch_del_file(del_file_list)

#         ************************** 判断文件是否存在 *******************************
# file_name = "wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg"
#
# exist = dose_file_exist_in_oss(file_name)
#
# print(exist)

#         ************************** 多文件上传 - 不用线程池 *******************************
# del_file_list = ["wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg","wh3/M07/B1/13/poYBAF43LOaASPV6ABN0JLXxsgE643.jpg","wh1/M03/6A/69/oYYBAF43LOiARci9ACqH-xHWJvI290.jpg","wh2/M06/3B/1D/pIYBAF43LOmAYOkTADE9baf5RnI206.jpg"]
#
# batch_del_file(del_file_list)
# start_time = time.time()
# file_list = ["wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg", "wh3/M07/B1/13/poYBAF43LOaASPV6ABN0JLXxsgE643.jpg",
#              "wh1/M03/6A/69/oYYBAF43LOiARci9ACqH-xHWJvI290.jpg", "wh2/M06/3B/1D/pIYBAF43LOmAYOkTADE9baf5RnI206.jpg"]
# prefix = 'http://dl.wdcloud.cc/'
# exist_list = []
# for file_name in file_list:
#     exist_file = upload_file(file_name)
#     if exist_file != '':
#         exist_list.append(exist_file)
# end_time = time.time()
# running_time = end_time - start_time
#
# print("已存在的文件", "*" * 10, "长度：", "*" * 10, len(exist_list), "*" * 10)
# print("已存在的文件", "*" * 10, exist_list)
# print('用时 : %.5f s' % running_time)

#         ************************** 多文件上传 - 使用线程池 *******************************
# del_file_list = ["wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg","wh3/M07/B1/13/poYBAF43LOaASPV6ABN0JLXxsgE643.jpg","wh1/M03/6A/69/oYYBAF43LOiARci9ACqH-xHWJvI290.jpg","wh2/M06/3B/1D/pIYBAF43LOmAYOkTADE9baf5RnI206.jpg"]
#
# batch_del_file(del_file_list)
try:
    file_list = read_file('人人通社区附件迁移10000 - 20.txt')

    # print(len(file_list))
    # print(file_list)
    start_time = time.time()
    print(datetime.datetime.now())
    # file_list = ["wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg", "wh3/M07/B1/13/poYBAF43LOaASPV6ABN0JLXxsgE643.jpg",
    #              "wh1/M03/6A/69/oYYBAF43LOiARci9ACqH-xHWJvI290.jpg", "wh2/M06/3B/1D/pIYBAF43LOmAYOkTADE9baf5RnI206.jpg"]
    pool = threadpool.ThreadPool(75)  # 线程池设置

    # makeRequests构造线程task请求,第一个参数是线程函数,第二个是参数数组
    tasks = threadpool.makeRequests(upload_file, file_list)
    [pool.putRequest(task) for task in tasks]
    # 列表推导式,putRequest向线程池里加task,让pool自己去调度task
    pool.wait()  # 等所有任务结束
    end_time = time.time()
    running_time = end_time - start_time

    print('用时 : %.5f s' % running_time)
    print("已存在的数量" , len(exist_list))
except Exception as e:
    print(e)

#         ************************** 单文件上传 *******************************
# start_time = datetime.datetime.now()
# file_name = "wh3/M00/77/E8/pYYBAF43LOaAOmEcAA829MJGVUA409.jpg"
# # print(url)
# exist_list = []
# exist_file = upload_file(file_name)
# if exist_file != '':
#     exist_list.append(exist_file)
#
# print("已存在的文件", "*" * 10, "长度：", "*" * 10, len(exist_list), "*" * 10)
# print("已存在的文件", "*" * 10, exist_list)
# time.sleep(3)
#
# end_time = datetime.datetime.now()
#
# print("开始时间", "*" * 20, start_time)
# print("结束时间", "*" * 20, end_time)
