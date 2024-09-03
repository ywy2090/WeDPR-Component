# -*- coding: utf-8 -*-
import os

import pandas as pd

from ppc_common.ppc_utils import utils
from ppc_scheduler.mpc_generator.generator import CodeGenerator
from ppc_scheduler.workflow.common.job_context import JobContext


class MpcWorkerEngine:
    def __init__(self, mpc_client, worker_type, components, job_context: JobContext):
        self.mpc_client = mpc_client
        self.worker_type = worker_type
        self.components = components
        self.job_context = job_context
        self.log = self.components.logger()

    def run(self) -> list:
        bit_length = self._prepare_mpc_file()
        if self.job_context.need_run_psi:
            self._prepare_mpc_after_psi()
        else:
            self._prepare_mpc_without_psi()
        self._run_mpc_job(bit_length)
        self._finish_mpc_job()
        return [self.job_context.mpc_output_path]

    def _prepare_mpc_file(self):
        # if self.job_context.sql is not None:
        #     # compile sql to mpc content
        #     mpc_content = CodeGenerator(self.job_context.sql)
        # else:
        #     mpc_content = self.job_context.mpc_content
        utils.write_content_to_file(self.job_context.mpc_content, self.job_context.mpc_file_path)

        self.components.storage_client.upload_file(self.job_context.mpc_file_path,
                                                   self.job_context.job_id + os.sep + self.job_context.mpc_file_name)
        return self._get_share_bytes_length(self.job_context.mpc_content)

    def _run_mpc_job(self, bit_length):
        job_id = self.job_context.job_id
        mpc_record = 0
        self.log.info(f"start compute_mpc_job, job id: {job_id}")
        if self.job_context.mpc_prepare_path:
            mpc_record = sum(1 for _ in open(self.job_context.mpc_prepare_path))
            self.log.info(f"compute_mpc_job, mpc record: {mpc_record}")
        utils.replace(self.job_context.mpc_file_path, mpc_record)
        self._replace_mpc_field_holder()
        self.components.storage_client.upload_file(self.job_context.mpc_file_path,
                                                   job_id + os.sep + self.job_context.mpc_file_name)
        job_info = {
            "jobId": job_id,
            "mpcNodeUseGateway": False,
            "receiverNodeIp": "",
            "mpcNodeDirectPort": self.components.config_data["MPC_NODE_DIRECT_PORT"],
            "participantCount": len(self.job_context.participant_id_list),
            "selfIndex": self.job_context.my_index,
            "isMalicious": self.components.config_data["IS_MALICIOUS"],
            "bitLength": bit_length,
            "inputFileName": "{}-P{}-0".format(JobContext.MPC_PREPARE_FILE, self.job_context.my_index),
            "outputFileName": JobContext.MPC_OUTPUT_FILE
        }

        self.log.info(f"call compute_mpc_job service, model run, params: {job_info}")
        self.mpc_client.run(job_info, self.components.config_data['PPCS_RPC_TOKEN'])
        self.components.storage_client.download_file(job_id + os.sep + JobContext.MPC_OUTPUT_FILE,
                                                     self.job_context.mpc_output_path)
        self.log.info(f"call compute_mpc_job service success")

    def _finish_mpc_job(self):
        job_id = self.job_context.job_id
        index_file = None
        if self.components.config_data['AGENCY_ID'] in self.job_context.result_receiver_list:
            if self.job_context.need_run_psi:
                if not utils.file_exists(self.job_context.psi_result_path):
                    self.log.info(
                        f"download finish_mpc_job psi_result_path, job_id={job_id}, "
                        f"download {job_id + os.sep + JobContext.PSI_RESULT_FILE}")
                    self.components.storage_client.download_file(job_id + os.sep + JobContext.PSI_RESULT_FILE,
                                                                 self.job_context.psi_result_path)
                self._order_psi_csv()
                index_file = self.job_context.psi_result_path
            if not utils.file_exists(self.job_context.mpc_output_path):
                self.log.info(
                    f"download finish_mpc_job mpc_output_path, job_id={job_id}, "
                    f"download {job_id + os.sep + JobContext.MPC_OUTPUT_FILE}")
                self.components.storage_client.download_file(job_id + os.sep + JobContext.MPC_OUTPUT_FILE,
                                                             self.job_context.mpc_output_path)

            self.log.info(
                f"finish_mpc_job mpc_output_path, job_id={job_id}")
            self._parse_and_write_final_mpc_result(self.job_context.mpc_output_path, index_file)
            self.components.storage_client.upload_file(self.job_context.mpc_result_path,
                                                       job_id + os.sep + JobContext.MPC_RESULT_FILE)
            self.log.info(f"finish_mpc_job success, job_id={job_id}")

    def _get_share_bytes_length(self, algorithm_content):
        target = '# BIT_LENGTH = '
        if target in algorithm_content:
            start = algorithm_content.find(target)
            end = algorithm_content.find('\n', start + len(target))
            bit_length = int(algorithm_content[start + len(target): end].strip())
            self.log.info(f"OUTPUT_BIT_LENGTH = {bit_length}")
            return bit_length
        else:
            self.log.info(f"OUTPUT_BIT_LENGTH = 64")
            return 64

    def _get_dataset_column_count(self):
        with open(self.job_context.mpc_file_path, "r") as file:
            mpc_str = file.read()

        lines = mpc_str.split('\n')
        for line in lines:
            if f"source{self.job_context.my_index}_column_count =" in line or \
                    f"source{self.job_context.my_index}_column_count=" in line:
                index = line.find('=')
                return int(line[index + 1:].strip('\n').strip())

    def _make_dataset_to_mpc_data_plus_psi_data(self, my_dataset_number):
        chunk_list = pd.read_csv(self.job_context.dataset_file_path, delimiter=utils.CSV_SEP,
                                 chunksize=self.components.file_chunk_config.read_chunk_size)
        psi_data = pd.read_csv(self.job_context.psi_result_path, delimiter=utils.CSV_SEP)
        for chunk in chunk_list:
            self._make_dataset_field_normalized(chunk)
            mpc_data_df = pd.merge(chunk, psi_data, on=['id']).sort_values(
                by='id', ascending=True)
            self._save_selected_column_data(
                my_dataset_number, mpc_data_df, self.job_context.mpc_prepare_path)

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
    def _save_selected_column_data(my_dataset_number, data_df, mpc_prepare_path):
        column_list = []
        for i in range(0, int(my_dataset_number)):
            column_list.append(utils.NORMALIZED_NAMES.format(i))
        result_new = pd.DataFrame(data_df, columns=column_list)
        # sep must be space (ppc-mpc inputs)
        result_new.to_csv(mpc_prepare_path, sep=' ', mode='a', header=False, index=None)

    def _prepare_mpc_after_psi(self):
        job_id = self.job_context.job_id
        self.log.info(f"start prepare_mpc_after_psi, job_id={job_id}")
        my_dataset_number = self._get_dataset_column_count()

        # TODO: 下载数据
        # dataset_helper_factory.download_dataset(
        #     dataset_helper_factory=None,
        #     dataset_user=self.job_context.user_name,
        #     dataset_id=self.job_context.dataset_id,
        #     dataset_local_path=self.job_context.dataset_file_path,
        #     log_keyword="prepare_mpc_after_psi",
        #     logger=self.log)

        if not utils.file_exists(self.job_context.psi_result_path):
            self.log.info(
                f"prepare_mpc_after_psi, download psi_result_path ,job_id={job_id}, "
                f"download {job_id + os.sep + JobContext.PSI_RESULT_FILE}")

            self.components.storage_client.download_file(job_id + os.sep + JobContext.PSI_RESULT_FILE,
                                                         self.job_context.psi_result_path)

        self._make_dataset_to_mpc_data_plus_psi_data(my_dataset_number)

        hdfs_mpc_prepare_path = "{}-P{}-0".format(job_id + os.sep + JobContext.MPC_PREPARE_FILE,
                                                  self.job_context.my_index)
        self.components.storage_client.upload_file(self.job_context.mpc_prepare_path, hdfs_mpc_prepare_path)
        self.log.info(f"call prepare_mpc_after_psi success: job_id={job_id}")

    def _make_dataset_to_mpc_data_direct(self, my_dataset_number):
        chunk_list = pd.read_csv(self.job_context.dataset_file_path, delimiter=utils.CSV_SEP,
                                 chunksize=self.components.file_chunk_config.read_chunk_size)
        for chunk in chunk_list:
            self._make_dataset_field_normalized(chunk)
            self._save_selected_column_data(my_dataset_number, chunk, self.job_context.mpc_prepare_path)

    def _prepare_mpc_without_psi(self):
        job_id = self.job_context.job_id
        self.log.info(f"start prepare_mpc_without_psi, job_id={job_id}")
        my_dataset_number = self._get_dataset_column_count()
        # TODO: 下载数据
        # dataset_helper_factory.download_dataset(
        #     dataset_helper_factory=None,
        #     dataset_user=self.job_context.user_name,
        #     dataset_id=self.job_context.dataset_id,
        #     dataset_local_path=self.job_context.dataset_file_path,
        #     log_keyword="prepare_mpc_without_psi",
        #     logger=self.log)

        self._make_dataset_to_mpc_data_direct(my_dataset_number)

        hdfs_mpc_prepare_path = "{}-P{}-0".format(job_id + os.sep + JobContext.MPC_PREPARE_FILE,
                                                  self.job_context.my_index)
        self.components.storage_client.upload_file(self.job_context.mpc_prepare_path, hdfs_mpc_prepare_path)
        self.log.info(f"call prepare_mpc_without_psi success: job_id={job_id}")

    def _order_psi_csv(self):
        """
        order_psi_csv
        """
        data = pd.read_csv(self.job_context.psi_result_path, delimiter=utils.CSV_SEP)
        data.sort_values(by="id").to_csv(self.job_context.psi_result_path,
                                         sep=utils.CSV_SEP, header=True, index=None)

    def _parse_and_write_final_mpc_result(self, mpc_output_path, index_file):
        self.log.info("run parse_and_write_final_mpc_result")
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

        id_list = []
        if self.job_context.need_run_psi:
            df = pd.read_csv(index_file, delimiter=utils.CSV_SEP)
            for result_id in df["id"]:
                id_list.append(result_id)

        with open(self.job_context.mpc_result_path, "w", encoding='utf-8') as file:
            file.write(final_result_fields + '\n')
            row_count = 0
            for row_data in open(mpc_output_path):
                if row_data.__contains__(utils.PPC_RESULT_VALUES_FLAG):
                    values = row_data.split('=')[1].strip().split(utils.BLANK_SEP)
                    if self.job_context.need_run_psi:
                        if row_count >= len(id_list):
                            row = str(id_list[-1] + row_count - len(id_list) + 1)
                        else:
                            row = str(id_list[row_count])
                    else:
                        row = str(row_count)

                    for value in values:
                        try:
                            row += (',' + value)
                        except:
                            row += (',%s' % value)
                    file.write(row + '\n')
                    row_count += 1
            file.close()

        self.log.info("finish parse_and_write_final_mpc_result")

    def _replace_mpc_field_holder(self):
        party_count = len(self.job_context.participant_id_list)
        if self.job_context.need_run_psi:
            dataset_record_count = 0
            if self.job_context.mpc_prepare_path:
                dataset_record_count = sum(1 for _ in open(self.job_context.mpc_prepare_path))
            for i in range(party_count):
                utils.replace(self.job_context.mpc_file_path,
                              dataset_record_count, f'$(source{i}_record_count)')
        else:
            for i in range(party_count):
                utils.replace(self.job_context.mpc_file_path,
                              self.job_context.dataset_record_count, f'$(source{i}_record_count)')
