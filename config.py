# API endpoint of ComfyUI
COMFYUI_URL = 'http://127.0.0.1:8188/'
# ComfyUI workflow
COMFYUI_WORKFLOW = "./Workflow/text2image_api.json"
# ComfyUI model checkpoint
COMFYUI_USE_CHECKPOINT = "animagineXLV31_v31.safetensors"
#COMFYUI_USE_CHECKPOINT = "AnythingXL_xl.safetensors"
# ComfyUI checkpoint node
COMFYUI_NODE_CHECKPOINT = "6"
# ComfyUI prompt node
COMFYUI_NODE_PROMPT = "7"
# ComfyUI negative prompt node
COMFYUI_NODE_NEGATIVE = "8"
# ComfyUI seed node
COMFYUI_NODE_SEED = "13"
# ComfyUI output node
COMFYUI_NODE_OUTPUT = "14"

# parts collection list
PROMPT_PARTS_LIST = ["positive", "pose", "composition", "hairstyle", "expression", "cloths", "accessory", "location", "props",]
