from dataclasses import dataclass


@dataclass(init=True)
class Student:
    name: str
    account: str
    password: str
    location: str


@dataclass()
class Config:
    # 打卡信息，可配置多个
    datas = [
        Student(
            # 打卡用户姓名
            name="",
            # 用户小北学生账号
            account="",
            # 用户小北学生密码
            password="",
            # 用户打卡地点
            location=""
        )
    ]
    # 微信推送的token，可前往pushplus官网获取 https://www.pushplus.plus/push1.html
    PUSH_PLUS_TOKEN = ""

    # 打卡时间，默认7点过2分
    HOUR = 7
    MINUTE = 2
