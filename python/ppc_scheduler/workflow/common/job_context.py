import os

class JobContext:
    DATASET_FILE = "dataset.csv"
    PSI_PREPARE_FILE = "psi_inputs"
    PSI_RESULT_INDEX_FILE = "psi_result_index"
    PSI_RESULT_FILE = "psi_result"
    MPC_PREPARE_FILE = "mpc_prepare.csv"
    MPC_RESULT_FILE = "mpc_result.csv"
    MPC_OUTPUT_FILE = "mpc_output.txt"

    def __init__(self, job_id, workspace):
        self.job_id = job_id
        self.workspace = workspace

        self.workflow_view_path = 'workflow_view'
        self.job_cache_dir = "{}{}{}".format(self.workspace, os.sep, self.job_id)
        self.dataset_file_path = "{}{}{}".format(self.job_cache_dir, os.sep, JobContext.DATASET_FILE)
        
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
    def create_job_context(request_json: object, workspace: str):
        
        job_id = request_json['jobId']
        job_context = JobContext(job_id=job_id, workspace = workspace)
        
        """
        request format
        {
        "jobId": "job_id",
        "agency": "WeBank",
        "workflow": [
            {
            "index": 1,
            "type": "WorkerType1",
            "args": [
                "arg1",
                "arg2"
            ]
            },
            {
            "index": 2,
            "type": "WorkerType1",
            "args": [
                "arg1",
                "arg2"
            ],
            "upstreams": [
                {
                "index": 1
                }
            ]
            }
        ]
        }
        """
        
        # job_context.request_json = request_json
        # job_context.job_id = request_json['jobId']
        job_context.agency = request_json['agency']
        job_context.workflow_configs = request_json['workflow']
        
        return job_context