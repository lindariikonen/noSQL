
#
# do not import anything
#


def invoke_llm(llm, prompt):
    response = llm.invoke(prompt)
    return response


def get_calc_template(Templ):
    tmpl = """
    Interpret only mathemathical expressions. You should limit your
    response to the expression entered by the user and it's result in the form
    'expression = result'.
    Solve the following equation: {expression}

    If the prompt is not a mathematical expression, respond with 'not an expression'.
    No further explanation is needed.
    """
    prompt = Templ(input_variables=["expression"],template=tmpl)
    return prompt


def invoke_llm_tmpl(llm, tmpl, expr):
    result = llm.invoke(tmpl.format(expression=expr))
    return result


def get_chain(Chain, llm, tmpl ):
    chain = Chain(llm=llm, prompt=tmpl)
    return chain


def invoke_chain(chain, params):
    if 'question' in params.keys():
        if 'chat_history' in params.keys():
            response = chain.invoke({"question":params['question'], "chat_history":params['chat_history']})
        else: response = chain.invoke({"question":params['question']})
    elif 'functions' in params.keys():
        response = chain.invoke({"expression":params['expr'], "function":params['functions']})
    else: response = chain.invoke({"expression":params['expr']})
    return response['text']


def get_calc_template_ctx(Templ):
    tmpl = """
    Calculate the hypotenuse according to directions in {function}.
    You should limit your response to 'sqrt(a^2 + b^2) = result' with 'a' and 'b'
    replaced by the numbers given by the user.
    Solve the hypothenuse according to these instructions from {expression}.
    """
    prompt = Templ(input_variables=["expression","function"],template=tmpl)
    return prompt


def get_calc_context():
    context = {"name": "hypotenuse",
         "description": "returns the length of the hypotenuse of a right-angled triangle when the lengths of the legs are given as parameters",
         "parameters": ["a", "b"]}
    
    return context


def get_chat_template(Templ):
    template= """You are a friendly AI who answers shortly to human's
    questions. Chat history: {chat_history}
    Answer the {question} according to instructions.
    """
    prompt = Templ(template=template)
    return prompt


def get_chat_memory(ChatMemory):
    memory = ChatMemory(memory_key="chat_history")
    memory.load_memory_variables({})
    return memory


def get_chain_mem(Chain, llm, tmpl, chat_memory):
    chain = Chain(llm=llm, prompt=tmpl, memory=chat_memory)
    return chain
