from django.core.management.base import BaseCommand

from feedback.models import Question
import csv

class Command(BaseCommand):

    def handle(self, *args, **options):
        Question.objects.all().delete()

        with open('data/feedback_questions.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=';')
            for row in csv_reader:
                question_text, question_type, question_allow_comment, question_order, choice_text = row
                question_allow_comment = question_allow_comment == "True"
                question_order = int(question_order)
                if question_type == "text":
                    question = Question.objects.create(text=question_text, type=question_type, allow_comment=question_allow_comment, order=question_order)
                else:
                    question, _ = Question.objects.get_or_create(text=question_text, type=question_type, allow_comment=question_allow_comment, order=question_order)
                    question.choices.create(text=choice_text)

