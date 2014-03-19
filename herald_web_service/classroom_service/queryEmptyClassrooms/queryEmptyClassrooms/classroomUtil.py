# encoding: UTF-8
''' 处理数据库 '''
import MySQLdb, urllib, json
from django.db import connection
from models import CourseInfo
import settings

# 查询丁家桥，比较奇葩
def getDJQ(classWeek, classWeekNum, beginTime, endTime):
    if settings.TERM[-1: ] == '2':
        classWeekNum += 4 # 奇葩的丁家桥在第二学期要+4
    # 连接数据库
    cursor = connection.cursor() # 使用django的connection

    classrooms = [] # 教室列表

    # 得到所有的教室
    sqlGetAllClassrooms = "SELECT DISTINCT classPlace FROM course WHERE `classPlace` LIKE %s"
    cursor.execute(sqlGetAllClassrooms, ['%-%'])
    rs = cursor.fetchall()
    for r in rs:
        classrooms.append(r[0])

    # 得到所有上课的教室
    if classWeekNum % 2 == 0: # 双周
        sqlGetClassroomsUnderUsed = "SELECT DISTINCT classPlace FROM course WHERE " \
            + "((classType != 1) " \
            + "AND (`classWeek` = %s) AND (`beginWeekNum` <= %s AND `endWeekNum` >= %s) " \
            + "AND ((%s - classEndTime) * (%s - classBeginTime) <= 0))" 
    else: # 单周
        sqlGetClassroomsUnderUsed = "SELECT DISTINCT classPlace FROM course WHERE " \
            + "((classType != -1) " \
            + "AND (`classWeek` = %s) AND (`beginWeekNum` <= %s AND `endWeekNum` >= %s) " \
            + "AND ((%s - classEndTime) * (%s - classBeginTime) <= 0))" 
    try:
        cursor.execute(sqlGetClassroomsUnderUsed, [classWeek, classWeekNum, classWeekNum, beginTime, endTime])
    except: 
        return []
    rs = cursor.fetchall()

    # 去除掉上课的教室
    for r in rs:
        if classrooms.__contains__(r[0]):
            classrooms.remove(r[0])

    # Exception
    try:
        classrooms.remove("九龙湖其它-大活322")
    except:
        pass


    # 将教室分校区
    JiuLongHu = []
    SiPaiLou = []
    DingJiaQiao = []
    for room in classrooms:
        if room.find('教') != -1 or room.find('九龙湖') != -1:
            JiuLongHu.append(room)
        elif room.find('基') != -1 or (room.find('综合') != -1 and room.find('综合楼') == -1)\
            or room.find('公卫') != -1:
            DingJiaQiao.append(room)
        else:
            SiPaiLou.append(room)
    #JiuLongHu = sortClassroomsByCN(JiuLongHu)
    return DingJiaQiao

# 查询第(classWeekNum)周星期(classWeek)第(beginTime)节到第(endTime)节的空教室
def getEmptyClassrooms(classWeek, classWeekNum, beginTime, endTime):
    # 连接数据库
    cursor = connection.cursor() # 使用django的connection

    classrooms = [] # 教室列表

    # 得到所有的教室
    sqlGetAllClassrooms = "SELECT DISTINCT classPlace FROM course WHERE `classPlace` LIKE %s"
    cursor.execute(sqlGetAllClassrooms, ['%-%'])
    rs = cursor.fetchall()
    for r in rs:
        classrooms.append(r[0])

    # 得到所有上课的教室
    if classWeekNum % 2 == 0: # 双周
        sqlGetClassroomsUnderUsed = "SELECT DISTINCT classPlace FROM course WHERE " \
            + "((classType != 1) " \
            + "AND (`classWeek` = %s) AND (`beginWeekNum` <= %s AND `endWeekNum` >= %s) " \
            + "AND ((%s - classEndTime) * (%s - classBeginTime) <= 0))" 
    else: # 单周
        sqlGetClassroomsUnderUsed = "SELECT DISTINCT classPlace FROM course WHERE " \
            + "((classType != -1) " \
            + "AND (`classWeek` = %s) AND (`beginWeekNum` <= %s AND `endWeekNum` >= %s) " \
            + "AND ((%s - classEndTime) * (%s - classBeginTime) <= 0))" 
    try:
        cursor.execute(sqlGetClassroomsUnderUsed, [classWeek, classWeekNum, classWeekNum, beginTime, endTime])
    except: 
        return {'SPL': [], 'JLH': [], 'DJQ': []}
    rs = cursor.fetchall()

    # 去除掉上课的教室
    for r in rs:
        if classrooms.__contains__(r[0]):
            classrooms.remove(r[0])

    # Exception
    try:
        classrooms.remove("九龙湖其它-大活322")
    except:
        pass


    # 将教室分校区
    JiuLongHu = []
    SiPaiLou = []
    DingJiaQiao = []
    for room in classrooms:
        if room.find('教') != -1:
            JiuLongHu.append(room)
        elif room.find('基') != -1 or (room.find('综合') != -1 and room.find('综合楼') == -1)\
            or room.find('公卫') != -1:
            DingJiaQiao.append(room)
        else:
            SiPaiLou.append(room)
    JiuLongHu = sortClassroomsByCN(JiuLongHu)
    return {'SPL': SiPaiLou, 'JLH': JiuLongHu, 'DJQ': DingJiaQiao}


# 根据中文顺序对列表排序，返回排好序的列表
def sortClassroomsByCN(l):
    # 将九龙湖的教室进行排序，花费空间节省时间
    tmpJLH = []
    for room in l:
        if room.find("教一") != -1:
            tmpJLH.append(room.replace("教一", "J1"))
        if room.find("教二") != -1:
            tmpJLH.append(room.replace("教二", "J2"))
        if room.find("教三") != -1:
            tmpJLH.append(room.replace("教三", "J3"))
        if room.find("教四") != -1:
            tmpJLH.append(room.replace("教四", "J4"))
        if room.find("教五") != -1:
            tmpJLH.append(room.replace("教五", "J5"))
        if room.find("教六") != -1:
            tmpJLH.append(room.replace("教六", "J6"))
        if room.find("教七") != -1:
            tmpJLH.append(room.replace("教七", "J7"))
        if room.find("教八") != -1:
            tmpJLH.append(room.replace("教八", "J8"))

    tmpJLH.sort()
    l = []
    for room in tmpJLH:
        if room.find("J1") != -1:
            l.append(room.replace("J1", "教一"))
        if room.find("J2") != -1:
            l.append(room.replace("J2", "教二"))
        if room.find("J3") != -1:
            l.append(room.replace("J3", "教三"))
        if room.find("J4") != -1:
            l.append(room.replace("J4", "教四"))
        if room.find("J5") != -1:
            l.append(room.replace("J5", "教五"))
        if room.find("J6") != -1:
            l.append(room.replace("J6", "教六"))
        if room.find("J7") != -1:
            l.append(room.replace("J7", "教七"))
        if room.find("J8") != -1:
            l.append(room.replace("J8", "教八"))
    return l


