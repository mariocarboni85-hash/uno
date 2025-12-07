
from flask import Flask, render_template_string, request
from core.brain import SuperAgent
app = Flask(__name__)
MESSAGES = []
HTML = '''
<html><body>
<h2>Chat SuperAgent</h2>
<form method="post">
  <input name="msg" autofocus>
  <input type="submit" value="Invia">
</form>
<ul>{% for m in messages %}<li>{{m}}</li>{% endfor %}</ul>
</body></html>
'''

# Istanza SuperAgent
agent = SuperAgent(name="WebChatAgent", skills=["chat", "apprendimento", "risposta"])

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_msg = request.form['msg']
        MESSAGES.append(f"Tu: {user_msg}")
        # SuperAgent apprende e risponde
        agent.learn_from_chat(user_msg)
        risposta = agent.propose_solution(user_msg, ambito="informatica")
        MESSAGES.append(f"SuperAgent: {risposta}")
    return render_template_string(HTML, messages=MESSAGES)

if __name__ == '__main__':
    app.run(port=5000)
