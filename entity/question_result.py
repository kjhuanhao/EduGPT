# -*- coding:utf-8 -*-
# @FileName  : question_result.py
# @Time      : 2023/7/17
# @Author    : LaiJiahao
# @Desc      : 选择题

from typing import Dict


class ChoiceQuestionResult:
    def __init__(self, response: str):
        structure = dict(eval(response))
        self.question = structure["question"]
        self.options = {
            "A": structure["A"],
            "B": structure["B"],
            "C": structure["C"],
            "D": structure["D"],
        }
        self.clue = structure["clue"]
        self.answer = structure["answer"]
        self.explanation = structure["explanation"]
        self.type = "choice"

    def get_choice_question(self) -> Dict:
        return {
            "question": self.question,
            "options": self.options,
            "clue": self.clue,
            "answer": self.answer,
            "explanation": self.explanation,
            "type": self.type,
        }


class ShortAnswerQuestionResult:
    def __init__(self, response: str):
        structure = dict(eval(response))
        self.question = structure["question"]
        self.clue = structure["clue"]
        self.answer = structure["answer"]
        self.explanation = structure["explanation"]
        self.type = "short_answer"

    def get_short_answer_question(self) -> Dict:
        return {
            "question": self.question,
            "clue": self.clue,
            "answer": self.answer,
            "explanation": self.explanation,
            "type": self.type,
        }
