
import re
import traceback

try: import readline
except: pass 

from dotenv import load_dotenv # pyright: ignore
from supp.config import set_config, todo
from supp import helpers

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory

def repl():

    llm, chat = helpers.get_llm()
   
    calc_template = todo['apps'].get_calc_template(PromptTemplate)
    calc_template_ctxt = todo['apps'].get_calc_template_ctx(PromptTemplate)
    calc_context = todo['apps'].get_calc_context()

    calc_chain = todo['apps'].get_chain(
        Chain = LLMChain,
        llm = llm,
        tmpl = calc_template
    ) if calc_template else None

    calc_chain_ctxt = todo['apps'].get_chain(
        Chain = LLMChain,
        llm = chat,
        tmpl = calc_template_ctxt
    ) if calc_template_ctxt else None

    chat_template = todo['apps'].get_chat_template(PromptTemplate)
    chat_memory = todo['apps'].get_chat_memory(ConversationBufferMemory)

    chat_chain = todo['apps'].get_chain(
        Chain = LLMChain,
        llm = chat,
        tmpl = chat_template
    ) if chat_template else None

    chat_chain_mem = todo['apps'].get_chain_mem(
        Chain = LLMChain,
        llm = chat,
        tmpl = chat_template,
        chat_memory = chat_memory
    ) if chat_template and chat_memory else None

    app = None

    while True:

        app_prompt = helpers.get_app_prompt(app)

        try:
            user_input = input(app_prompt)

        except EOFError:
            print('')
            break        

        if not user_input.strip(): continue
        input_strings = user_input.lower().split()
        command = input_strings[0]

        try:

            if app and command != 'app':

                # --------------------------------------------------------------
                if app == '1':
                # --------------------------------------------------------------

                    response = todo['apps'].invoke_llm(llm, prompt=user_input)
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                elif app == '2':
                # --------------------------------------------------------------

                    if not calc_template: continue

                    response = todo['apps'].invoke_llm_tmpl(
                        llm = llm,
                        tmpl = calc_template, 
                        expr = user_input
                    )
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                elif app == '3':
                # --------------------------------------------------------------

                    if not calc_chain: continue

                    response = todo['apps'].invoke_chain(
                        chain = calc_chain, 
                        params={'expr': user_input}
                    )
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                elif app == '4':
                # --------------------------------------------------------------

                    if not (calc_context and calc_chain_ctxt): continue

                    response = todo['apps'].invoke_chain(
                        chain = calc_chain_ctxt, 
                        params = {
                            'expr': user_input,
                            'functions': calc_context
                        }
                    )
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                elif app == '5':
                # --------------------------------------------------------------

                    if not chat_chain: continue

                    response = todo['apps'].invoke_chain(
                        chain = chat_chain, 
                        params = {
                            'chat_history': '',
                            'question': user_input
                        }
                    )
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                elif app == '6':
                # --------------------------------------------------------------

                    if not chat_chain_mem: continue

                    response = todo['apps'].invoke_chain( 
                        chain = chat_chain_mem, 
                        params = {
                            'question': user_input
                        }
                    )
                    helpers.print_blue(response)
                    continue

                # --------------------------------------------------------------
                continue
                # --------------------------------------------------------------

            if len(input_strings) == 1: 

                if command in ('exit', 'quit'):
                    break

                if command in ('app'):
                    app = None
                    continue

                raise AssertionError

            if len(input_strings) == 2: 

                if command in ('app'):

                    param = input_strings[1]
                    if not re.search("^[1-6]$",param): 
                        raise AssertionError
                    app = param
                    continue

                raise AssertionError

            raise AssertionError

        except AssertionError:
            print('Usage:{ app [ {1|2|3|4|5|6} ] | <llm_promt> | exit | quit }')
            
        except Exception as err:
            print(err)
            # traceback.print_exc()

if __name__ == '__main__':

    load_dotenv()
    set_config()
    repl()
