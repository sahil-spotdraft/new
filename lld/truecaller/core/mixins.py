import abc
from collections import defaultdict
from enum import Enum
from typing import Any, Dict, List

from core.exceptions import Raise404


class SortOrder(Enum):
    ACS = "acs"
    DESC = "desc"


class ModelSet(list):
    def __init__(self, seq: List["ModelMixin"]):
        self.__list = list(seq)

    def to_list(self):
        return self.__list
    
    def to_dict(self):
        return [
            item.to_dict() for item in self.to_list()
        ]

    def order_by(self, field: str, order: SortOrder = SortOrder.ACS.value):
        try:
            sorted_data = sorted(self.to_list(), key=lambda x: x[field], reverse=(order == SortOrder.DESC.value))
            return ModelSet(sorted_data)
        except KeyError:
            raise
    
    def count(self):
        return len(self.to_list())

    def __repr__(self):
        return f"ModelSet({self.to_list()})"
    

class IdMixin(abc.ABC):
    __entry_id: int = 1

    def __init__(self):
        self.id = self.__class__.__entry_id
        self.__class__.__entry_id += 1
    

class DbMixin(IdMixin):
    def __init__(self):
        super().__init__()
        self._store_data()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.meta = cls.meta if hasattr(cls, "meta") else {}
        cls.indexes = {}
        cls.objects: Dict[int, cls] = {}
        cls._read_meta()

    def _store_data_in_indexes(self, index):
        data = getattr(self, index["name"], {})
        l = []
        dict_data = self.to_dict()
        for field in index["fields"]:
            if isinstance(dict_data[field], IdMixin):
                l.append(dict_data[field].id)
            else:
                l.append(dict_data[field])
        _index_key = l[0] if len(l) == 1 else tuple(l)
        if index["unique"]:
            data[_index_key] = self
        else:
            data[_index_key].append(self)
        setattr(self.__class__, index["name"], data)

    def _store_data(self):
        self.objects[self.id] = self
        for key in self.__class__.indexes:
            index = self.__class__.indexes[key]
            self._store_data_in_indexes(index)

    @classmethod
    def _read_meta(cls):
        if cls.meta:
            cls._create_indexes()

    @classmethod
    def _create_indexes(cls):
        if "indexes" in cls.meta:
            for index in cls.meta["indexes"]:
                if index["unique"]:
                    setattr(cls, index["name"], {})
                else:
                    setattr(cls, index["name"], defaultdict(list))
                cls.indexes[index["name"]] = index


class ModelMixin(DbMixin):
    @classmethod
    def _get_fields(cls):
        return {key for key in cls.__dict__ if not key.startswith("__")}

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
    
    def __str__(self):
        return f"<{self.__class__.__name__}: {self.id}>"
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"
    
    @classmethod
    def list(cls, data_set_name: str = "objects"):
        data_set = getattr(cls, data_set_name, None)
        if not data_set: return AttributeError
        return ModelSet(
            data_set.values()
        )
    
    @classmethod
    def filter_by_ids(cls, ids: List[int]) -> ModelSet:
        return ModelSet([
            cls.objects[id].to_dict() for id in ids if id in cls.objects
        ])
    
    def _delete_from_indexes(self, index):
        data = getattr(self.__class__, index["name"], {})
        l = []
        dict_data = self.to_dict()
        for field in index["fields"]:
            if isinstance(dict_data[field], IdMixin):
                l.append(dict_data[field].id)
            else:
                l.append(dict_data[field])
        _index_key = l[0] if len(l) == 1 else tuple(l)
        data.pop(_index_key)
        setattr(self.__class__, index["name"], data)
    
    @classmethod
    def delete(cls, ids: List[int]):
        for id in ids:
            if id in cls.objects: 
                obj = cls.objects.pop(id)
                print(obj.id)
                if not obj: return
                if "indexes" not in cls.meta: continue
                for key in cls.indexes:
                    index = cls.indexes[key]
                    obj._delete_from_indexes(index)
                    del obj

    @classmethod
    def get(cls, id: int):
        try:
            return cls.objects[id]
        except KeyError:
            raise Raise404

    @classmethod
    def filter(cls, attrs: List[str], values: List[Any] = []):
        # try:
        #     index = None
        #     for key in cls.indexes:
        #         curr_index = cls.indexes[key]
        #         if len(attrs) == 1 and len(curr_index["fields"]) == 1:
        #             if attrs[0] == curr_index["fields"][0]:
        #                 index = key
        #         elif sorted(attrs) == sorted(curr_index["fields"]):
        #             index = key
        #             break
        #     if index:
        #         index_data = getattr(cls, index, {})
        #         data = []
        #         for value in values:
        #             if value in index_data:
        #                 data.extend(index_data[value])
        #         return ModelSet(data)
        # except:
        #     pass

        data = cls.objects.values()
        for attr in attrs:
            try:
                data = filter(
                    lambda obj: str(getattr(obj, attr)).lower() in [str(v).lower() for v in values],
                    list(data)
                )
            except AttributeError:
                raise AttributeError(f"{attr} not found for {cls.__name__} object")
                
        return ModelSet(data)