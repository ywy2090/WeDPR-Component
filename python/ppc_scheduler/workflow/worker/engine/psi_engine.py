# -*- coding: utf-8 -*-
import codecs
import os
import time

from ppc_common.ppc_utils import utils, common_func
from ppc_scheduler.workflow.common.job_context import JobContext


class PsiWorkerEngine:
    def __init__(self, psi_client, worker_type, components, job_context: JobContext):
        self.psi_client = psi_client
        self.worker_type = worker_type
        self.components = components
        self.job_context = job_context
        self.log = self.components.logger()

    def run(self) -> list:
        job_id = self.job_context.job_id
        start_time = time.time()
        self.origin_dataset_to_psi_inputs()

        self.log.info(f"compute two party psi, job_id={job_id}")
        if len(self.job_context.participant_id_list) == 2:
            self._run_two_party_psi()
        else:
            self._run_multi_party_psi()
        time_costs = time.time() - start_time
        self.log.info(f"computing psi finished, job_id={job_id}, timecost: {time_costs}s")
        return [JobContext.HDFS_STORAGE_PATH + job_id + os.sep + self.job_context.PSI_RESULT_INDEX_FILE]

    def _run_two_party_psi(self):
        job_id = self.job_context.job_id
        agency_id = self.components.config_data['AGENCY_ID']
        job_info = {
            "taskID": job_id,
            "type": 0,
            "algorithm": 0,
            "syncResult": True,
            "lowBandwidth": False,
            "parties": [
                {
                    "id": self.job_context.participant_id_list[1 - self.job_context.my_index],
                    "partyIndex": 1 - self.job_context.my_index
                },
                {
                    "id": agency_id,
                    "partyIndex": self.job_context.my_index,
                    "data":
                        {
                            "id": self.job_context.job_id,
                            "input": {
                                "type": 2,
                                "path": self.job_context.HDFS_STORAGE_PATH + job_id + os.sep + JobContext.PSI_PREPARE_FILE
                            },
                            "output": {
                                "type": 2,
                                "path": self.job_context.HDFS_STORAGE_PATH + job_id + os.sep + JobContext.PSI_RESULT_FILE
                            }
                        }
                }
            ]
        }
        psi_result = self.psi_client.run(job_info, self.components.config_data['PPCS_RPC_TOKEN'])
        self.log.info(f"call psi service successfully, job_id={job_id}, result: {psi_result}")

    def _run_multi_party_psi(self):
        job_id = self.job_context.job_id
        participant_number = len(self.job_context.participant_id_list)
        participant_list = []
        # parties_index = [0, 1 ··· 1, 2]
        parties_index = participant_number * [1]  # role: partner
        parties_index[0] = 0  # role: calculator
        parties_index[-1] = 2  # role: master
        for index, agency_id in enumerate(self.job_context.participant_id_list):
            party_map = {}
            if self.job_context.my_index == index:
                party_map["id"] = agency_id
                party_map["partyIndex"] = parties_index[index]
                party_map["data"] = {
                    "id": self.job_context.job_id,
                    "input": {
                        "type": 2,
                        "path": self.job_context.HDFS_STORAGE_PATH + job_id + os.sep + JobContext.PSI_PREPARE_FILE
                    },
                    "output": {
                        "type": 2,
                        "path": self.job_context.HDFS_STORAGE_PATH + job_id + os.sep + JobContext.PSI_RESULT_FILE
                    }
                }
            else:
                party_map["id"] = agency_id
                party_map["partyIndex"] = parties_index[index]
            participant_list.append(party_map)

        job_info = {
            "taskID": job_id,
            "type": 0,
            "algorithm": 4,
            "syncResult": True,
            "receiverList": self.job_context.result_receiver_list,
            "parties": participant_list
        }
        psi_result = self.psi_client.run(job_info, self.components.config_data['PPCS_RPC_TOKEN'])
        self.log.info(f"call psi service successfully, job_id={job_id}, result: {psi_result}")

    def origin_dataset_to_psi_inputs(self):
        # TODO: 下载数据
        # dataset_helper_factory.download_dataset(
        #     dataset_helper_factory=None,
        #     dataset_user=self.job_context.user_name,
        #     dataset_id=self.job_context.dataset_id,
        #     dataset_local_path=self.job_context.dataset_file_path,
        #     log_keyword="prepare_dataset",
        #     logger=self.log)

        field = (self.job_context.psi_fields.split(utils.CSV_SEP)[self.job_context.my_index]).lower()
        if field == '':
            field = 'id'
        prepare_file = open(self.job_context.psi_prepare_path, 'w')
        psi_split_reg = "==="
        file_encoding = common_func.get_file_encoding(self.job_context.dataset_file_path)
        if psi_split_reg in field:
            field_multi = field.split(psi_split_reg)
            with codecs.open(self.job_context.dataset_file_path, "r", file_encoding) as dataset:
                fields = next(dataset).lower()
                fields_list = fields.strip().split(utils.CSV_SEP)
                id_idx_list = []
                for filed_idx in field_multi:
                    id_idx_list.append(fields_list.index(filed_idx))
                for line in dataset:
                    if line.strip() == "":
                        continue
                    final_str = ""
                    for id_idx_multi in id_idx_list:
                        if len(line.strip().split(utils.CSV_SEP, id_idx_multi + 1)) < id_idx_multi + 1:
                            continue
                        final_str = "{}-{}".format(final_str, line.strip().split(
                            utils.CSV_SEP, id_idx_multi + 1)[id_idx_multi]).strip("\r\n")
                    print(final_str, file=prepare_file)
            prepare_file.close()
        else:
            with codecs.open(self.job_context.dataset_file_path, "r", file_encoding) as dataset:
                # ignore lower/upper case
                fields = next(dataset).lower()
                fields_list = fields.strip().split(utils.CSV_SEP)
                id_idx = fields_list.index(field)
                for line in dataset:
                    if line.strip() == "":
                        continue
                    if len(line.strip().split(utils.CSV_SEP, id_idx + 1)) < id_idx + 1:
                        continue
                    print(line.strip().split(utils.CSV_SEP, id_idx + 1)
                          [id_idx], file=prepare_file)
            prepare_file.close()
        self.components.storage_client.upload_file(self.job_context.psi_prepare_path,
                                                   self.job_context.job_id + os.sep + JobContext.PSI_PREPARE_FILE)
        utils.delete_file(self.job_context.psi_prepare_path)
