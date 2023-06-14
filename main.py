from modules.ip_checker import PublicIP
from modules.aliyun_dns import AliDNS
from modules.config_manager import ConfigManager


def main():
    config = ConfigManager()

    ali_key_id = config.get("AccessKeyID")
    ali_secret = config.get("AccessSecret")
    ali_region = config.get("RegionEndpoint")
    domain_name = config.get("DomainName")
    record_keyword = config.get("RecordKeyword")
    record_type = config.get("RecordType")
    record_value = PublicIP.get(record_type)

    ali_dns_client = AliDNS(AccessKeyID=ali_key_id, AccessSecret=ali_secret, EndPoint=ali_region, DomainName=domain_name, RecordKeyword=record_keyword, RecordType=record_type, RecordValue=record_value)
    ali_dns_client.dynamic_update()

if __name__ == "__main__":
    main()
