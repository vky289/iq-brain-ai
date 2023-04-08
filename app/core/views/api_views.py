import uuid

from rest_framework import viewsets
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse

from app.core.serializers import QuestionsSerializer, StatsSerializer
from app.core.models import Questions, Answers, Stats


class QuestionsList(viewsets.ModelViewSet):
    """
    This API send back all the questions
    """
    serializer_class = QuestionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    http_method_names = ['get', 'post']

    def get_queryset(self):
        qq = self.queryset.order_by("id", "question", "iq_index", "created_date")
        return qq

    def perform_create(self, serializer):
        question = self.request.data.get("question", None)
        index = self.request.data.get("iq_index", None)
        answer = self.request.data.get("answer", None)
        w_answer = self.request.data.get("wrong_answer", None)
        if question and index and answer and w_answer:
            instance = serializer.save(question=question, iq_index=index)
            Answers.objects.create(options=answer, questions=instance, correct=True)
            for each in w_answer:
                Answers.objects.create(options=each, questions=instance, correct=False)


class ComposeQuestion(RetrieveUpdateAPIView):
    """
    This View is going to be used for composing questions based on the user inputs eg: name, age
    Also This is the entry point to the client, where app request for questions
    Question will be sent out with answer options, answer_id
    and also, it receives the answers from the client
    question_id, answer_id, question_index(number of questions answers by the current session)
    """
    serializer_class = QuestionsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Questions.objects.all()
    http_method_names = ['put']

    # def get(self, request, *args, **kwargs):
    #     age = self.request.data.get("age", None)
    #     session_id = self.request.data.get("session_id", None)
    #     return JsonResponse(data=self.compose_question(age), safe=False)

    def put(self, request, *args, **kwargs):
        name = self.request.data.get("name", None)
        age = self.request.data.get("age", None)
        session_id = self.request.data.get("session_id", None)
        question_id = self.request.data.get("question_id", None)
        answer_id = self.request.data.get("answer_id", None)
        q_index = self.request.data.get("question_index", None)
        submit = self.request.data.get("submit", None)
        print(self.request.data)
        if name and session_id:
            Stats.objects.get_or_create(name=name, age=age, session_id=session_id, iq_score=0)
        if q_index and q_index >= 20:
            Stats.objects.filter(name=name, age=age, session_id=session_id).update(iq_score=200)
        if submit:
            stats = Stats.objects.get_or_create(name=name, age=age, session_id=session_id, iq_score=200)
        return JsonResponse(data=self.compose_question(age, session_id)[0], safe=False)

    def compose_question(self, age, session_id):
        res = {}
        if age:
            qq = Questions.objects.order_by("?").filter(iq_index__gte=3).values()[:1]
        else:
            qq = Questions.objects.order_by("?").filter(iq_index__gte=1).values()[:1]
        qq = list(qq)
        for q in qq:
            if session_id is None:
                qq[0]['session_id'] = uuid.uuid4()
            else:
                qq[0]['session_id'] = session_id
            for aa in Answers.objects.filter(questions__id=q['id']):
                if qq[0].get('answers') is None:
                    qq[0]['answers'] = [{"answer_id": aa.id, "answer_option": aa.options}]
                else:
                    qq[0]['answers'] += [{"answer_id": aa.id, "answer_option": aa.options}]
        return qq


class StatsList(viewsets.ModelViewSet):
    """
    Stats List
    """
    serializer_class = StatsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Stats.objects.all()
    http_method_names = ['get', 'put']

    def get_queryset(self):
        return self.queryset.order_by("age", "-iq_score", "-created_date", "name", "id")

    def put(self, request, *args, **kwargs):
        session_id = self.request.data.get("session_id", None)

        stats = Stats.objects.filter(session_id=session_id).update(iq_score=200)
        print(self.request.data)

        res = Stats.objects.order_by("?").values()[:1]
        print(list(res)[0])
        return JsonResponse(data=list(res)[0], safe=False)
