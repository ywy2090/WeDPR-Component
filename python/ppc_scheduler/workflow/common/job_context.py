import os

from ppc_scheduler.job.job_type import JobType
from ppc_scheduler.mpc_generator.generator import CodeGenerator
from ppc_scheduler.workflow.common.default_flow_config import flow_dict
from ppc_scheduler.common.global_context import components


class JobContext:
    PSI_PREPARE_FILE = "psi_inputs"
    PSI_RESULT_INDEX_FILE = "psi_result_index"
    PSI_RESULT_FILE = "psi_result"
    MPC_PREPARE_FILE = "mpc_prepare.csv"
    MPC_RESULT_FILE = "mpc_result.csv"
    MPC_OUTPUT_FILE = "mpc_output.txt"
    HDFS_STORAGE_PATH = "/user/ppc/"

    def __init__(self, args, workspace):
        self.args = args
        #todo: 确保java服务给过来的任务信息包含如下字段，如果是建模相关的任务，还需要job_context.model_config_dict = args['model_config']
        # 如果是mpc任务，还需要有args['sql']，或者args['mpc_content']
        self.job_id: str = args['job_id']
        self.user_name: str = args['user_name']
        self.dataset_id: str = args['dataset_id']

        self.psi_fields: str = args['psi_fields']

        self.result_receiver_list: list = args['result_receiver_list']
        self.participant_id_list: list = args['participant_id_list']
        self.job_type = args['job_type']
        self.dataset_record_count = args['dataset_record_count']

        self.my_index = None
        self.need_run_psi = False
        self.need_run_fe = False
        self.mpc_content = None

        self.model_config_dict: dict = {}
        self.tag_provider_agency_id = None
        self.job_subtype = None
        self.predict_algorithm = None

        self.worker_configs: list = []
        self.workflow_view_path = 'workflow_view'

        self.workspace = workspace
        self.job_cache_dir = "{}{}{}".format(self.workspace, os.sep, self.job_id)
        self.dataset_file_path = "{}{}{}".format(self.job_cache_dir, os.sep, self.dataset_id)
        self.psi_prepare_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.PSI_PREPARE_FILE)
        self.psi_result_index_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.PSI_RESULT_INDEX_FILE)
        self.psi_result_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.PSI_RESULT_FILE)
        self.mpc_file_name = "{}.mpc".format(self.job_id)
        self.mpc_model_module_name = "{}.json".format(self.job_id)
        self.mpc_file_path = "{}{}{}".format(self.job_cache_dir, os.sep, self.mpc_file_name)
        self.mpc_prepare_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.MPC_PREPARE_FILE)
        self.mpc_result_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.MPC_RESULT_FILE)
        self.mpc_output_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.MPC_OUTPUT_FILE)

    @staticmethod
    def load_from_args(args, workspace):
        job_context = JobContext(args, workspace)
        job_context.my_index = job_context.participant_id_list.index(components.config_data['AGENCY_ID'])

        if job_context.job_type == JobType.PREPROCESSING or \
                job_context.job_type == JobType.TRAINING or \
                job_context.job_type == JobType.PREDICTION or \
                job_context.job_type == JobType.FEATURE_ENGINEERING:

            job_context.model_config_dict = args['model_config']
            job_context.tag_provider_agency_id = job_context.participant_id_list[0]
            if 'job_subtype' in job_context.model_config_dict:
                job_context.job_subtype = job_context.model_config_dict['job_subtype']
            if 'predict_algorithm' in job_context.model_config_dict:
                job_context.predict_algorithm = job_context.model_config_dict['predict_algorithm']
            if 'use_psi' in job_context.model_config_dict:
                job_context.need_run_psi = job_context.model_config_dict['use_psi'] == 1
            if 'use_iv' in job_context.model_config_dict:
                job_context.need_run_fe = job_context.model_config_dict['use_iv'] == 1

        if job_context.job_type == JobType.PSI:
            job_context.worker_configs = flow_dict['PSI']
        elif job_context.job_type == JobType.MPC:
            if 'sql' in job_context.args:
                job_context.sql = args['sql']
                job_context.mpc_content = CodeGenerator(job_context.sql)
            else:
                job_context.mpc_content = job_context.args['mpc_content']
            if "PSI_OPTION=True" in job_context.mpc_content:
                job_context.need_run_psi = True
                job_context.worker_configs = flow_dict['PSI_MPC']
            else:
                job_context.worker_configs = flow_dict['MPC']
        elif job_context.job_type == JobType.PREPROCESSING:
            job_context.worker_configs = flow_dict['PREPROCESSING']
        elif job_context.job_type == JobType.FEATURE_ENGINEERING:
            if job_context.need_run_psi:
                job_context.worker_configs = flow_dict['PSI_FEATURE_ENGINEERING']
            else:
                job_context.worker_configs = flow_dict['FEATURE_ENGINEERING']
        elif job_context.job_type == JobType.TRAINING:
            if job_context.need_run_psi:
                if job_context.need_run_fe:
                    job_context.worker_configs = flow_dict['PSI_FEATURE_ENGINEERING_TRAINING']
                else:
                    job_context.worker_configs = flow_dict['PSI_TRAINING']
            else:
                if job_context.need_run_fe:
                    job_context.worker_configs = flow_dict['FEATURE_ENGINEERING_TRAINING']
                else:
                    job_context.worker_configs = flow_dict['TRAINING']
        elif job_context.job_type == JobType.PREDICTION:
            job_context.worker_configs = flow_dict['PREDICTION']
        else:
            raise Exception("Unsupported job type {}".format(job_context.job_type))
        return job_context
