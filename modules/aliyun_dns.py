#!/usr/bin/env python
# coding=utf-8

# https://next.api.aliyun.com/api-tools/sdk/Alidns?version=2015-01-09&language=python-tea

from alibabacloud_tea_util import models as UtilModels
from alibabacloud_tea_util.client import Client as UtilClient
from alibabacloud_tea_openapi import models as OpenApiModels
from alibabacloud_alidns20150109 import models as AlidnsModels
from alibabacloud_alidns20150109.client import Client as AlidnsClient

class AliDNSError(Exception):
    pass

class AliDNS:
    def __init__(self, AccessKeyID, AccessSecret, EndPoint, DomainName,RecordKeyword, RecordType, RecordValue):
        """
        Args:
            AccessKeyID='' # Your Access Secret
            AccessSecret='' # Your Access Key ID
            EndPoint='' # https://next.api.aliyun.com/product/Alidns
        """
        self.access_key_id = AccessKeyID
        self.access_key_secret = AccessSecret
        self.endpoint = EndPoint
        self.domain_name = DomainName
        self.record_keyword = RecordKeyword
        self.record_type = RecordType
        self.record_value = RecordValue

    def create_client(self) -> AlidnsClient:
        authentication = OpenApiModels.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )
        authentication.endpoint = self.endpoint
        return AlidnsClient(authentication)

    def get_records(self,DomainName):
        client = self.create_client()
        request = AlidnsModels.DescribeDomainRecordsRequest(domain_name=DomainName)
        runtime = UtilModels.RuntimeOptions()
        try:
            response = client.describe_domain_records_with_options(request, runtime)
            response_body = response.to_map().get("body")
            if response_body.get("TotalCount", 0) > 0:
                records = response_body.get("DomainRecords", {}).get("Record", [])
                return records
            else:
                error_message = f"获取{DomainName}解析记录成功，但是未查询到任何解析记录,结果为空"
                print(error_message)
                raise AliDNSError(error_message)
        except Exception as e:
            raise AliDNSError(f"获取解析记录异常: {e}")

    def add_record(self, DomainName, RecordKeyword, RecordType, RecordValue):
        client = self.create_client()
        request = AlidnsModels.AddDomainRecordRequest(
            domain_name=DomainName,
            rr=RecordKeyword,
            type=RecordType,
            value=RecordValue
        )
        runtime = UtilModels.RuntimeOptions()
        try:
            client.add_domain_record_with_options(request, runtime)
        except Exception as e:
            raise AliDNSError(f"添加解析记录异常: {e}")

    def update_record(self, RecordID, RecordKeyword, RecordType, RecordValue):
        client = self.create_client()
        request = AlidnsModels.UpdateDomainRecordRequest(
            record_id=RecordID,
            rr=RecordKeyword,
            type=RecordType,
            value=RecordValue
        )
        runtime = UtilModels.RuntimeOptions()
        try:
            client.update_domain_record_with_options(request, runtime)
        except Exception as e:
            raise AliDNSError(f"更新解析记录异常: {e}")

    def dynamic_update(self):
        domain_name = self.domain_name
        record_keyword = self.record_keyword
        record_type = self.record_type
        record_value = self.record_value

        records_response = self.get_records(DomainName=domain_name)

        for record in records_response:
            if record.get("RR") == record_keyword:
                record_id = record.get("RecordId")
                record_type_results = record.get("Type")
                record_value_results = record.get("Value")
                break
        else:
            self.add_record(DomainName=domain_name, RecordKeyword=record_keyword, RecordType=record_type,
                                        RecordValue=record_value)
            print(f"已使用配置文件内容为 {record_keyword}.{domain_name} 添加 {record_type} 记录,记录值为 {record_value}")

        if record_type_results != record_type:
            print(f"解析记录类型不匹配,配置文件内记录类型为 {record_type}, 获取到记录类型为 {record_value_results}")
            return


        if record_value_results != record_value:
            self.update_record(RecordID=record_id, RecordKeyword=record_keyword, RecordType=record_type, RecordValue=record_value)
            print(f"{record_keyword}.{domain_name} 的 {record_type} 记录已更新为 {record_value}, 原记录为 {record_value_results}")
        else:
            print(f"{record_keyword}.{domain_name} 的 {record_type} 记录 {record_value} 本地公网IP一致,暂不需要更新")
