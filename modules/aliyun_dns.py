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

    def __init__(self, AccessKeyID, AccessSecret, EndPoint):
        """
        Args:
            AccessKeyID='' # 阿里云用户AccessKey ID
            AccessSecret='' # 阿里云用户AccessKey Secret
            EndPoint='' # https://next.api.aliyun.com/product/Alidns
        """
        self.access_key_id = AccessKeyID
        self.access_key_secret = AccessSecret
        self.endpoint = EndPoint

    def create_client(self) -> AlidnsClient:
        authentication = OpenApiModels.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )
        authentication.endpoint = self.endpoint
        return AlidnsClient(authentication)

    def get_records(self, DomainName):
        """
        Args:
            DomainName='' # 主域名
        """
        client = self.create_client()
        request = AlidnsModels.DescribeDomainRecordsRequest(
            domain_name=DomainName)
        runtime = UtilModels.RuntimeOptions()
        try:
            response = client.describe_domain_records_with_options(
                request, runtime)
            results = response.to_map().get("body")
            if results.get("TotalCount", 0) > 0:
                records = results.get("DomainRecords", {}).get("Record", [])
                return records
            else:
                return None
        except Exception as e:
            raise AliDNSError(f"获取解析记录异常: {e}")

    def add_record(self, DomainName, RecordKeyword, RecordType, RecordValue):
        """
        Args:
            DomainName= '',# 域名
            RecordKeyword= '',# 主机记录
            RecordType= '',# 记录类型
            RecordValue= '',# 记录值
        """
        client = self.create_client()
        request = AlidnsModels.AddDomainRecordRequest(
            domain_name=DomainName,
            rr=RecordKeyword,
            type=RecordType,
            value=RecordValue
        )
        runtime = UtilModels.RuntimeOptions()
        try:
            response = client.add_domain_record_with_options(request, runtime)
            results = response.to_map().get("body")
            new_record_id = results.get("RecordId")
            get_record_info = self.record_info(RecordID=new_record_id)
            return get_record_info
        except Exception as e:
            raise AliDNSError(f"添加解析记录异常: {e}")

    def update_record(self, RecordID, RecordKeyword, RecordType, RecordValue):
        """
        Args:
            RecordID = '',# 记录ID
            DomainName = '',# 域名
            RecordKeyword = '',# 主机记录
            RecordType = '',# 记录类型
            RecordValue = '',# 记录值
        """
        client = self.create_client()
        request = AlidnsModels.UpdateDomainRecordRequest(
            record_id=RecordID,
            rr=RecordKeyword,
            type=RecordType,
            value=RecordValue
        )
        runtime = UtilModels.RuntimeOptions()
        try:
            response = client.update_domain_record_with_options(
                request, runtime)
            results = response.to_map().get("body")
            return results
        except Exception as e:
            raise AliDNSError(f"更新解析记录异常: {e}")

    def record_info(self, RecordID):
        """
        Args:
            RecordID = '',# 记录ID
        """
        client = self.create_client()
        request = AlidnsModels.DescribeDomainRecordInfoRequest(
            record_id=RecordID)
        runtime = UtilModels.RuntimeOptions()
        try:
            response = client.describe_domain_record_info_with_options(
                request, runtime)
            results = response.to_map().get("body")
            return results
        except Exception as e:
            raise AliDNSError(f"获取解析记录详细异常: {e}")
