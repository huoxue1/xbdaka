import time

from config import Config
import base64
import json


try:
    import requests
    from colorama import init
    from requests.packages import urllib3
except ImportError as e:
    print("导入三方库失败 ==>"+e.msg)
    print("请尝试使用pip安装后执行")
    exit(3)

urllib3.disable_warnings()
headers = {
    'user-agent': 'PCAM10(Android/10) (uni.UNIA68F45B/2.1.3) Weex/0.26.0 1080x2264',
    'Host': 'xiaobei.yinghuaonline.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}


def login(client1: requests.Session, user_name: str, password: str) -> str:
    # 获取验证码
    cap = client1.get("https://xiaobei.yinghuaonline.com/xiaobei-api/captchaImage", headers=headers).json()
    # print(cap)
    # 登录小北学生，获取token
    login_resp = client1.post("https://xiaobei.yinghuaonline.com/xiaobei-api/login", headers=headers,
                              json={"username": user_name,
                                    "password": base64.encodebytes(password.encode(encoding='utf-8')).decode(),
                                    "code": cap.get("showCode"),
                                    "uuid": cap.get("uuid")}).json()
    headers["Authorization"] = "Bearer " + login_resp.get("token")
    return "Bearer " + login_resp.get("token")


def get_info(client1: requests.Session, token: str):
    headers["Authorization"] = token
    # 获取用户登录信息
    info = client1.get("https://xiaobei.yinghuaonline.com/xiaobei-api/getInfo", headers=headers).json()
    # print(json.dumps(info, indent=4, sort_keys=True))


def healthy(client1: requests.Session, local: str, token: str) -> str:
    headers["Authorization"] = token
    client1.get("https://xiaobei.yinghuaonline.com/xiaobei-api/student/health/checkHealth", headers=headers).json()
    location = client1.get("https://xiaobei.yinghuaonline.com/xiaobei-api/student/healthLocation",
                           headers=headers).json()

    # 提交打卡信息，返回内容 {"code":200,"msg":"操作成功"}为打卡成功
    data = client1.post("https://xiaobei.yinghuaonline.com/xiaobei-api/student/health", headers=headers, json={
        "temperature": "36.8", "coordinates": location.get("data").get("coordinates"),
        "location": local, "healthState": "1",
        "dangerousRegion": "2", "dangerousRegionRemark": "", "contactSituation": "2", "goOut": "1", "goOutRemark": "",
        "remark": "", "familySituation": "1"}).json()
    return data.get('msg')


class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def pushplus_bot(title: str, content: str) -> None:
    """
    通过 push+ 推送消息。
    """
    if Config.PUSH_PLUS_TOKEN == "":
        print("PUSHPLUS 服务的 PUSH_PLUS_TOKEN 未设置!!\n取消推送")
        return
    print("PUSHPLUS 服务启动")

    url = "http://www.pushplus.plus/send"
    data = {
        "token": Config.PUSH_PLUS_TOKEN,
        "title": title,
        "content": content
    }
    body = json.dumps(data).encode(encoding="utf-8")
    response = requests.post(url=url, data=body, headers={"Content-Type": "application/json"}).json()

    if response["code"] == 200:
        print("PUSHPLUS 推送成功！")

    else:

        url_old = "http://pushplus.hxtrip.com/send"
        headers["Accept"] = "application/json"
        response = requests.post(url=url_old, data=body, headers=headers).json()

        if response["code"] == 200:
            print("PUSHPLUS(hxtrip) 推送成功！")

        else:
            print("PUSHPLUS 推送失败！")


def main():
    msgs = []
    for student in Config.datas:
        print("开始打卡" + student.name)
        client = requests.Session()
        t = login(client, student.account, student.password)
        if t == "Bearer ":
            msgs.append(f"{student.name}打卡失败 ==》 账号或者密码错误")
            print(f"{student.name}打卡失败 ==》 账号或者密码错误")
            continue
        get_info(client1=client, token=t)
        data = healthy(client1=client, local=student.location, token=t)
        if data != "操作成功":
            msgs.append(f"{student.name}打卡失败 ==> {data}")
            print(f"{student.name}打卡失败 ==> {data}")
        else:
            msgs.append(f"{student.name}打卡失败 ==> {data}")
            print(f"{student.name}打卡成功")
    pushplus_bot("小北打卡", "\n".join(msgs))


if __name__ == '__main__':
    init(autoreset=True)
    print('*' * 20)
    print(Bcolors.OKBLUE + "该脚本仅用于成都文理学院自动打卡，不做任何盈利行为")
    print('*' * 20)
    # if len(sys.argv) > 1:
    main()
    # else:
    #     scheduler = BlockingScheduler()
    #     scheduler.add_job(main, "cron", hour=Config.HOUR, minute=Config.MINUTE, timezone="Asia/Shanghai")
    #     scheduler.start()
