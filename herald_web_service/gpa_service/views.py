import recognize
import urllib2,urllib
import io
import Image
import cookielib
import BeautifulSoup
import json

VERCODE_URL = r"http://xk.urp.seu.edu.cn/studentService/getCheckCode" #验证码地址

LOGIN_URL = r"http://xk.urp.seu.edu.cn/studentService/system/login.action" #登陆地址

INFO_URL = r"http://xk.urp.seu.edu.cn/studentService/cs/stuServe/studentExamResultQuery.action" #信息的地址

def gpa(request):
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    data = io.BytesIO(urllib2.urlopen(VERCODE_URL).read())
    im = Image.open(data)
    vercode = recognize.solve(im)
    data = {
        'userName':request.POST['username'],
        'password':request.POST['password'],
        'vercode':vercode
    }
    # print ans
    req = urllib2.Request(LOGIN_URL,urllib.urlencode(data))
    res_len = urllib2.urlopen(req,timeout = 60).info().get('Content-Length')
    # print res_len
    if res_len!= str(770):
        return HttpResponse("userName or password error")
    else:
        res = urllib2.urlopen(INFO_URL).read()
        soup = BeautifulSoup.BeautifulSoup(res)
        trs = soup.findAll('tr')
        ans = []
        for i in range(2,len(trs)-4):#only process useful info
            tds = trs[i].findAll('td')
            tmp = {'semester':tds[1].string,'name':tds[3].string,'credit':tds[4].string,'score':tds[5].string,'score_type':tds[6].string,'extra':tds[7].string}
            ans.append(tmp)
        return(json.dumps(ans).replace('&nbsp;',''))