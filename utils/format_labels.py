from typing import List, Tuple, Dict

def fill_labels(labels:List[str],pad_length:int) -> List[str]:
    for label in labels:
        for _ in range(pad_length):
            yield label

def get_label_index_mappings(labels:List[str]) -> Tuple[Dict[int,str],Dict[str,int]]:
    index_label_mapping = dict(enumerate(set(labels)))
    label_index_mapping = {label:index for index,label in index_label_mapping.items()}
    return (index_label_mapping,label_index_mapping)

def remove_consequtive_duplicates(labels:List[str]) -> List[str]:
    previous_label = ''
    for label in labels:
        if label != previous_label:
            yield label
            previous_label = label