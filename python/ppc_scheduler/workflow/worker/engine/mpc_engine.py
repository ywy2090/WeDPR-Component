# -*- coding: utf-8 -*-
import json
import os
import time

import pandas as pd

from ppc_common.ppc_utils import utils
from ppc_scheduler.workflow.common.job_context import JobContext

class MpcWorkerEngine:
    def __init__(self, mpc_client, worker_type, worker_id, components, job_context: JobContext):
        self.mpc_client = mpc_client
        self.worker_type = worker_type
        self.worker_id = worker_id
        self.components = components
        self.job_context = job_context
        self.logger = self.components.logger()
        
        self.job_id = self.job_context.job_id
        
        self.mpc_prepare_record_count = 0
        self.dataset_column_number = 0
        self.share_bytes_length = 0

    def run(self, *args) -> list:
        
        start_time = time.time()
        
        self.args = json.loads(args[0])
        self.logger.info(f"## mpc engine run begin, job_id={self.job_id}, worker_id={self.worker_id}, args: {args}")
        
        self._prepare_mpc_job(self.args)
        self._run_mpc_job()
        self._finish_mpc_job()
        
        time_costs = time.time() - start_time
        self.logger.info(f"## mpc engine run finished, job_id={self.job_id}, timecost: {time_costs}s")
        
        return [self.job_context.mpc_output_path]

    def _run_mpc_job(self):
        job_id = self.job_context.job_id
        
        self.logger.info(f"start run_mpc_job, job id: {job_id}")
        
        job_info = {
            "jobId": job_id,
            "mpcNodeUseGateway": False,
            "receiverNodeIp": "",
            "mpcNodeDirectPort": self.components.config_data["MPC_NODE_DIRECT_PORT"],
            "participantCount": self.party_count,
            "selfIndex": self.self_index,
            "isMalicious": self.components.config_data["IS_MALICIOUS"],
            "bitLength": self.share_bytes_length,
            "inputFileName": "{}-P{}-0".format(JobContext.MPC_PREPARE_FILE, self.self_index),
            "outputFileName": JobContext.MPC_OUTPUT_FILE
        }

        self.logger.info(f"call run_mpc_job, job info: {job_info}")
    
        self.mpc_client.run(job_info)
        
        self.logger.info(f"call run_mpc_job success")

    def _finish_mpc_job(self):
        job_id = self.job_id
        
        self.logger.info(
            f"finish_mpc_job start, job_id={job_id}")
        
        if not self.receive_result:
            return
        
        if not utils.file_exists(self.job_context.mpc_output_path):
            self.logger.info(
                f"download finish_mpc_job, job_id={job_id}, "
                f"download {job_id + os.sep + JobContext.MPC_OUTPUT_FILE}")
            self.components.storage_client.download_file(job_id + os.sep + JobContext.MPC_OUTPUT_FILE,
                                                            self.job_context.mpc_output_path)

        
        
        self._parse_and_write_final_mpc_result(self.job_context.mpc_output_path)
        self.components.storage_client.upload_file(self.job_context.mpc_result_path,
                                                    job_id + os.sep + JobContext.MPC_RESULT_FILE)
        
        self.logger.info(f"finish_mpc_job success, job_id={job_id}")

    def _get_share_bytes_length(self, mpc_content):
        target = '# BIT_LENGTH = '
        if target in mpc_content:
            start = mpc_content.find(target)
            end = mpc_content.find('\n', start + len(target))
            bit_length = int(mpc_content[start + len(target): end].strip())
            return bit_length
        else:
            return 64

    def _get_dataset_column_count(self, mpc_content: str, my_index: int):
        lines = mpc_content.split('\n')
        for line in lines:
            if f"source{my_index}_column_count =" in line or \
                    f"source{my_index}_column_count=" in line:
                index = line.find('=')
                return int(line[index + 1:].strip('\n').strip())

    @staticmethod
    def _make_dataset_field_normalized(dataset_df):
        data_field = dataset_df.columns.values
        if 'id' in data_field:
            data_field_normalized_names = ['id']
            size = len(data_field)
            for i in range(size - 1):
                data_field_normalized_names.append(
                    utils.NORMALIZED_NAMES.format(i))
        else:
            data_field_normalized_names = []
            size = len(data_field)
            for i in range(size):
                data_field_normalized_names.append(
                    utils.NORMALIZED_NAMES.format(i))
        dataset_df.columns = data_field_normalized_names

    @staticmethod
    def _save_selected_column_data(data_df, dataset_column_number, mpc_prepare_path):
        column_list = []
        for i in range(0, int(dataset_column_number)):
            column_list.append(utils.NORMALIZED_NAMES.format(i))
        result_new = pd.DataFrame(data_df, columns=column_list)
        # sep must be space (ppc-mpc inputs)
        result_new.to_csv(mpc_prepare_path, sep=' ', mode='a', header=False, index=None)
        mpc_prepare_new_record_count = len(result_new)
        # print(" ==> mpc_prepare_new_record_count " + str(mpc_prepare_new_record_count))
        return mpc_prepare_new_record_count
        
    @staticmethod
    def _make_dataset_to_mpc_data_direct(dataset_file_path: str, mpc_prepare_path: str, dataset_column_number: int, chunksize: int = 1024 * 1024):
        
        chunk_list = pd.read_csv(dataset_file_path, delimiter=utils.CSV_SEP,
                                 chunksize=chunksize)
        mpc_prepare_record_count = 0
        for chunk in chunk_list:
            MpcWorkerEngine._make_dataset_field_normalized(chunk)
            mpc_prepare_record_count += MpcWorkerEngine._save_selected_column_data(chunk, dataset_column_number, mpc_prepare_path)
        
        return mpc_prepare_record_count

    def _prepare_mpc_job(self, args):
        job_id = self.job_id
        self.logger.info(f"start prepare_mpc_psi, job_id={job_id}")
        
        # parser parameters
        self.mpc_content = args["mpcContent"]
        self.self_index = args["selfIndex"]
        self.party_count = args["partyCount"]
        self.input_file = args["inputFilePath"]
        # self.output_file = args["outputFilePath"]
        self.receive_result = args["receiveResult"]
        self.dataset_list = args["datasetList"]
        
        # 
        self.share_bytes_length = self._get_share_bytes_length(self.mpc_content)
        self.dataset_column_number = self._get_dataset_column_count(self.mpc_content, self.self_index)
        
        try:
            # download dataset
            self.components.storage_client.download_file(
                        self.input_file, self.job_context.dataset_file_path)
            # prepare mpc 
            self.mpc_prepare_record_count = MpcWorkerEngine._make_dataset_to_mpc_data_direct(self.job_context.dataset_file_path, self.dataset_column_number, self.job_context.mpc_prepare_path)

            hdfs_mpc_prepare_path = "{}-P{}-0".format(job_id + os.sep + JobContext.MPC_PREPARE_FILE,self.self_index)
            
            self.components.storage_client.upload_file(self.job_context.mpc_prepare_path, hdfs_mpc_prepare_path)
            
            self.mpc_content = self._replace_mpc_prepare_record_count(self.mpc_content, self.mpc_prepare_record_count)
            self.mpc_content = self._replace_mpc_field_holder(self.mpc_content)
            
            self.components.storage_client.save_data(self.mpc_content,
                                                   job_id + os.sep + self.job_context.mpc_file_name)
        finally:
            if utils.file_exists(self.job_context.dataset_file_path):
                utils.delete_file(self.job_context.dataset_file_path)
            
            if utils.file_exists(self.job_context.mpc_prepare_path):
                utils.delete_file(self.job_context.mpc_prepare_path)
        
        self.logger.info(f"call prepare_mpc_psi success: job_id={job_id}")

    def _parse_and_write_final_mpc_result(self, mpc_output_path):
        self.logger.info("run parse_and_write_final_mpc_result")
        
        final_result_fields = 'id'
        need_add_fields = True
        column_count = 0
        for row_data in open(mpc_output_path):
            if row_data.__contains__(utils.PPC_RESULT_FIELDS_FLAG):
                need_add_fields = False
                final_result_fields += ',' + \
                                       row_data[row_data.find(
                                           '=') + 1:].strip().replace(utils.BLANK_SEP, utils.CSV_SEP)
            elif row_data.__contains__(utils.PPC_RESULT_VALUES_FLAG):
                column_count = len(row_data.split(
                    '=')[1].strip().split(utils.BLANK_SEP))
                break

        if need_add_fields:
            for i in range(column_count):
                final_result_fields += ',' + 'result' + str(i)

        with open(self.job_context.mpc_result_path, "w", encoding='utf-8') as file:
            file.write(final_result_fields + '\n')
            row_count = 0
            for row_data in open(mpc_output_path):
                if row_data.__contains__(utils.PPC_RESULT_VALUES_FLAG):
                    values = row_data.split('=')[1].strip().split(utils.BLANK_SEP)
                    row = str(row_count)

                    for value in values:
                        try:
                            row += (',' + value)
                        except:
                            row += (',%s' % value)
                    file.write(row + '\n')
                    row_count += 1

        self.logger.info("finish parse_and_write_final_mpc_result")
    
    def _replace_mpc_prepare_record_count(self, mpc_content, mpc_prepare_record_count):
        return mpc_content.replace(utils.MPC_RECORD_PLACE_HOLDER, str(mpc_prepare_record_count))
    
    def _replace_mpc_field_holder(self, mpc_content):
        for i in self.party_count:
            dataset_record_count = self.dataset_list[i].dataset_record_count
            mpc_content = mpc_content.replace(dataset_record_count, f'$(source{i}_record_count)')
        return mpc_content