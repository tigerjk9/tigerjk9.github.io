"""
generate_image.py — 이미지 생성 스크립트

지원 API:
  - gemini   : Google Gemini Imagen API (클라우드, API 키 필요)
  - comfyui  : ComfyUI 로컬 서버 (http://localhost:8188)
  - sd_webui : Stable Diffusion WebUI 로컬 서버 (http://localhost:7860)

Usage:
    python generate_image.py "<prompt>" "<filename>" "<output_dir>" [api_type]

Output:
    SUCCESS:<absolute_path>   — 성공 시
    ERROR:<message>           — 실패 시
"""

import sys
import os
import base64
import time
import yaml
import requests


def generate_gemini(prompt: str, cfg: dict) -> bytes:
    """Google Gemini API로 이미지 생성, JPEG bytes 반환.

    모델 계열에 따라 API 호출 방식 분기:
      - imagen-*  : client.models.generate_images()
      - gemini-*  : client.models.generate_content() with IMAGE modality
    """
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise ImportError(
            "google-genai 패키지가 필요합니다: pip install google-genai"
        )

    api_key = cfg.get("gemini_api_key") or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "Gemini API 키가 없습니다. "
            "config.yaml의 gemini_api_key 또는 GEMINI_API_KEY 환경변수를 설정하세요."
        )

    client = genai.Client(api_key=api_key)
    model = cfg.get("gemini_model", "gemini-3.1-flash-image-preview")

    if model.startswith("imagen"):
        # Imagen 계열: generate_images() 사용
        response = client.models.generate_images(
            model=model,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/jpeg",
            ),
        )

        if not response.generated_images:
            raise ValueError("이미지 생성 실패: Gemini 응답이 비어 있습니다")

        img = response.generated_images[0].image

        if hasattr(img, "data") and img.data:
            return img.data

        # 폴백: 임시 파일 저장 후 읽기
        import tempfile
        tmp_path = tempfile.mktemp(suffix=".jpg")
        try:
            img.save(tmp_path)
            with open(tmp_path, "rb") as f:
                return f.read()
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    else:
        # Gemini Flash Image 계열: generate_content() 사용
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                return part.inline_data.data  # raw bytes (SDK가 base64 디코딩)

        raise ValueError("이미지 생성 실패: 응답에 이미지가 없습니다")


def load_config():
    """tools/config.yaml 로드"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.yaml")
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_comfyui(prompt: str, cfg: dict) -> bytes:
    """ComfyUI API로 이미지 생성, PNG bytes 반환"""
    api_url = cfg["api_url"]

    # 간단한 txt2img 워크플로우
    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "seed": int(time.time()) % 2**32,
                "steps": cfg.get("steps", 20),
                "cfg": cfg.get("cfg_scale", 7),
                "sampler_name": cfg.get("sampler", "euler"),
                "scheduler": cfg.get("scheduler", "normal"),
                "denoise": 1.0,
                "model": ["4", 0],
                "positive": ["6", 0],
                "negative": ["7", 0],
                "latent_image": ["5", 0],
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": cfg.get("model", "nanobana2.safetensors")},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "width": cfg.get("width", 1024),
                "height": cfg.get("height", 768),
                "batch_size": 1,
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["4", 1]},
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": cfg.get("negative_prompt", "blurry, bad quality"),
                "clip": ["4", 1],
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {"images": ["8", 0], "filename_prefix": "paperbana"},
        },
    }

    # 프롬프트 큐에 추가
    resp = requests.post(
        f"{api_url}/prompt",
        json={"prompt": workflow},
        timeout=30,
    )
    resp.raise_for_status()
    prompt_id = resp.json()["prompt_id"]

    # 완료 대기 (최대 120초)
    for _ in range(120):
        time.sleep(1)
        history_resp = requests.get(f"{api_url}/history/{prompt_id}", timeout=10)
        history = history_resp.json()
        if prompt_id in history:
            outputs = history[prompt_id].get("outputs", {})
            for node_output in outputs.values():
                images = node_output.get("images", [])
                if images:
                    img_info = images[0]
                    img_resp = requests.get(
                        f"{api_url}/view",
                        params={
                            "filename": img_info["filename"],
                            "subfolder": img_info.get("subfolder", ""),
                            "type": img_info.get("type", "output"),
                        },
                        timeout=30,
                    )
                    img_resp.raise_for_status()
                    return img_resp.content

    raise TimeoutError("ComfyUI 이미지 생성 타임아웃 (120초)")


def generate_sd_webui(prompt: str, cfg: dict) -> bytes:
    """Stable Diffusion WebUI API로 이미지 생성, PNG bytes 반환"""
    api_url = cfg["api_url"].rstrip("/")

    payload = {
        "prompt": prompt,
        "negative_prompt": cfg.get("negative_prompt", "blurry, bad quality"),
        "steps": cfg.get("steps", 20),
        "cfg_scale": cfg.get("cfg_scale", 7),
        "width": cfg.get("width", 1024),
        "height": cfg.get("height", 768),
        "sampler_name": cfg.get("sampler", "Euler"),
        "override_settings": {
            "sd_model_checkpoint": cfg.get("model", "nanobana2"),
        },
    }

    resp = requests.post(f"{api_url}/sdapi/v1/txt2img", json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    img_b64 = data["images"][0]
    return base64.b64decode(img_b64)


def save_image(img_bytes: bytes, filename: str, output_dir: str) -> str:
    """이미지를 저장하고 절대 경로 반환"""
    os.makedirs(output_dir, exist_ok=True)
    # 확장자 보장
    if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
        filename = filename + ".jpg"
    out_path = os.path.join(output_dir, filename)

    # PNG → JPG 변환 (선택적, PIL이 있을 때만)
    try:
        from PIL import Image
        import io

        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img.save(out_path, "JPEG", quality=92)
    except ImportError:
        # PIL 없으면 그냥 bytes 저장
        with open(out_path, "wb") as f:
            f.write(img_bytes)

    return os.path.abspath(out_path)


def main():
    if len(sys.argv) < 4:
        print("ERROR:Usage: python generate_image.py <prompt> <filename> <output_dir> [api_type]")
        sys.exit(1)

    prompt = sys.argv[1]
    filename = sys.argv[2]
    output_dir = sys.argv[3]
    api_type_override = sys.argv[4] if len(sys.argv) > 4 else None

    try:
        config = load_config()
        cfg = config["nanobana2"]

        api_type = api_type_override or cfg.get("api_type", "comfyui")

        if api_type == "gemini":
            img_bytes = generate_gemini(prompt, cfg)
        elif api_type == "comfyui":
            img_bytes = generate_comfyui(prompt, cfg)
        elif api_type == "sd_webui":
            img_bytes = generate_sd_webui(prompt, cfg)
        else:
            print(f"ERROR:지원하지 않는 api_type: {api_type} (gemini, comfyui, sd_webui 중 선택)")
            sys.exit(1)

        out_path = save_image(img_bytes, filename, output_dir)
        print(f"SUCCESS:{out_path}")

    except requests.exceptions.ConnectionError as e:
        cfg_type = api_type_override or cfg.get("api_type", "comfyui")
        port = "8188" if cfg_type == "comfyui" else "7860"
        print(f"ERROR:API 서버에 연결할 수 없습니다. localhost:{port} 실행 여부를 확인하세요. ({e})")
        sys.exit(1)
    except ImportError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"ERROR:API 요청 실패: {e}")
        sys.exit(1)
    except TimeoutError as e:
        print(f"ERROR:{e}")
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"ERROR:설정 파일을 찾을 수 없습니다: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR:{type(e).__name__}: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
