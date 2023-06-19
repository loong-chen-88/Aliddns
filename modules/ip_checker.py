#!/usr/bin/env python
# coding=utf-8

import requests
import ipaddress


class GetIPError(Exception):
    pass


class PublicIP:
    def __init__(self):
        pass

    @staticmethod
    def get(RecordType: str = "A") -> str:
        """
        Args:
            获取IPv4地址, RecordType="A"
            获取IPv6地址, RecordType="AAAA"
        """
        try:
            if RecordType == "A":
                return PublicIP.v4()
            elif RecordType == "AAAA":
                return PublicIP.v6()
            else:
                error_message = f"获取IP地址参数不能是'{RecordType}',修改配置文件后再运行"
                raise GetIPError(error_message)
        except Exception as e:
            raise GetIPError(str(e))

    @staticmethod
    def v4() -> str:
        try:
            response = requests.get('https://api.ipify.org')
            if response.status_code != 200:
                raise GetIPError(f"获取IP地址API 响应错误,错误代码:{response.status_code}")

            results = response.text
            if not ipaddress.ip_address(results):
                raise GetIPError(f"获取IP地址成功,但获取结果 {results} 不是有效的 IP 地址")

            public_ip = results
            if ipaddress.ip_address(results).version != 4:
                raise GetIPError(f"获取IP地址成功,但{public_ip}不能用于'A'记录")

            return public_ip

        except Exception as e:
            raise GetIPError(f'获取IP地址异常:{str(e)}')

    @staticmethod
    def v6() -> str:
        try:
            response = requests.get('https://api64.ipify.org')
            if response.status_code != 200:
                raise GetIPError(f"获取IP地址API 响应错误,错误代码:{response.status_code}")

            results = response.text
            if not ipaddress.ip_address(results):
                raise GetIPError(f"获取IP地址成功,但获取结果 {results} 不是有效的 IP 地址")

            public_ip = results
            if ipaddress.ip_address(results).version != 6:
                raise GetIPError(f"获取IP地址成功,但{results}不能用于'AAAA'记录")

            return public_ip

        except Exception as e:
            raise GetIPError(f'获取IP地址异常:{str(e)}')
