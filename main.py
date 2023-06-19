from modules.aliyun_dns import AliDNS
from modules.log_manager import Logger
from modules.ip_checker import PublicIP
from modules.config_manager import ConfigManager


def main():
    try:
        logger = Logger()
        config = ConfigManager()
        ali_key_id = config.get("AccessKeyID")
        ali_secret = config.get("AccessSecret")
        ali_region = config.get("RegionEndpoint")
        domain_name = config.get("DomainName")
        record_keyword = config.get("RecordKeyword")
        record_type = config.get("RecordType")

        record_value = PublicIP.get(record_type)

        ali_dns_client = AliDNS(AccessKeyID=ali_key_id,
                                AccessSecret=ali_secret, EndPoint=ali_region)

        records = ali_dns_client.get_records(DomainName=domain_name)
        if records is not None:
            record_type_results = None
            record_value_results = None
            record_id = None

            for record in records:
                if record.get("RR") == record_keyword:
                    record_id = record.get("RecordId")
                    record_type_results = record.get("Type")
                    record_value_results = record.get("Value")
                    break

            if record_type_results != record_type:
                match_type_message = f"解析记录类型不匹配,配置文件内记录类型为 {record_type} ,获取到记录类型为 {record_value_results}"
                logger.log_error(match_type_message)
                return

            if record_value_results != record_value:
                ali_dns_client.update_record(
                    RecordID=record_id, RecordKeyword=record_keyword, RecordType=record_type, RecordValue=record_value)
                update_record_message = f"{record_keyword}.{domain_name} 的 {record_type} 记录已更新为 {record_value},原记录为 {record_value_results}"
                logger.log_info(update_record_message)
            else:
                match_value_message = f"{record_keyword}.{domain_name} 的 {record_type} 记录 {record_value} 本地公网IP一致,暂不需要更新"
                logger.log_warning(match_value_message)
        else:
            add_record_results = ali_dns_client.add_record(
                DomainName=domain_name, RecordKeyword=record_keyword, RecordType=record_type, RecordValue=record_value)
            add_record_message = f"'{record_keyword}.{domain_name}' 的 {record_type} 记录为空,已根据配置文件添加:\n{add_record_results}"
            logger.log_warning(add_record_message)
    except Exception as e:
        print(e)
        logger.log_error(e)


if __name__ == "__main__":
    main()
