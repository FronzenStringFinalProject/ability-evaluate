from typing import List, Dict

from pydantic import BaseModel


class BestParams(BaseModel):
    ability: List[float]
    diff: List[float]
    disc: List[float]
    lambdas: List[float]
    irt_model: str
    item_ids: Dict[str, str]
    subject_ids: Dict[str, str]


class SubjectOutput(BaseModel):
    subject_id: int
    ability: float


class ItemOutput(BaseModel):
    item_id: int
    diff: float
    disc: float
    lambdas: float


def serialize(params: BestParams):
    id_to_item = params.subject_ids
    id_to_quiz = params.item_ids

    for idx, ability in enumerate(params.ability):
        output = SubjectOutput(subject_id=int(id_to_item[str(idx)]), ability=ability)
        yield output

    for idx, (diff, disc, lambdas) in enumerate(zip(params.diff, params.disc, params.lambdas)):
        quiz_id = int(id_to_quiz[str(idx)])
        output = ItemOutput(item_id=quiz_id, diff=diff, disc=disc, lambdas=lambdas)
        yield output
