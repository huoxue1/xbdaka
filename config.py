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
            name="苟江山",
            # 用户小北学生账号
            account="15082717021",
            # 用户小北学生密码
            password="164652",
            # 用户打卡地点
            location="四川省-成都市-金堂县"
        )
    ]
    # 微信推送的token，可前往pushplus官网获取 https://www.pushplus.plus/push1.html
    PUSH_PLUS_TOKEN = "7424a35e9af748608ae7d81b62481a8e"

    # 打卡时间，默认7点过2分
    HOUR = 7
    MINUTE = 2
