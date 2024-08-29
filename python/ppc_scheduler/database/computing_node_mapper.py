from sqlalchemy import update, and_, select, delete

from ppc_common.db_models.computing_node import ComputingNodeRecord


def insert_computing_node(session, node_id: str, url: str, node_type: str, loading: int):
    new_node = ComputingNodeRecord(
        id=node_id,
        url=url,
        type=node_type,
        loading=loading
    )

    session.add(new_node)


def delete_computing_node(session, url: str, node_type: str):
    stmt = (
        delete(ComputingNodeRecord).where(
            and_(
                ComputingNodeRecord.url == url,
                ComputingNodeRecord.type == node_type
            )
        )
    )

    result = session.execute(stmt)

    return result.rowcount > 0


def get_and_update_min_loading_url(session, node_type):
    subquery = (
        select([ComputingNodeRecord.id]).where(
            and_(
                ComputingNodeRecord.type == node_type
            )
        ).order_by(ComputingNodeRecord.loading.asc()).limit(1)
    ).scalar_subquery()

    stmt = (
        update(ComputingNodeRecord).where(
            and_(
                ComputingNodeRecord.id == subquery
            )
        ).values(
            loading=ComputingNodeRecord.loading + 1
        ).returning(ComputingNodeRecord.url)
    )

    result = session.execute(stmt)
    return result.scalar()


def release_loading(session, url: str, node_type: str):
    stmt = (
        update(ComputingNodeRecord).where(
            and_(
                ComputingNodeRecord.url == url,
                ComputingNodeRecord.type == node_type,
                ComputingNodeRecord.loading > 0
            )
        ).values(
            loading=ComputingNodeRecord.loading - 1
        )
    )
    result = session.execute(stmt)

    return result.rowcount > 0
