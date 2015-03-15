#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-13 18:23:11
# @Author  : yml_bright@163.com

import mod.models.db

from datetime import date as datelib, timedelta
import config
import MySQLdb
import copy

# 所有教室的列表
classrooms = None

# @brief 检查参数是否满足通用查询的要求
#
# @return 如果参数符合要求，返回tuple(campus, week, date, start, end)，除了campus为str外，其他均为int
#   如果不符合要求，返回None。
def filter_common(campus, week, date, start_lesson, end_lesson):
    try:
        # some default limitation
        week_low = 1
        week_high = 4
        date_low = 1
        date_high = 7
        start_lesson_low = 1
        start_lesson_high = 13
        end_lesson_low = 1
        end_lesson_high = 13
        campus_options = ['djq', 'spl', 'jlh']

        term_tail = config.course_term_id[-1:]

        # change limitation according to term_tail and campus
        if term_tail == '1':
            pass
        elif term_tail == '2':
            if campus == 'djq':
                week_low = 5
                week_high = 20
            elif campus == 'jlh' or campus == 'spl':
                week_high = 16
        elif term_tail == '3':
            week_high = 16

        # convert to integer
        week_int = int(week)
        date_int = int(date)
        start_lesson_int = int(start_lesson)
        end_lesson_int = int(end_lesson)
    except:
        return None

    if campus in campus_options \
            and week_low <= week_int <= week_high \
            and date_low <= date_int <= date_high \
            and start_lesson_low <= start_lesson_int <= start_lesson_high \
            and end_lesson_low <= end_lesson_int <= end_lesson_high \
            and start_lesson_int <= end_lesson_int:
        return (campus, week_int, date_int, start_lesson_int, end_lesson_int)

    return None


# @brief 检查参数是否满足快速查询的要求
#   先将参数转换为通用查询的参数，接着使用filter_common进行检查。
#
# @return 同filter_common
def filter_quick(campus, today_or_tomorrow, start_lesson, end_lesson):
    if today_or_tomorrow not in ['today', 'tomorrow']:
        return None

    # 将今天/明天转换为相应的日期
    start_date = datelib(config.start_year, config.start_month, config.start_day)
    check_date = datelib.today()
    if today_or_tomorrow == 'tomorrow':
        try:
            check_date = datelib(check_date.year, check_date.month, check_date.day + 1)
        except:
            # 日超过了，累加到月上
            try:
                check_date = datelib(check_date.year, check_date.month + 1, check_date.day)
            except:
                # 月超过了，累加到年上
                check_date = datelib(check_date.year + 1, check_date.month, check_date.day)

    # 和第一周周一的日期比较，计算出第几周周几
    delta = check_date - start_date
    week = delta.days / 7 + 1
    date = check_date.isoweekday()

    return filter_common(campus, week, date, start_lesson, end_lesson)


# @brief 获取所有教室列表的方法
def get_classroom_list():
    connection = MySQLdb.connect(
        host=mod.models.db.DB_HOST, user=mod.models.db.DB_USER, passwd=mod.models.db.DB_PWD, db=mod.models.db.DB_NAME, charset='utf8')
    cursor = connection.cursor()

    global classrooms
    classrooms = []
    ALL_CLASSROOM_SQL = 'SELECT DISTINCT course_place FROM course_schedule WHERE course_place LIKE %s'
    cursor.execute(ALL_CLASSROOM_SQL, ['%-%'])
    rs = cursor.fetchall()
    for r in rs:
        classrooms.append(r[0])

    # 一些需要额外去除的教室
    try:
        classrooms.remove(u"九龙湖其它-大活322")
    except:
        pass

    connection.close()


# @brief 根据指定参数获取空教室
#   通过查询占用教室，接着从所有教室列表中筛选掉占用教室得到。
def get_free_classrooms(campus, week, date, start_lesson, end_lesson):
    global classrooms

    try:
        connection = MySQLdb.connect(
            host=mod.models.db.DB_HOST, user=mod.models.db.DB_USER, passwd=mod.models.db.DB_PWD, db=mod.models.db.DB_NAME, charset='utf8')
        cursor = connection.cursor()

        rtn_classrooms = copy.deepcopy(classrooms)
        # 判断单双周
        if week % 2 == 0:
            search_course_type = 1 # 双周，设置为单周
        else:
            search_course_type = 2 # 单周，设置为双周

        CLASSROOM_USING_SQL = 'SELECT DISTINCT course_place FROM course_schedule WHERE ' \
                + '((course_type != %s) ' \
                + "AND (course_date = %s) " \
                + "AND (course_start_week <= %s AND course_end_week >= %s)" \
                + "AND ((%s - course_end_lesson) * (%s - course_start_lesson) <= 0))"
        
        cursor.execute(CLASSROOM_USING_SQL, 
            [search_course_type, date, week, week, start_lesson, end_lesson])
        rs = cursor.fetchall()
        for r in rs:
            if rtn_classrooms.__contains__(r[0]):
                rtn_classrooms.remove(r[0])
    except:
        return [u'DB_ERROR']

    jlh = []
    djq = []
    spl = []

    # 根据各大校区教室名称特征区分
    for room in rtn_classrooms:
        if room.find(u'教') != -1:
            jlh.append(room)
        elif room.find(u'基') != -1 \
                or (room.find(u'综合') != -1 and room.find(u'综合楼') == -1) \
                or room.find(u'公卫') != -1:
            djq.append(room)
        else:
            spl.append(room)
    if campus == 'jlh':
        return sort_classroom_by_CN(jlh)
    elif campus == 'djq':
        return djq 
    elif campus == 'spl':
        return spl
    else:
        return []


# 根据中文顺序对列表排序，返回排好序的列表
def sort_classroom_by_CN(l):
    # 将九龙湖的教室进行排序，花费空间节省时间
    tmpJLH = []
    for room in l:
        if room.find(u"教一") != -1:
            tmpJLH.append(room.replace(u"教一", "J1"))
        if room.find(u"教二") != -1:
            tmpJLH.append(room.replace(u"教二", "J2"))
        if room.find(u"教三") != -1:
            tmpJLH.append(room.replace(u"教三", "J3"))
        if room.find(u"教四") != -1:
            tmpJLH.append(room.replace(u"教四", "J4"))
        if room.find(u"教五") != -1:
            tmpJLH.append(room.replace("教五", "J5"))
        if room.find(u"教六") != -1:
            tmpJLH.append(room.replace(u"教六", "J6"))
        if room.find(u"教七") != -1:
            tmpJLH.append(room.replace(u"教七", "J7"))
        if room.find(u"教八") != -1:
            tmpJLH.append(room.replace(u"教八", "J8"))

    tmpJLH.sort()
    l = []
    for room in tmpJLH:
        if room.find("J1") != -1:
            l.append(room.replace("J1", u"教一"))
        if room.find("J2") != -1:
            l.append(room.replace("J2", u"教二"))
        if room.find("J3") != -1:
            l.append(room.replace("J3", u"教三"))
        if room.find("J4") != -1:
            l.append(room.replace("J4", u"教四"))
        if room.find("J5") != -1:
            l.append(room.replace("J5", u"教五"))
        if room.find("J6") != -1:
            l.append(room.replace("J6", u"教六"))
        if room.find("J7") != -1:
            l.append(room.replace("J7", u"教七"))
        if room.find("J8") != -1:
            l.append(room.replace("J8", u"教八"))
    return l


# 在导入模块时尝试获取所有教室列表，出错则报错退出程序
try:
    get_classroom_list()
except:
    print '初始化qec/utils失败.'
    #exit()

