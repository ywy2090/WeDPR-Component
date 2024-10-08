from sqlalchemy import update, and_, select, delete
from sqlalchemy.exc import NoResultFound
from ppc_common.db_models.computing_node import ComputingNodeRecord


# def insert_computing_node(session, node_id: str, url: str, node_type: str, loading: int):
#     new_node = ComputingNodeRecord(
#         id=node_id,
#         url=url,
#         type=node_type,
#         loading=loading
#     )

#     session.add(new_node)


# def delete_computing_node(session, url: str, node_type: str):
#     stmt = (
#         delete(ComputingNodeRecord).where(
#             and_(
#                 ComputingNodeRecord.url == url,
#                 ComputingNodeRecord.type == node_type
#             )
#         )
#     )

#     result = session.execute(stmt)

#     return result.rowcount > 0


def get_and_update_min_loading_url(session, node_type):
    
    # select min_loading node
    min_loading_node = session.query(ComputingNodeRecord.url, ComputingNodeRecord.token, ComputingNodeRecord.id).filter(
        ComputingNodeRecord.type == node_type
    ).order_by(ComputingNodeRecord.loading.asc()).first()
    
    if min_loading_node is None:
        raise NoResultFound("No computing node found with the specified node type and minimum loading, node type is: " + node_type)
    
    # update loading
    stmt = (
        update(ComputingNodeRecord).where(
            and_(
                ComputingNodeRecord.id == min_loading_node.id
            )
        ).values(
            loading=ComputingNodeRecord.loading + 1
        )
    )
    session.execute(stmt)

    return min_loading_node

def release_loading(session, node_id: str):
    stmt = (
        update(ComputingNodeRecord).where(
            and_(
                ComputingNodeRecord.id == node_id,
                ComputingNodeRecord.loading > 0
            )
        ).values(
            loading=ComputingNodeRecord.loading - 1
        )
    )
    result = session.execute(stmt)

    return result.rowcount > 0
