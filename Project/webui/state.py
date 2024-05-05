import os
import requests
import json
import reflex as rx


BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")


def get_access_token():
    """
    :return: access_token
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": BAIDU_API_KEY,
        "client_secret": BAIDU_SECRET_KEY,
    }
    return str(requests.post(url, params=params).json().get("access_token"))


class QA(rx.Base):
    """A question and answer pair."""

    question: str
    answer: str


DEFAULT_CHATS = {
    "Intros": [],
}



def news(name):
    print(name)
    Statex.bb("Success2")

class Statex(rx.State):
    """The app state."""

    # A dict from the chat name to the list of questions and answers.
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    # The current chat name.
    current_chat = "Intros"

    # The current question.
    question: str

    # Whether we are processing the question.
    processing: bool = False

    # The name of the new chat.
    new_chat_name: str = ""

    # Whether the drawer is open.
    drawer_open: bool = False

    # Whether the modal is open.
    modal_open: bool = False

    api_type: str = "baidu" if BAIDU_API_KEY else "openai"
    
    def bb(self,string):
        print(string)
    def gg(self):
        print("Hehe")
    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_name
        self.chats[self.new_chat_name] = []

        # Toggle the modal.
        self.modal_open = False

    def toggle_modal(self):
        """Toggle the new chat modal."""
        self.modal_open = not self.modal_open

    def toggle_drawer(self):
        """Toggle the drawer."""
        self.drawer_open = not self.drawer_open

    def delete_chat(self):
        """Delete the current chat."""
        del self.chats[self.current_chat]
        if len(self.chats) == 0:
            self.chats = DEFAULT_CHATS
        self.current_chat = list(self.chats.keys())[0]
        self.toggle_drawer()

    def set_chat(self, chat_name: str):
        """Set the name of the current chat.

        Args:
            chat_name: The name of the chat.
        """
        self.current_chat = chat_name
        self.toggle_drawer()

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    def scroll_to_bottom(self):
        return rx.call_script(
        """
        window.scrollTo(0, document.body.scrollHeight);
        """
    )








    async def process_question(self, form_data: dict[str, str]):
        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        if self.api_type == "openai":
            model = self.openai_process_question
        else:
            model = self.baidu_process_question

        async for value in model(question):
            yield value

    async def process_question1(self, strr):
        # Get the question from the form
        question = strr

        # Check if the question is empty
        if question == "":
            return

        
        model = self.openai1
       

        async for value in model(question):
            yield value
    


    async def openai_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        if question is None:
            return
        
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly chatbot named Reflex."}
        ]
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        from .llm import q
        session = q(question)
        self.chats[self.current_chat][-1].answer += session
        yield
        #print(session)
        
        

        # Stream the results, yielding after every word.
        

        # Toggle the processing flag.
        self.processing = False
        yield self.scroll_to_bottom()

        
        
        

        # Stream the results, yielding after every word.
        

        # Toggle the processing flag.
        self.processing = False

    async def openai1(self, question : str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        if question is None:
            return
        
        # Add the question to the list of questions.
        qa1 = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa1)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = [
            {"role": "system", "content": "You are a friendly chatbot named Reflex."}
        ]
        for qa1 in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa1.question})
            messages.append({"role": "assistant", "content": qa1.answer})

        # Remove the last mock answer.
        messages = messages[:-1]

        # Start a new session to answer the question.
        from .llm import q
        session = q(question)
        self.chats[self.current_chat][-1].answer += session
        print(session)
        
        

        # Stream the results, yielding after every word.
        

        # Toggle the processing flag.
        self.processing = False
        yield self.scroll_to_bottom()
        
        

        

    async def baidu_process_question(self, question: str):
        """Get the response from the API.

        Args:
            form_data: A dict with the current question.
        """
        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        # Clear the input and start the processing.
        self.processing = True
        yield

        # Build the messages.
        messages = []
        for qa in self.chats[self.current_chat]:
            messages.append({"role": "user", "content": qa.question})
            messages.append({"role": "assistant", "content": qa.answer})

        # Remove the last mock answer.
        messages = json.dumps({"messages": messages[:-1]})
        # Start a new session to answer the question.
        session = requests.request(
            "POST",
            "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
            + get_access_token(),
            headers={"Content-Type": "application/json"},
            data=messages,
        )

        json_data = json.loads(session.text)
        if "result" in json_data.keys():
            answer_text = json_data["result"]
            self.chats[self.current_chat][-1].answer += answer_text
            self.chats = self.chats
            yield
        # Toggle the processing flag.
        self.processing = False
