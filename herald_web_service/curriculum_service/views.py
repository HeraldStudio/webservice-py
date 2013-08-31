# -*- coding: utf-8 -*-

from django.http import HttpResponse
from bs4 import BeautifulSoup
import urllib
import json
import re


def parserHtml(request, cardNumber, academicYear):
    params = urllib.urlencode(
        {'queryStudentId': cardNumber, 'queryAcademicYear': academicYear})
    uFile = urllib.urlopen(
        "http://xk.urp.seu.edu.cn/jw_service/service/stuCurriculum.action", params)
    html = uFile.read()

    pat = re.compile(ur'没有找到该学生信息', re.U)
    match = pat.search(html.decode('utf-8'))
    if match:
        return HttpResponse('没有找到该学生信息')
    else:
        soup = BeautifulSoup(html)
        sidebarCourses = soup.find_all('td', height='34', width='35%')[:-1]
        sidebarCourseList = [
            sidebarCourse for sidebarCourse in sidebarCourses if sidebarCourse.string != u'\xa0']
        lecturerList = [
            i.next_sibling.next_sibling.string for i in sidebarCourseList]
        creditList = [
            i.next_sibling.next_sibling.next_sibling.next_sibling.string for i in sidebarCourseList]
        weekList = [
            i.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.string for i in sidebarCourseList]
        sidebarList = []
        for i in xrange(len(sidebarCourseList)):
            sidebarList.append(
                [sidebarCourseList[i].string, lecturerList[i], creditList[i], weekList[i]])
        table = soup.find_all('td', rowspan='5')
        br = BeautifulSoup('<br/>')

        morningCourseList = []
        for i in xrange(1, 6):
            morningCourse = []
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    morningCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
            morningCourseList.append(morningCourse)

        afternoonCourseList = []
        for i in xrange(7, 12):
            afternoonCourse = []
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    afternoonCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
            afternoonCourseList.append(afternoonCourse)

        table = soup.find_all('td', rowspan='2')

        eveningCourseList = []
        for i in xrange(1, 6):
            eveningCourse = []
            temp = []
            for j in [k for k in xrange(len(table[i].contents[:-1])) if not (k % 2)]:
                if not j % 3:
                    temp = []
                    eveningCourse.append(temp)
                if table[i].contents[j] != br.br:
                    temp.append(table[i].contents[j])
            eveningCourseList.append(eveningCourse)

        courseList = [
            morningCourseList, afternoonCourseList, eveningCourseList]

        for i in courseList:
            for j in i:
                for k in j:
                    k.insert(1, k[1].split(']')[0][1:-1])
                    k[2] = k[2].split(']')[1][:-1]

        saturdayCourse = []
        print saturdayCourse
        for i in [j for j in xrange(len(table[7].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                print i
                temp = []
                saturdayCourse.append(temp)
            if table[7].contents[i] != br.br:
                temp.append(table[7].contents[i])
        for i in saturdayCourse:
            i.insert(1, i[1].split(']')[0][1:-1])
            i[2] = i[2].split(']')[1][:-1]
        sundayCourse = []
        print sundayCourse
        for i in [j for j in xrange(len(table[9].contents[:-1])) if not (j % 2)]:
            if not i % 3:
                print i
                temp = []
                sundayCourse.append(temp)
            if table[9].contents[i] != br.br:
                temp.append(table[9].contents[i])
        for i in sundayCourse:
            i.insert(1, i[1].split(']')[0][1:-1])
            i[2] = i[2].split(']')[1][:-1]

        courseList.append(saturdayCourse)
        courseList.append(sundayCourse)
        return HttpResponse(json.dumps([sidebarList, courseList], ensure_ascii=False), mimetype='application/json')
