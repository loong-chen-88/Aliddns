#!/usr/bin/env python
# coding=utf-8

import json
from datetime import datetime
from requests import get
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.AddDomainRecordRequest import AddDomainRecordRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest

# 配置accessKeyId & accessSecret & RegionID
AccessKeyID = "accessKeyId"
AccessSecret = "accessSecret"
RegionID = "cn-shenzhen"

# 配置主域名
MainDomain = "example.com"

# 配置子域名
SubDomains = "@"

# 创建AcsClient实例
client = AcsClient(AccessKeyID, AccessSecret, RegionID)

# 获取当前时间
current_time = datetime.now().isoformat(timespec='seconds')


# 获取本地公网IP
def LocalIP():
    request = get("https://api-ipv4.ip.sb/jsonip")
    response = request.json().get("ip") if request.ok else print(
        f"{current_time} Getting failed: {request.text}")
    return response


# 获取解析记录列表
def RecordList(DomainName):
    request = DescribeDomainRecordsRequest()
    request.set_accept_format("json")
    request.set_DomainName(DomainName)
    response = client.do_action_with_exception(request)
    records = json.loads(response)
    return records


# 添加解析记录
def AddRecords(DomainName, ResolutionRecord, RecordType, RecordValue):
    request = AddDomainRecordRequest()
    request.set_accept_format('json')
    request.set_DomainName(DomainName)
    request.set_RR(ResolutionRecord)
    request.set_Type(RecordType)
    request.set_Value(RecordValue)
    response = client.do_action_with_exception(request)
    records = json.loads(response)
    print(records)


# 修改解析记录
def UpdateRecords(RecordID, ResolutionRecord, RecordType, RecordValue):
    request = UpdateDomainRecordRequest()
    request.set_accept_format('json')
    request.set_RecordId(RecordID)
    request.set_RR(ResolutionRecord)
    request.set_Type(RecordType)
    request.set_Value(RecordValue)
    response = client.do_action_with_exception(request)
    records = json.loads(response)
    print(records)


if __name__ == "__main__":
    records = RecordList(MainDomain)
    local_ip = LocalIP()
    record_type = "A"
    if records.get("TotalCount") == 0:
        for subdomain in SubDomains:
            AddRecords(MainDomain, subdomain, record_type, local_ip)
            print(
                f"{current_time} Add resolution record. {record_type} record {subdomain} Default {local_ip}")
    elif records.get("TotalCount") == 1:
        subdomain_record = records["DomainRecords"]["Record"][0]
        resolution_record = subdomain_record.get("RR")
        record_id = subdomain_record.get("RecordId")
        remote_ip = subdomain_record.get("Value")

        if remote_ip == local_ip:
            print(
                f"{current_time} The DNS record already exists！the current resolution record {remote_ip} is the same as the local public network IP")
        else:
            UpdateRecords(record_id, resolution_record, record_type, local_ip)
            print(
                f"{current_time} Modify resolution record. {record_type} record {resolution_record} Default {remote_ip} changed to {record_type} record {resolution_record} Default {local_ip}")
