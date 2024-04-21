import json
import typing
from sys import stdin

import pydantic
from ordered_set import OrderedSet
from py_irt.dataset import Dataset
from sklearn.feature_extraction.text import CountVectorizer




class InputItem(pydantic.BaseModel):
    subject_id: int
    responses: typing.Dict[int, bool]


def load_dataset_from_iter(input_data: typing.Iterable[InputItem], train_items: dict = None,
                           amortized: bool = False) -> Dataset:
    item_ids = OrderedSet()
    subject_ids = OrderedSet()
    item_id_to_ix = {}
    ix_to_item_id = {}
    subject_id_to_ix = {}
    ix_to_subject_id = {}
    for line in input_data:
        subject_id = str(line.subject_id)
        subject_ids.add(subject_id)
        responses = line.responses
        for item_id in responses.keys():
            item_ids.add(str(item_id))

    for idx, item_id in enumerate(item_ids):
        item_id_to_ix[item_id] = idx
        ix_to_item_id[idx] = item_id

    for idx, subject_id in enumerate(subject_ids):
        subject_id_to_ix[subject_id] = idx
        ix_to_subject_id[idx] = subject_id

    if amortized:
        vectorizer = CountVectorizer(max_df=0.5, min_df=20, stop_words='english')
        vectorizer.fit(item_ids)

    observation_subjects = []
    observation_items = []
    observations = []
    training_example = []
    # console.log(f'amortized: {amortized}')
    for idx, line in enumerate(input_data):
        subject_id = str(line.subject_id)
        for item_id, response in line.responses.items():
            observations.append(response)
            observation_subjects.append(subject_id_to_ix[subject_id])
            if not amortized:
                observation_items.append(item_id_to_ix[str(item_id)])
            else:
                observation_items.append(vectorizer.transform([str(item_id)]).todense().tolist()[0])
            if train_items is not None:
                training_example.append(train_items[subject_id][str(item_id)])
            else:
                training_example.append(True)

    return Dataset(
        item_ids=item_ids,
        subject_ids=subject_ids,
        item_id_to_ix=item_id_to_ix,
        ix_to_item_id=ix_to_item_id,
        subject_id_to_ix=subject_id_to_ix,
        ix_to_subject_id=ix_to_subject_id,
        observation_subjects=observation_subjects,
        observation_items=observation_items,
        observations=observations,
        training_example=training_example,
    )


def load_dataset_from_stdin(train_items: dict = None,
                            amortized: bool = False) -> Dataset:
    stdin_iter = [InputItem(**json.loads(line.strip())) for line in stdin.readlines()]
    return load_dataset_from_iter(stdin_iter, train_items, amortized)


def load_dateset_from_file(file: str, train_items: dict = None, amortized: bool = False) -> Dataset:
    with open(file) as f:
        file_iter = [InputItem(**json.loads(line.strip())) for line in f.readlines()]

    return load_dataset_from_iter(file_iter, train_items, amortized)


if __name__ == '__main__':
    with open("ans.jsonline", "r") as f:
        input_iter = [InputItem(**json.loads(line.strip())) for line in f.readlines()]

    print(input_iter)

    out = load_dataset_from_iter(input_iter)

    print(out)
