from sqlalchemy import and_, update
from sqlalchemy.exc import NoResultFound

from ppc_common.db_models.job_worker_record import JobWorkerRecord
from ppc_common.ppc_utils import utils
from ppc_scheduler.workflow.common import codec


def query_job_worker(session, job_id, worker_id):
    try:
        return session.query(JobWorkerRecord).filter(
            and_(JobWorkerRecord.worker_id == worker_id,
                 JobWorkerRecord.job_id == job_id)).one()
    except NoResultFound:
        return None


def update_job_worker(session, job_id, worker_id, status, outputs):
    stmt = (
        update(JobWorkerRecord).where(
            and_(
                JobWorkerRecord.job_id == job_id,
                JobWorkerRecord.worker_id == worker_id
            )
        ).values(
            status=status,
            outputs=codec.serialize_worker_outputs_for_db(outputs),
            update_time=utils.make_timestamp()
        )
    )
    result = session.execute(stmt)
    return result.rowcount > 0
