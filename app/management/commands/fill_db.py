from random import choice, choices, sample
from string import ascii_letters, digits
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import *


class Command(BaseCommand):
    help = "Fill your database"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int, help="The filling ratio (num_users)")

    def handle(self, *args, **kwargs):
        ratio = kwargs["ratio"]

        users = []
        for _ in range(ratio):
            username = "".join(choices(ascii_letters + digits, k=10))
            user = User.objects.create_user(username=username, password="password1!")
            profile = Profile.objects.create(user=user)
            users.append(profile)

        self.stdout.write(self.style.SUCCESS("Users filled"))

        tags = [Tag.objects.create(name=f"tag {i}") for i in range(1, ratio)]

        self.stdout.write(self.style.SUCCESS("Tags filled"))

        questions = []
        for i in range(1, ratio * 10):
            question = Question.objects.create(
                user=choice(users),
                title=f"Question {i}",
                text=f"This is text about problem {i}"
            )
            question.tags.add(
                *sample(tags, k=2)
            )
            questions.append(question)

        self.stdout.write(self.style.SUCCESS("Questions filled"))

        answers = []
        for i in range(1, ratio * 100):
            question = choice(questions)
            answer = Answer.objects.create(
                question=question,
                user=choice(users),
                text=f"This is answer about problem{i}"
            )
            answers.append(answer)

        self.stdout.write(self.style.SUCCESS("Answers filled"))

        question_likes = []
        for _ in range(ratio * 200):
            user = choice(users)
            question = choice(questions)
            if not QuestionLike.objects.filter(user=user, question=question).exists():
                like = QuestionLike.objects.create(user=user, question=question)
                question_likes.append(like)

        self.stdout.write(self.style.SUCCESS("Q-Likes filled"))

        answer_likes = []
        for _ in range(ratio * 200):
            user = choice(users)
            answer = choice(answers)
            if not AnswerLike.objects.filter(user=user, answer=answer).exists():
                like = AnswerLike.objects.create(user=user, answer=answer)
                answer_likes.append(like)

        self.stdout.write(self.style.SUCCESS("A-Likes filled"))

        self.stdout.write(self.style.SUCCESS("Database filled"))