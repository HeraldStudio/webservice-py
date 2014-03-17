# encoding: UTF-8

from django.db import models

class CourseInfo(models.Model):
    beginWeekNum = models.IntegerField() # 开始上课的周
    endWeekNum = models.IntegerField() # 结束上课的周
    classWeek = models.IntegerField() # 周几上课
    classBeginTime = models.IntegerField() # 第几节开始上课
    classEndTime = models.IntegerField() # 第几节下课
    classPlace = models.CharField(max_length = 255) # 上课地点
    classType = models.IntegerField() # 课程类型（1-单周，-1-双周，0-全部）
    term = models.CharField(max_length = 45) # 上课学期
    courseName = models.CharField(max_length = 255) # 课程名
    teacher = models.CharField(max_length = 255) # 老师名

    class Meta:
        db_table = 'course'

    def __unicode__(self):
        return self.id