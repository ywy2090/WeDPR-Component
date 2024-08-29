import os
import time

from ppc_scheduler.workflow.common.job_context import JobContext
from ppc_scheduler.workflow.common.worker_type import WorkerType


class ModelWorkerEngine:
    def __init__(self, model_client, worker_type, components, job_context: JobContext):
        self.model_client = model_client
        self.worker_type = worker_type
        self.components = components
        self.job_context = job_context
        self.log = self.components.logger()

    def run(self) -> list:
        if self.worker_type == WorkerType.T_PREPROCESSING:
            self._run_preprocessing()
        elif self.worker_type == WorkerType.T_FEATURE_ENGINEERING:
            self._run_feature_engineering()
        elif self.worker_type == WorkerType.T_TRAINING:
            self._run_training()
        elif self.worker_type == WorkerType.T_PREDICTION:
            self._run_prediction()
        else:
            raise ValueError(f"Unsupported worker type: {self.worker_type}")
        return []

    def _run_preprocessing(self):
        start = time.time()
        job_id = self.job_context.job_id
        task_id = job_id + '_d'
        user_name = self.job_context.user_name
        dataset_storage_path = os.path.join(user_name, self.job_context.dataset_id)
        args = {
            'job_id': job_id,
            'task_id': task_id,
            'task_type': 'PREPROCESSING',
            'dataset_id': self.job_context.dataset_id,
            'dataset_storage_path': dataset_storage_path,
            'job_algorithm_type': self.job_context.job_type,
            'need_run_psi': self.job_context.need_run_psi,
            'model_dict': self.job_context.model_config_dict
        }
        self.log.info(f"start prepare_xgb, job_id: {job_id}, task_id: {task_id}, args: {args}")
        self.model_client.run(args)
        self.log.info(
            f"call compute_xgb_job service success, job: {job_id}, "
            f"task_id: {task_id}, timecost: {time.time() - start}")

    def _run_feature_engineering(self):
        start = time.time()
        job_id = self.job_context.job_id
        task_id = job_id + '_f'
        args = {
            'job_id': job_id,
            'task_id': task_id,
            'task_type': 'FEATURE_ENGINEERING',
            'is_label_holder': self.job_context.tag_provider_agency_id == self.components.config_data['AGENCY_ID'],
            'result_receiver_id_list': self.job_context.result_receiver_list,
            'participant_id_list': self.job_context.participant_id_list,
            'model_dict': self.job_context.model_config_dict
        }
        self.log.info(f"start feature_engineering, job_id: {job_id}, task_id: {task_id}, args: {args}")
        self.model_client.run(args)
        self.log.info(
            f"call compute_xgb_job service success, job: {job_id}, "
            f"task_id: {task_id}, timecost: {time.time() - start}")

    def _run_training(self):
        # todo 支持LR
        task_id = self.job_context.job_id + '_t'
        task_type = 'XGB_TRAINING'
        xgb_predict_algorithm = ''
        self._run_model(task_id, task_type, xgb_predict_algorithm)

    def _run_prediction(self):
        # todo 支持LR
        task_id = self.job_context.job_id + '_p'
        task_type = 'XGB_PREDICTING'
        xgb_predict_algorithm = self.job_context.predict_algorithm
        self._run_model(task_id, task_type, xgb_predict_algorithm)

    def _run_model(self, task_id, task_type, model_algorithm):
        job_id = self.job_context.job_id
        args = {
            "job_id": job_id,
            'task_id': task_id,
            'task_type': task_type,
            'is_label_holder': self.job_context.tag_provider_agency_id == self.components.config_data['AGENCY_ID'],
            'result_receiver_id_list': self.job_context.result_receiver_list,
            'participant_id_list': self.job_context.participant_id_list,
            'model_predict_algorithm': model_algorithm,
            "algorithm_type": self.job_context.job_type,
            "algorithm_subtype": self.job_context.job_subtype,
            "model_dict": self.job_context.model_config_dict
        }
        self.log.info(f"start run xgb task, job_id, job: {job_id}, "
                      f"task_id: {task_id}, task_type: {task_type}, args: {args}")
        self.model_client.run(args)
        self.log.info(f"call compute_xgb_job service success, job: {job_id}")
