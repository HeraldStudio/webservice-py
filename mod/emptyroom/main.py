#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-03-13 13:50:42
# @Author  : yml_bright@163.com

# 把config所在文件夹加入搜索路径
import sys
sys.path.insert(0, '../models')

import MySQLdb
import copy
import requests
import db
import config
from lxml import etree as ET

# 设置编码，保证中文为utf-8编码
reload(sys)
sys.setdefaultencoding('utf-8')

# 数据来源URL
ACADEMY_COURSE_LIST_URL = 'http://xk.urp.seu.edu.cn/jw_service/service/academyClassLook.action'
ACADEMY_EXAM_LIST_URL = 'http://xk.urp.seu.edu.cn/jw_service/service/runAcademyClassDepartmentQueryAction.action'
ACADEMY_PREFIX_URL = 'http://xk.urp.seu.edu.cn/jw_service/service/'

# SQL
COURSE_SQL = "INSERT INTO course_info VALUES (%s, %s, %s, %s, %s)"
COURSE_SCHEDULE_SQL = "INSERT INTO course_schedule VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
EXAM_SCHEDULE_SQL = "INSERT INTO exam_schedule VALUES (%s, %s, %s, %s, %s)"

# 读取配置文件
course_term = config.course_term
course_term_id = config.course_term_id
exam_term = config.exam_term
host = db.DB_HOST
username = db.DB_USER
password = db.DB_PWD
db_name = db.DB_NAME


# @brief 清空（truncate）数据库中指定的表
# 
# @param tb_name 要清空的表名
def truncate_table(tb_name):
    connection = MySQLdb.connect(
        host=host, user=username, passwd=password, db=db_name, charset='utf8')
    cursor = connection.cursor()

    command = 'SET FOREIGN_KEY_CHECKS = 0;'
    cursor.execute(command)
    connection.commit()
    command = 'truncate %s;' % tb_name
    cursor.execute(command)
    connection.commit()
    command = 'SET FOREIGN_KEY_CHECKS = 1'
    cursor.execute(command)
    connection.commit()


# @brief 更新考试记录表exam_schedule
#
# @logic
# 1. 从院系列表页获取各院系考试安排的链接。
# 2. 针对每个链接，获取其页面。
# 3. 过滤掉非选中学期的考试，分解字段，插入exam_schedule表中。
def update_exam():
    response = requests.get(ACADEMY_EXAM_LIST_URL)
    html = ET.HTML(response.text)
    department_nodes = html.xpath('//a[@target]')

    connection = MySQLdb.connect(
        host=host, user=username, passwd=password, db=db_name, charset='utf8')
    cursor = connection.cursor()

    log_string = ""
    lineno = 1
    err_lines = []
    last_success_sql = ''

    for department in department_nodes:
        academy_href = department.attrib['href']
        academy_url = ACADEMY_PREFIX_URL + academy_href

        response = requests.get(academy_url)
        html = ET.HTML(response.text)
        xpath_condition = "//tr[@onmouseover]/td[2][contains(text(), '%s')]/parent::*" % exam_term
        exams = html.xpath(xpath_condition)

        for exam in exams:
            tds = exam.xpath('.//td')

            exam_campus = tds[2].text.strip()
            exam_place = tds[6].text.strip()
            exam_datetime = tds[5].text.strip()
            (exam_date, exam_time) = split_exam_datetime(exam_datetime)

            values = [exam_term, exam_campus, exam_place, exam_date, exam_time]
            sql = EXAM_SCHEDULE_SQL % (exam_term, exam_campus, exam_place, exam_date, exam_time)
            try:
                cursor.execute(EXAM_SCHEDULE_SQL, values)
                connection.commit()
                log_string += "EXECUTE: " + sql + '\n'
                last_success_sql = sql
                lineno += 1
            except:
                # 过滤掉重复执行相同sql导致的错误
                if last_success_sql != sql:
                    err_lines.append(lineno)
                    lineno += 1
                    log_string += 'ERROR: ' + sql + '\n'

    connection.commit()
    connection.close()

    log_string += '\n------------Update Exam Result-------------\n';
    report_string = 'Error(' + str(len(err_lines)) + ')\n'
    log_string += report_string
    for i in err_lines:
        log_string += ('err at line ' + str(i) + '\n')
    log_file = open('exam_log', 'w')
    log_file.write(log_string)
    log_file.close()
    print report_string, 'Check log file for detail.'


# 清空exam_schedule表
def truncate_exam():
    truncate_table('exam_schedule')


# @brief 分割如【2014-06-16 02:00(星期一)】这样的字符串
#   时间将被映射成为相应的数字。
#
# @param dt 要分割的字符串
#
# @return 返回tuple(date, time)
#
# @logic
# 1. 分割成两段，第一段为考试日期，第二段具体时间。
# 2. 考试日期转换成整型，格式为YYYYMMDD。
# 3. 考试时间根据时间划分为相应数据，0（上午09:00），1（02:00），2（其他时间）。
def split_exam_datetime(dt):
    split_dt = dt.split(' ')
    part_1 = split_dt[0]
    part_2 = split_dt[1]

    if part_1:
        split_part_1 = part_1.split('-')
        date = ""
        for p in split_part_1:
            date += p
        date = int(date)

    if part_2.find('02:00'):
        time = 1
    elif part_2.find('09:00'):
        time = 0
    else:
        time = 2

    return (date, time)


# @brief 更新course_info和course_schedule
#
# @logic
# 1. 获取各个院系的开课列表页面，提取各院系开课链接。
# 2. 针对每个链接，获取满足条件（如学期）的课程（行）。
# 3. 对每一项在course_info表中插入新课程。
# 4. 解析上课时间地点字段，插入course_schedule中。
def update_course():
    response = requests.get(ACADEMY_COURSE_LIST_URL)
    html = ET.HTML(response.text)
    department_nodes = html.xpath('//a[@target]')

    connection = MySQLdb.connect(
        host=host, user=username, passwd=password, db=db_name, charset='utf8')
    cursor = connection.cursor()

    log_string = ""
    lineno = 1
    err_lines = []

    for department in department_nodes:
        academy_href = department.attrib['href']
        academy_info = department.text.strip()
        academy_id = academy_info[academy_info.find('[') + 1: academy_info.find(']')].strip()
        academy_name = academy_info[academy_info.find(']') + 1:].strip()
        print academy_name
        academy_url = ACADEMY_PREFIX_URL + academy_href

        response = requests.get(academy_url)
        html = ET.HTML(response.text)
        xpath_condition = "//tr[@onmouseover]/td[2][contains(text(), '%s')]/parent::*" % course_term
        courses = html.xpath(xpath_condition)

        for course in courses:
            tds = course.xpath('.//td')

            course_number = tds[0].text.strip()
            course_id = (academy_id + course_term_id + course_number).strip()
            # course_term = course_term
            course_name = tds[2].text.strip()
            course_for_student = tds[3].text.strip()
            course_teacher = tds[4].text.strip()
            course_time_and_place = tds[5].text
            course_schedule_details = split_course_info(course_time_and_place)

            values = [course_id, course_term, course_name, course_for_student, course_teacher]
            sql = COURSE_SQL % (course_id, 
                course_term, course_name, course_for_student, course_teacher)
            try:
                cursor.execute(COURSE_SQL, values)
                connection.commit()
                log_string += ('EXECUTE: ' + sql + '\n') 
                lineno += 1
            except:
                log_string += ('ERROR: ' + sql + '\n')
                err_lines.append(lineno)
                lineno += 1

            last_success_sql = ''
            for detail in course_schedule_details:
                course_start_week = str(detail['course_start_week'])
                course_end_week = str(detail['course_end_week'])
                course_date = str(detail['course_date'])
                course_start_lesson = str(detail['course_start_lesson'])
                course_end_lesson = str(detail['course_end_lesson'])
                course_type = str(detail['course_type'])
                course_place = str(detail['course_place'])

                values = [course_id, course_start_week, course_end_week, course_date, 
                    course_start_lesson, course_end_lesson, course_type, course_place]
                sql = COURSE_SCHEDULE_SQL % (course_id, course_start_week, 
                    course_end_week, course_date, course_start_lesson, course_end_lesson, 
                    course_type, course_place)
                try:
                    cursor.execute(COURSE_SCHEDULE_SQL, values)
                    connection.commit()
                    log_string += ('EXECUTE: ' + sql + '\n')
                    last_success_sql = sql
                    lineno += 1
                except:
                    # 过滤掉重复执行相同sql导致的错误
                    if last_success_sql != sql:
                        log_string += ('ERROR: ' + sql + '\n')
                        err_lines.append(lineno)
                        lineno += 1

    connection.commit()
    connection.close()
    
    log_string += '\n------------Update Course Result------------\n';
    report_string = 'Error(' + str(len(err_lines)) + ')\n'
    log_string += report_string
    for i in err_lines:
        log_string += ('err at line ' + str(i) + '\n')
    log_file = open('course_log', 'w')
    log_file.write(log_string)
    log_file.close()
    print report_string, 'Check log file for detail.'


# 清空course_info和course_schedule表
def truncate_course():
    truncate_table('course_info')
    truncate_table('course_schedule')


# @brief 分割如【[1-16周] 周二(3-4)教七-30A,周四(双3-4)教七-30A】这样的数据
#
# @param course_info 如上所述的字符串
#
# @return detail的list，list中每一项参见detail_format的格式
# 
# @logic
# 1. 将字段分为两段。
# 2. 前半段为[1-16周]这样的通用信息（一个字段记录可切为多个表中记录）。
# 3. 后半段根据逗号进行分割，再针对每一项提取信息，封装成一个detail，加入返回的结果。
# 4. 返回结果（detail list）。
def split_course_info(course_info):
    split_result = []
    detail_format = {
        'course_id': 1,
        'course_start_week': -1,
        'course_end_week': -1,
        'course_date': -1,
        'course_start_lesson': -1,
        'course_end_lesson': -1,
        'course_type': 0,
        'course_place': ""
    }

    split_pos = course_info.find(']')
    part_1 = course_info[0: split_pos + 1].strip()
    part_2 = course_info[split_pos + 1:].strip()

    if part_1:
        part_1 = part_1.replace('[', '').replace(u'周]', '').strip()
        dash_pos = part_1.find('-')
        detail_format['course_start_week'] = part_1[0: dash_pos].strip()
        detail_format['course_end_week'] = part_1[dash_pos + 1:].strip()

    if part_2:
        split_part_2 = part_2.split(',')

        for p in split_part_2:
            p = p.strip()
            if p:
                detail_copy = copy.deepcopy(detail_format)

                detail_copy['course_place'] = p[p.find(')') + 1:].strip()

                if p.find(u'单') != -1:
                    detail_copy['course_start_lesson'] = p[
                        p.find(u'单') + len(u'单'): p.find('-')].strip()
                    detail_copy['course_end_lesson'] = p[
                        p.find('-') + 1: p.find(')')].strip()
                    detail_copy['course_type'] = 1
                elif p.find(u'双') != -1:
                    detail_copy['course_start_lesson'] = p[
                        p.find(u'双') + len(u'双'): p.find('-')].strip()
                    detail_copy['course_end_lesson'] = p[
                        p.find('-') + 1: p.find(')')].strip()
                    detail_copy['course_type'] = 2
                else:
                    detail_copy['course_start_lesson'] = p[
                        p.find('(') + 1: p.find('-')].strip()
                    detail_copy['course_end_lesson'] = p[
                        p.find('-') + 1: p.find(')')].strip()

                date = p[0: p.find('(')].strip()
                if date == '周一':
                    detail_copy['course_date'] = 1
                elif date == '周二':
                    detail_copy['course_date'] = 2
                elif date == '周三':
                    detail_copy['course_date'] = 3
                elif date == '周四':
                    detail_copy['course_date'] = 4
                elif date == '周五':
                    detail_copy['course_date'] = 5
                elif date == '周六':
                    detail_copy['course_date'] = 6
                elif date == '周日':
                    detail_copy['course_date'] = 7

                split_result.append(detail_copy)

    return split_result


# 更新所有的表
def update_all():
    truncate_course()
    truncate_exam()
    update_course()
    update_exam()


# 打印帮助信息
def print_help():
    print \
    u'''
    工具简介：获取上课教室及考试教室数据的爬虫
    
    用法：get_info.py [cmd]
    
    cmd：（所有的更新命令都会清空原表，请注意备份）
    \t -ua, --update-all 更新所有的表
    \t -uc, --update-course 更新和上课教室相关的表
    \t -ue, --update-exam 更新和考试教室相关的表
    \t -h, --help 打印帮助信息
    '''


if __name__ == "__main__":
    if len(sys.argv) == 2:
        cmd = sys.argv[1]

        if cmd == '-ua' or cmd == '--update_all':
            update_all()
        elif cmd == '-uc' or cmd == '--update-course':
            truncate_course()
            update_course()
            print 'ok'
        elif cmd == '-ue' or cmd == '--update-exam':
            truncate_exam()
            update_exam()
        elif cmd == '-h' or cmd == '--help':
            print_help()
        else:
            print '命令行参数错误'
            print_help()
    else:
        print '命令行参数个数错误'
        print_help()

