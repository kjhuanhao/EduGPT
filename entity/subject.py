# -*- coding:utf-8 -*-
# @FileName  : subject.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : 科目类型

from enum import Enum


class SubjectType(Enum):
    Chinese = "语文"
    Math = "数学"
    English = "英语"
    Physics = "物理"
    Chemistry = "化学"
    Biology = "生物"
    Politics = "政治"
    History = "历史"
    Geography = "地理"

    @staticmethod
    def get(subject):
        for subject_type in SubjectType:
            if subject_type.name.lower() == subject.lower():
                return subject_type.value
        raise ValueError("科目类型不存在")

    @staticmethod
    def validate_subject_type(subject_type: str) -> bool:
        subjects = [value.name for value in list(SubjectType)]
        if subject_type not in subjects:
            raise ValueError("科目类型不存在")
        return True
