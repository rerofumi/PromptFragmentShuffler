import gradio as gr
import random
import json
import time
import PIL.Image as Image
import requests
import os
import io

import config

store_prompt = {"0": ["1girl"]}


# ------------------- mixer ------------------- #
def add_prompt(type, prompt):
    prompt["1"] = prompt["0"].copy()
    prompt["2"] = prompt["0"].copy()
    wordfile = f"./Collection/{type}.txt"
    if not os.path.exists(wordfile):
        return prompt
    with open(wordfile, "r", encoding="utf8") as f:
        words = [word.strip() for word in f.readlines() if not word.strip().startswith('#')]
    for key in ["1", "2"]:
        common_words = list(set(words) - set(prompt[key]))
        if len(common_words) > 0:
            add_word = common_words[random.randint(0, len(common_words) - 1)]
            prompt[key].append(add_word)
            print(f"Add word: {add_word}")
    return prompt


def remove_prompt(type, prompt):
    prompt["1"] = prompt["0"].copy()
    prompt["2"] = prompt["0"].copy()
    wordfile = f"./Collection/{type}.txt"
    if not os.path.exists(wordfile):
        return prompt
    with open(wordfile, "r", encoding="utf8") as f:
        words = [word.strip() for word in f.readlines() if not word.strip().startswith('#')]
    for key in ["1", "2"]:
        common_words = list(set(prompt[key]) & set(words))
        if len(common_words) > 0:
            delword = common_words[random.randint(0, len(common_words) - 1)]
            prompt[key].remove(delword)
            print(f"Remove word: {delword}")
    return prompt


def replace_prompt(type, prompt):
    prompt["1"] = prompt["0"].copy()
    prompt["2"] = prompt["0"].copy()
    wordfile = f"./Collection/{type}.txt"
    if not os.path.exists(wordfile):
        return prompt
    with open(wordfile, "r", encoding="utf8") as f:
        words = [word.strip() for word in f.readlines() if not word.strip().startswith('#')]
    for key in ["1", "2"]:
        common_words = list(set(prompt[key]) & set(words))
        if len(common_words) > 0:
            delword = common_words[random.randint(0, len(common_words) - 1)]
            common_words.remove(delword)
            prompt[key].remove(delword)
            diff_words = list(set(words) - set(common_words))
            word = diff_words[random.randint(0, len(diff_words) - 1)]
            prompt[key].append(word)
            print(f"Replace word: {delword} -> {word}")
    return prompt


def add_prompt_to_zero(type, prompt):
    wordfile = f"./Collection/{type}.txt"
    if not os.path.exists(wordfile):
        return prompt
    with open(wordfile, "r", encoding="utf8") as f:
        words = [word.strip() for word in f.readlines() if not word.strip().startswith('#')]
    # prompt["0"] にある単語は除外
    common_words = list(set(words) - set(prompt["0"]))
    if len(common_words) > 0:
        add_word = common_words[random.randint(0, len(common_words) - 1)]
        prompt["0"].append(add_word)
        print(f"Add word: {add_word}")
    return prompt


def t2i_request(prompt, negative):
    with open(config.COMFYUI_WORKFLOW, "r", encoding="utf-8") as f:
        prompt_path = json.load(f)
    ids = []
    # パラメータ埋め込み(workflowによって異なる処理)
    prompt_path[config.COMFYUI_NODE_CHECKPOINT]["inputs"]["ckpt_name"] = config.COMFYUI_USE_CHECKPOINT
    prompt_path[config.COMFYUI_NODE_PROMPT]["inputs"]["text"] = prompt
    prompt_path[config.COMFYUI_NODE_NEGATIVE]["inputs"]["text"] = negative
    prompt_path[config.COMFYUI_NODE_SEED]["inputs"]["seed"] = random.randint(
        1, 10000000000
    )
    request_id = send_request(prompt_path)
    return request_id


def send_request(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    response = requests.post(
        f"{config.COMFYUI_URL}prompt",
        headers=headers,
        data=json.dumps(data).encode("utf-8"),
    )
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()["prompt_id"]


def await_request():
    # 1秒ごとにリクエストの状態を確認
    while True:
        time.sleep(1)
        headers = {"Content-Type": "application/json"}
        response = requests.get(f"{config.COMFYUI_URL}queue", headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.text)
            time.sleep(3)
            continue
        json_data = response.json()
        # json の queue_running, queue_pending が存在し、 list 長が両方 0 の場合は break
        if (
            len(json_data["queue_running"]) == 0
            and len(json_data["queue_pending"]) == 0
        ):
            break


def get_image(id):
    # リクエストヒストリからファイル名を取得
    headers = {"Content-Type": "application/json"}
    response = requests.get(f"{config.COMFYUI_URL}history/{id}", headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    filename = response.json()[id]["outputs"][config.COMFYUI_NODE_OUTPUT]["images"][0][
        "filename"
    ]
    # API で画像ファイルを取得
    headers = {"Content-Type": "application/json"}
    params = {"filename": filename}
    response = requests.get(f"{config.COMFYUI_URL}view", headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    return Image.open(io.BytesIO(response.content))


# ------------------- gradio UI ------------------- #
# Function to generate random prompt
def random_prompt():
    global store_prompt
    prompt = {"0": ["1girl"]}
    for i in range(4):
        prompt = add_prompt_to_zero("positive", prompt)
    for i in range(1):
        prompt = add_prompt_to_zero("composition", prompt)
    for i in range(1):
        prompt = add_prompt_to_zero("pose", prompt)
    for i in range(1):
        prompt = add_prompt_to_zero("hairstyle", prompt)
    for i in range(2):
        prompt = add_prompt_to_zero("expression", prompt)
    for i in range(1):
        prompt = add_prompt_to_zero("cloths", prompt)
    for i in range(3):
        prompt = add_prompt_to_zero("accessory", prompt)
    for i in range(10):
        prompt = add_prompt_to_zero("location", prompt)
    for i in range(5):
        prompt = add_prompt_to_zero("props", prompt)
    prompt["1"] = prompt["0"].copy()
    prompt["2"] = prompt["0"].copy()
    store_prompt = prompt
    return ",".join(prompt["0"])


# Function to generate images
def generate_images(text_prompt, negative_prompt, operation, part, choice):
    prompt = store_prompt
    prompt["0"] = [word.strip() for word in text_prompt.split(",")]
    prompt["0"] = prompt[choice].copy()
    if operation == "add":
        prompt = add_prompt(part, prompt)
        word_a = ",".join(list(set(prompt["1"]) - set(prompt["0"])))
        word_b = ",".join(list(set(prompt["2"]) - set(prompt["0"])))
    elif operation == "remove":
        prompt = remove_prompt(part, prompt)
        word_a = ",".join(list(set(prompt["0"]) - set(prompt["1"])))
        word_b = ",".join(list(set(prompt["0"]) - set(prompt["2"])))
    elif operation == "replace":
        prompt = replace_prompt(part, prompt)
        word_a = ",".join(list(set(prompt["1"]) - set(prompt["0"])))
        word_b = ",".join(list(set(prompt["2"]) - set(prompt["0"])))
    id1 = t2i_request(",".join(prompt["1"]), negative_prompt)
    id2 = t2i_request(",".join(prompt["2"]), negative_prompt)
    await_request()
    img_a = get_image(id1)
    img_b = get_image(id2)
    return img_a, img_b, ",".join(prompt["0"]), word_a, word_b


def generate_images_add_a(prompt, negative_prompt, operation, part):
    return generate_images(prompt, negative_prompt, operation, part, "1")


def generate_images_add_b(prompt, negative_prompt, operation, part):
    return generate_images(prompt, negative_prompt, operation, part, "2")


def generate_images_neither(prompt, negative_prompt, operation, part):
    return generate_images(prompt, negative_prompt, operation, part, "0")


# Create Gradio interface
with gr.Blocks() as demo:
    prompt = gr.Textbox(
        label="Prompt", placeholder="Enter prompt here...", value="1girl"
    )
    with gr.Row():
        gr.Button("🎲", variant="primary").click(fn=random_prompt, outputs=prompt)
    negative_prompt = gr.Textbox(
        label="Negative Prompt",
        placeholder="Enter negative prompt here...",
        value="worst quality, low quality, normal quality, poorly drawn face, poorly drawn hands, ugly, bad anatomy, bad hands, missing fingers, disfigured, mutation, mutated, extra limb,missing limbs, floating limbs, disconnected limbs, signature, watermark, username, blurry, cropped",
    )
    with gr.Row():
        with gr.Column():
            img_a = gr.Image(label="Image A")
            add_word_a = gr.Textbox(
                label="Word A", placeholder="new word...", interactive=False
            )
        with gr.Column():
            img_b = gr.Image(label="Image B")
            add_word_b = gr.Textbox(
                label="Word B", placeholder="new word...", interactive=False
            )
    with gr.Row():
        operation = gr.Dropdown(
            choices=["add", "replace", "remove"], label="Operate", value="add"
        )
        part = gr.Dropdown(
            choices=config.PROMPT_PARTS_LIST, label="Parts", value="positive"
        )
    with gr.Row():
        btn_a = gr.Button("A")
        btn_neither = gr.Button("Neither")
        btn_b = gr.Button("B")

    # Button click handlers
    btn_a.click(
        fn=generate_images_add_a,
        inputs=[prompt, negative_prompt, operation, part],
        outputs=[img_a, img_b, prompt, add_word_a, add_word_b],
    )
    btn_b.click(
        fn=generate_images_add_b,
        inputs=[prompt, negative_prompt, operation, part],
        outputs=[img_a, img_b, prompt, add_word_a, add_word_b],
    )
    btn_neither.click(
        fn=generate_images_neither,
        inputs=[prompt, negative_prompt, operation, part],
        outputs=[img_a, img_b, prompt, add_word_a, add_word_b],
    )

demo.launch()
