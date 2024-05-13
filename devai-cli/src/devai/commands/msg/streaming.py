# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import click

from devai.util.file_processor import get_text_files_contents
from devai.util.secret_manager import get_access_secret
from vertexai.language_models import CodeChatModel, ChatModel

@click.command(name='with_msg_streaming')
@click.option('-q', '--query', required=False, type=str, default="Provide a summary of this source code")
@click.option('-p', '--path', required=False, type=str, default=".")
def with_msg_streaming(query, path):
   
    # code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    code_chat_model = CodeChatModel.from_pretrained("codechat-bison")
    # code_chat_model = CodeChatModel.from_pretrained("codechat-bison-32k")  
    # code_chat_model = ChatModel.from_pretrained("chat-bison@001")
   
    initial_prompt='''
    I'm going to provide you with a series of files individually over multiple messages. 
    For each file do nothing other than reply with the file name.  
    I will signify I'm done sending file with the following string "===LOAD COMPLETE===". 
    After I've sent the message "===LOAD COMPLETE===" respond listing all the file names you've received. 
    Next I will ask a question about all those files.

    Here are the files
    '''
    chat = code_chat_model.start_chat()


    responses = chat.send_message_streaming(initial_prompt)
    rtrn=""
    for response in responses:
        rtrn+=response.text
    click.echo(rtrn)


    ignored = ["__pycache__", "venv", ".vscode", ".git"]
    text_files_contents = get_text_files_contents(path, ignore=ignored)

    
    for full_path, contents in text_files_contents.items():
        click.echo(full_path)
#         click.echo(f'''
# File: {full_path}
# -----------------
# {contents}
# =================
# ''')
        rr=chat.send_message_streaming(f'''
File: {full_path}
-----------------
{contents}
=================
''')
        #click.echo(responses.response)
        # rtrn=""
        # for response in rr:
        #     rtrn+=response.text
        # click.echo(rtrn)
        

    chat.send_message_streaming("===LOAD COMPLETE===")
    #click.echo(response.response)

    # response = chat.send_message(query)
    # click.echo(response)

    click.echo(query)
    responses = chat.send_message_streaming(query)
    rtrn=""
    for response in responses:
        rtrn+=response.text
    click.echo(rtrn)