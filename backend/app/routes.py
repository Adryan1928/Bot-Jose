from fastapi import APIRouter, Depends, HTTPException
import os
from sqlalchemy.orm import Session
from dependecies import get_session
from schemas import MessageSchema, QuestionSchema
from utils import create_instance, update_instance
from models import User, Choices, Question
import random

messages_default = [
    {"id": 1, "message": "Bem vindo ao BotJosé!\n Escolhas umas das opções:\n0-sair\n1-Responder questão aleatória"},
    {"id": 2, "message": "Como é seu primeiro acesso, por favor, digite seu nome:"},
    {"id": 3, "message": "Mensagem inválida, escolha uma das opções!"},
    {"id": 4, "message": "Obrigado por usar nosso serviço!"},
    {"id": 5, "message": "Deseja continuar?\n0-Sim\n1-Não"}
]

router = APIRouter()

instance_name = os.getenv("BACK_NAME", "default-backend")

@router.get("/")
async def home():

    return {"messages": "Bem vindo ao BotJosé!", "instância": instance_name}

@router.post("/")
async def create_message(message: MessageSchema, session:Session=Depends(get_session)):
    try:
        user = session.query(User).filter(User.number == message.number).first()
        if not user:
            user = User(number=message.number)
            create_instance(session, user)
            user.last_received_message = messages_default[1]["message"]
            update_instance(session)
            return {"message": messages_default[1]["message"]}

        elif user.last_received_message == messages_default[1]["message"] or user.last_received_message == None or user.last_sent_message == None:

            user.last_received_message = messages_default[0]["message"]
            user.last_sent_message = None
            update_instance(session)
            return {"message": messages_default[0]["message"]}
        
        elif user.last_received_message == messages_default[0]["message"]:
            if (message.message == "0" or message.message.lower() == "sair"):
                user.last_received_message = None
                user.last_sent_message = None
                update_instance(session)
                return {"message": messages_default[3]["message"]}
            elif (message.message == "1" or message.message.lower() == "responder questão aleatória"):
                
                user.last_sent_message = message.message
                

                questions = session.query(Question).all()
                max_random = len(questions) - 1
                random_question = questions[random.randint(0, max_random)]

                choices = session.query(Choices).filter(Choices.question_id == random_question.id).all()

                user.last_received_message = "question:" + str(random_question.id)
                update_instance(session)

                message = "Pergunta: " + random_question.question + "\n\nEscolha uma das opções:\n"
                for choice in choices:
                    message += f"{choice.id}- {choice.text}\n"
                return {"message": message}
        
        elif user.last_received_message.startswith("question:"):
            question_id = int(str(user.last_received_message).split(":")[1])
            question = session.query(Question).filter(Question.id == question_id).first()
            if question:
                if (message.message.isdigit()):
                    choice_id = int(message.message)
                    choice = session.query(Choices).filter(Choices.id == choice_id).first()
                    if choice:
                        user.last_received_message = messages_default[0]["message"]
                        user.last_sent_message = None
                        if (choice.is_right):
                            return {"message": f"Resposta correta!\n{messages_default[4]['message']}"}
                        else:
                            return {"message": f"Resposta errada, tente novamente!\n{messages_default[5]['message']}"}
    finally:
        return {"message": messages_default[2]["message"]}
    


@router.post("/create_question")
async def create_question(question: QuestionSchema, session: Session = Depends(get_session)):
    try:
        question = question.model_dump()
        print(question)
        new_question = Question(question=question["question"])
        create_instance(session, new_question)
        for choice in question["choices"]:
            new_choice = Choices(text=choice["text"], is_right=choice["is_right"], question_id=new_question.id)
            create_instance(session, new_choice)

        
        return {"message": "Pergunta criada com sucesso."}
    
    except Exception as e:
        print(e)
        session.rollback()
        raise HTTPException(status_code=400, detail={"message": "Erro ao criar pergunta."})